from metaflow.plugins.secrets import SecretsProvider
from typing import Dict

import base64
import json
import requests
import time


class OuterboundsSecretsException(Exception):
    pass


class OuterboundsSecretsApiResponse:
    def __init__(self, response):
        self.response = response

    @property
    def secret_resource_id(self):
        return self.response["secret_resource_id"]

    @property
    def secret_backend_type(self):
        return self.response["secret_backend_type"]


class OuterboundsSecretsProvider(SecretsProvider):
    TYPE = "outerbounds"

    def get_secret_as_dict(self, secret_id, options={}, role=None):
        """
        Supports a special way of specifying secrets sources in outerbounds using the format:
            @secrets(sources=["outerbounds.<integrations_name>"])

        When invoked it makes a requests to the integrations secrets metadata endpoint on the
        keywest server to get the cloud resource id for a secret. It then uses that to invoke
        secrets manager on the core oss and returns the secrets.
        """
        headers = {"Content-Type": "application/json", "Connection": "keep-alive"}
        perimeter, integrations_secrets_metadata_url = self._get_secret_configs()
        integration_name = secret_id
        request_payload = {
            "perimeter_name": perimeter,
            "integration_name": integration_name,
        }
        response = self._make_request(
            integrations_secrets_metadata_url, headers, request_payload
        )
        secret_resource_id = response.secret_resource_id
        secret_backend_type = response.secret_backend_type

        from metaflow.plugins.secrets.secrets_decorator import (
            get_secrets_backend_provider,
        )

        secrets_provider = get_secrets_backend_provider(secret_backend_type)
        secret_dict = secrets_provider.get_secret_as_dict(
            secret_resource_id, options={}, role=role
        )

        # Outerbounds stores secrets as binaries. Hence we expect the returned secret to be
        # {<cloud-secret-name>: <base64 encoded full secret>}. We decode the secret here like:
        # 1. decode the base64 encoded full secret
        # 2. load the decoded secret as a json
        # 3. decode the base64 encoded values in the dict
        # 4. return the decoded dict
        binary_secret = next(iter(secret_dict.values()))
        return self._decode_secret(binary_secret)

    def _is_base64_encoded(self, data):
        try:
            if isinstance(data, str):
                # Check if the string can be base64 decoded
                base64.b64decode(data).decode("utf-8")
                return True
            return False
        except Exception:
            return False

    def _decode_secret(self, secret):
        try:
            result = {}
            secret_str = secret
            if self._is_base64_encoded(secret):
                # we check if the secret string is base64 encoded because the returned secret from
                # AWS secret manager is base64 encoded while the secret from GCP is not
                secret_str = base64.b64decode(secret).decode("utf-8")

            secret_dict = json.loads(secret_str)
            for key, value in secret_dict.items():
                result[key] = base64.b64decode(value).decode("utf-8")

            return result
        except Exception as e:
            raise OuterboundsSecretsException(f"Error decoding secret: {e}")

    def _get_secret_configs(self):
        from metaflow_extensions.outerbounds.remote_config import init_config
        from os import environ

        conf = init_config()
        if "OBP_PERIMETER" in conf:
            perimeter = conf["OBP_PERIMETER"]
        else:
            # if the perimeter is not in metaflow config, try to get it from the environment
            perimeter = environ.get("OBP_PERIMETER", "")

        if "OBP_INTEGRATIONS_SECRETS_METADATA_URL" in conf:
            integrations_secrets_metadata_url = conf[
                "OBP_INTEGRATIONS_SECRETS_METADATA_URL"
            ]
        else:
            # if the integrations secrets metadata url is not in metaflow config, try to get it from the environment
            integrations_secrets_metadata_url = environ.get(
                "OBP_INTEGRATIONS_SECRETS_METADATA_URL", ""
            )

        if not perimeter:
            raise OuterboundsSecretsException(
                "No perimeter set. Please make sure to run `outerbounds configure <...>` command which can be found on the Ourebounds UI or reach out to your Outerbounds support team."
            )

        if not integrations_secrets_metadata_url:
            raise OuterboundsSecretsException(
                "No integrations secrets metadata url set. Please notify your Outerbounds support team about this issue."
            )

        return perimeter, integrations_secrets_metadata_url

    def _make_request(self, url, headers: Dict, payload: Dict):
        try:
            from metaflow.metaflow_config import SERVICE_HEADERS

            request_headers = {**headers, **(SERVICE_HEADERS or {})}
        except ImportError:
            headers = self.headers

        retryable_status_codes = [409]
        json_payload = json.dumps(payload)
        for attempt in range(2):  # 0 = initial attempt, 1-2 = retries
            response = requests.get(url, data=json_payload, headers=request_headers)
            if response.status_code not in retryable_status_codes:
                break

            if attempt < 2:  # Don't sleep after the last attempt
                sleep_time = 0.5 * (attempt + 1)
                time.sleep(sleep_time)

        response = requests.get(url, data=json_payload, headers=request_headers)
        self._handle_error_response(response)
        return OuterboundsSecretsApiResponse(response.json())

    @staticmethod
    def _handle_error_response(response: requests.Response):
        if response.status_code >= 500:
            raise OuterboundsSecretsException(
                f"Server error: {response.text}. Please reach out to your Outerbounds support team."
            )

        body = response.json()
        status_code = body.get("error", {}).get("statusCode", response.status_code)
        if status_code == 404:
            raise OuterboundsSecretsException(f"Secret not found: {body}")

        if status_code >= 400:
            try:
                raise OuterboundsSecretsException(
                    f"status_code={status_code}\t*{body['error']['details']['kind']}*\n{body['error']['details']['message']}"
                )
            except KeyError:
                raise OuterboundsSecretsException(
                    f"status_code={status_code} Unexpected error: {body}"
                )
