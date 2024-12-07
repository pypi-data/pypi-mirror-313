import os
import sys

from metaflow.exception import MetaflowException
from metaflow.decorators import StepDecorator
from metaflow.metadata_provider.util import sync_local_metadata_to_datastore
from metaflow.metaflow_config import DATASTORE_LOCAL_DIR
from metaflow.sidecar import Sidecar
from metaflow.plugins.timeout_decorator import get_run_time_limit_for_task
from .nvcf import NvcfException

from metaflow.metadata_provider import MetaDatum


class NvcfDecorator(StepDecorator):
    name = "nvidia"
    # defaults = {"function_id": "9e5647f2-740f-4101-a129-1c961a075575"}
    defaults = {}
    # "0817006f-018b-4590-b2a5-6cf9d64d9d9a"}
    #

    package_url = None
    package_sha = None

    # Refer https://github.com/Netflix/metaflow/blob/master/docs/lifecycle.png
    # to understand where these functions are invoked in the lifecycle of a
    # Metaflow flow.
    def step_init(self, flow, graph, step, decos, environment, flow_datastore, logger):
        # Executing NVCF functions requires a non-local datastore.
        if flow_datastore.TYPE not in ("s3", "azure", "gs"):
            raise NvcfException(
                "The *@nvidia* decorator requires --datastore=s3 or --datastore=azure or --datastore=gs at the moment."
            )
        # if self.attributes["function_id"] is None:
        #     raise NvcfException(
        #         "The *@nvidia* decorator requires a function_id. Please reach out to Outerbounds if you are unsure how to get access to one."
        #     )
        # Set internal state.
        self.logger = logger
        self.environment = environment
        self.step = step
        self.flow_datastore = flow_datastore

        if any([deco.name == "kubernetes" for deco in decos]):
            raise MetaflowException(
                "Step *{step}* is marked for execution both on Kubernetes and "
                "Nvidia. Please use one or the other.".format(step=step)
            )
        if any([deco.name == "parallel" for deco in decos]):
            raise MetaflowException(
                "Step *{step}* contains a @parallel decorator "
                "with the @nvidia decorator. @parallel is not supported with @nvidia.".format(
                    step=step
                )
            )

        # Set run time limit for the NVCF function.
        self.run_time_limit = get_run_time_limit_for_task(decos)
        if self.run_time_limit < 60:
            raise NvcfException(
                "The timeout for step *{step}* should be at least 60 seconds for "
                "execution with @nvidia.".format(step=step)
            )

    def runtime_init(self, flow, graph, package, run_id):
        # Set some more internal state.
        self.flow = flow
        self.graph = graph
        self.package = package
        self.run_id = run_id

    def runtime_task_created(
        self, task_datastore, task_id, split_index, input_paths, is_cloned, ubf_context
    ):
        if not is_cloned:
            self._save_package_once(self.flow_datastore, self.package)

    def runtime_step_cli(
        self, cli_args, retry_count, max_user_code_retries, ubf_context
    ):
        if retry_count <= max_user_code_retries:
            # after all attempts to run the user code have failed, we don't need
            # to execute on NVCF anymore. We can execute possible fallback
            # code locally.
            cli_args.commands = ["nvidia", "step"]
            cli_args.command_args.append(self.package_sha)
            cli_args.command_args.append(self.package_url)
            cli_args.command_options.update(self.attributes)
            # cli_args.command_options["run-time-limit"] = self.run_time_limit
            cli_args.entrypoint[0] = sys.executable

    def task_pre_step(
        self,
        step_name,
        task_datastore,
        metadata,
        run_id,
        task_id,
        flow,
        graph,
        retry_count,
        max_retries,
        ubf_context,
        inputs,
    ):
        self.metadata = metadata
        self.task_datastore = task_datastore

        # task_pre_step may run locally if fallback is activated for @catch
        # decorator.

        if "NVCF_CONTEXT" in os.environ:
            meta = {}

            meta["nvcf-function-id"] = os.environ.get("NVCF_FUNCTION_ID")
            meta["nvcf-function-version-id"] = os.environ.get(
                "NVCF_FUNCTION_VERSION_ID"
            )
            meta["nvcf-region"] = os.environ.get("NVCF_REGION")
            meta["nvcf-ncaid"] = os.environ.get("NVCF_NCAID")
            meta["nvcf-sub"] = os.environ.get("NVCF_SUB")
            meta["nvcf-instancetype"] = os.environ.get("NVCF_INSTANCETYPE")
            meta["nvcf-reqid"] = os.environ.get("NVCF_REQID")
            meta["nvcf-env"] = os.environ.get("NVCF_ENV")
            meta["nvcf-backend"] = os.environ.get("NVCF_BACKEND")
            meta["nvcf-function-name"] = os.environ.get("NVCF_FUNCTION_NAME")
            meta["nvcf-nspectid"] = os.environ.get("NVCF_NSPECTID")

            entries = [
                MetaDatum(field=k, value=v, type=k, tags=[])
                for k, v in meta.items()
                if v is not None
            ]
            # Register book-keeping metadata for debugging.
            metadata.register_metadata(run_id, step_name, task_id, entries)

            self._save_logs_sidecar = Sidecar("save_logs_periodically")
            self._save_logs_sidecar.start()

    def task_finished(
        self, step_name, flow, graph, is_task_ok, retry_count, max_retries
    ):
        # task_finished may run locally if fallback is activated for @catch
        # decorator.
        if "NVCF_CONTEXT" in os.environ:
            # If `local` metadata is configured, we would need to copy task
            # execution metadata from the NVCF container to user's
            # local file system after the user code has finished execution.
            # This happens via datastore as a communication bridge.
            if hasattr(self, "metadata") and self.metadata.TYPE == "local":
                sync_local_metadata_to_datastore(
                    DATASTORE_LOCAL_DIR, self.task_datastore
                )

        try:
            self._save_logs_sidecar.terminate()
        except:
            # Best effort kill
            pass

    @classmethod
    def _save_package_once(cls, flow_datastore, package):
        if cls.package_url is None:
            cls.package_url, cls.package_sha = flow_datastore.save_data(
                [package.blob], len_hint=1
            )[0]
