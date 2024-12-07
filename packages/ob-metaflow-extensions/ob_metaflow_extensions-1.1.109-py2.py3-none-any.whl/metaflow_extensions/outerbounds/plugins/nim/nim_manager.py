import os
import time
import json
import requests
from urllib.parse import urlparse
from metaflow.metaflow_config import SERVICE_URL
from metaflow.metaflow_config_funcs import init_config
import sys
import random

NVCF_URL = "https://api.nvcf.nvidia.com"
NVCF_SUBMIT_ENDPOINT = f"{NVCF_URL}/v2/nvcf/pexec/functions"
NVCF_RESULT_ENDPOINT = f"{NVCF_URL}/v2/nvcf/pexec/status"

COMMON_HEADERS = {"accept": "application/json", "Content-Type": "application/json"}
POLL_INTERVAL = 1


class NimMetadata(object):
    def __init__(self):
        self._nvcf_chat_completion_models = []
        self._coreweave_chat_completion_models = []

        conf = init_config()

        if "OBP_AUTH_SERVER" in conf:
            auth_host = conf["OBP_AUTH_SERVER"]
        else:
            auth_host = "auth." + urlparse(SERVICE_URL).hostname.split(".", 1)[1]

        nim_info_url = "https://" + auth_host + "/generate/nim"

        if "METAFLOW_SERVICE_AUTH_KEY" in conf:
            headers = {"x-api-key": conf["METAFLOW_SERVICE_AUTH_KEY"]}
            res = requests.get(nim_info_url, headers=headers)
        else:
            headers = json.loads(os.environ.get("METAFLOW_SERVICE_HEADERS"))
            res = requests.get(nim_info_url, headers=headers)

        res.raise_for_status()
        self._ngc_api_key = res.json()["nvcf"]["api_key"]

        for model in res.json()["nvcf"]["functions"]:
            self._nvcf_chat_completion_models.append(
                {
                    "name": model["model_key"],
                    "function-id": model["id"],
                    "version-id": model["version"],
                }
            )
        for model in res.json()["coreweave"]["containers"]:
            self._coreweave_chat_completion_models.append(
                {"name": model["nim_name"], "ip-address": model["ip_addr"]}
            )

    def get_nvcf_chat_completion_models(self):
        return self._nvcf_chat_completion_models

    def get_coreweave_chat_completion_models(self):
        return self._coreweave_chat_completion_models

    def get_headers_for_nvcf_request(self):
        return {**COMMON_HEADERS, "Authorization": f"Bearer {self._ngc_api_key}"}

    def get_headers_for_coreweave_request(self):
        return COMMON_HEADERS


class NimManager(object):
    def __init__(self, models, backend):
        nim_metadata = NimMetadata()
        if backend == "managed":
            nvcf_models = [
                m["name"] for m in nim_metadata.get_nvcf_chat_completion_models()
            ]
            cw_models = [
                m["name"] for m in nim_metadata.get_coreweave_chat_completion_models()
            ]

            self.models = {}
            for m in models:
                if m in nvcf_models:
                    self.models[m] = NimChatCompletion(
                        model=m, provider="NVCF", nim_metadata=nim_metadata
                    )
                elif m in cw_models:
                    self.models[m] = NimChatCompletion(
                        model=m, provider="CoreWeave", nim_metadata=nim_metadata
                    )
                else:
                    raise ValueError(
                        f"Model {m} not supported by the Outerbounds @nim offering."
                        f"\nYou can choose from these options: {nvcf_models + cw_models}\n\n"
                        "Reach out to Outerbounds if there are other models you'd like supported."
                    )
        else:
            raise ValueError(
                f"Backend {backend} not supported by the Outerbounds @nim offering. Please reach out to Outerbounds."
            )


class NimChatCompletion(object):
    def __init__(
        self,
        model="meta/llama3-8b-instruct",
        provider="CoreWeave",
        nim_metadata=None,
        **kwargs,
    ):
        if nim_metadata is None:
            raise ValueError(
                "NimMetadata object is required to initialize NimChatCompletion object."
            )

        self._nim_metadata = nim_metadata
        self.compute_provider = provider
        self.invocations = []
        self.max_request_retries = int(
            os.environ.get("METAFLOW_EXT_HTTP_MAX_RETRIES", "10")
        )

        if self.compute_provider == "CoreWeave":
            cw_model_names = [
                m["name"]
                for m in self._nim_metadata.get_coreweave_chat_completion_models()
            ]
            self.model = model
            self.ip_address = self._nim_metadata.get_coreweave_chat_completion_models()[
                cw_model_names.index(model)
            ]["ip-address"]
            self.endpoint = f"http://{self.ip_address}:8000/v1/chat/completions"

        elif self.compute_provider == "NVCF":
            nvcf_model_names = [
                m["name"] for m in self._nim_metadata.get_nvcf_chat_completion_models()
            ]
            self.model = model
            self.function_id = self._nim_metadata.get_nvcf_chat_completion_models()[
                nvcf_model_names.index(model)
            ]["function-id"]
            self.version_id = self._nim_metadata.get_nvcf_chat_completion_models()[
                nvcf_model_names.index(model)
            ]["version-id"]

    def __call__(self, **kwargs):

        if self.compute_provider == "CoreWeave":
            request_data = {"model": self.model, **kwargs}
            response = requests.post(
                self.endpoint,
                headers=self._nim_metadata.get_headers_for_coreweave_request(),
                json=request_data,
            )
            response.raise_for_status()
            return response.json()

        elif self.compute_provider == "NVCF":

            request_data = {"model": self.model, **kwargs}
            request_url = f"{NVCF_SUBMIT_ENDPOINT}/{self.function_id}"

            attempts = 0
            while attempts < self.max_request_retries:
                try:
                    attempts += 1
                    response = requests.post(
                        request_url,
                        headers=self._nim_metadata.get_headers_for_nvcf_request(),
                        json=request_data,
                    )
                    response.raise_for_status()
                    if response.status_code == 202:
                        invocation_id = response.headers.get("NVCF-REQID")
                        self.invocations.append(invocation_id)
                    elif response.status_code == 200:
                        return response.json()
                except (
                    requests.exceptions.ConnectionError,
                    requests.exceptions.ReadTimeout,
                ) as e:
                    # ConnectionErrors are generally temporary errors like DNS resolution failures,
                    # timeouts etc.
                    print(
                        "received error of type {}. Retrying...".format(type(e)),
                        e,
                        file=sys.stderr,
                    )
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Double the delay for the next attempt
                    retry_delay += random.uniform(0, 1)  # Add jitter
                    retry_delay = min(retry_delay, 10)

            def _poll():
                poll_request_url = f"{NVCF_RESULT_ENDPOINT}/{invocation_id}"
                attempts = 0

                while attempts < self.max_request_retries:
                    try:
                        attempts += 1
                        poll_response = requests.get(
                            poll_request_url,
                            headers=self._nim_metadata.get_headers_for_nvcf_request(),
                        )
                        poll_response.raise_for_status()
                        if poll_response.status_code == 200:
                            return poll_response.json()
                        elif poll_response.status_code == 202:
                            return 202
                        else:
                            raise Exception(
                                f"NVCF returned {poll_response.status_code} status code. Please contact Outerbounds."
                            )
                    except (
                        requests.exceptions.ConnectionError,
                        requests.exceptions.ReadTimeout,
                    ) as e:
                        # ConnectionErrors are generally temporary errors like DNS resolution failures,
                        # timeouts etc.
                        print(
                            "received error of type {}. Retrying...".format(type(e)),
                            e,
                            file=sys.stderr,
                        )
                        time.sleep(retry_delay)
                        retry_delay *= 2  # Double the delay for the next attempt
                        retry_delay += random.uniform(0, 1)  # Add jitter
                        retry_delay = min(retry_delay, 10)

            while True:
                data = _poll()
                if data and data != 202:
                    return data
                time.sleep(POLL_INTERVAL)
