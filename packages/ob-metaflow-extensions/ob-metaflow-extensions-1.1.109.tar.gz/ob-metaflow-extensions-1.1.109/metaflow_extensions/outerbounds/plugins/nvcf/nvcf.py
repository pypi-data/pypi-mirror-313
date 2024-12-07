import json
import os
import threading
from urllib.parse import urlparse
from urllib.request import HTTPError, Request, URLError, urlopen

from metaflow import util
from metaflow.exception import MetaflowException
from metaflow.mflog import (
    BASH_SAVE_LOGS,
    bash_capture_logs,
    export_mflog_env_vars,
    tail_logs,
    get_log_tailer,
)
import requests
from metaflow.metaflow_config_funcs import init_config


class NvcfException(MetaflowException):
    headline = "Nvidia error"


class NvcfKilledException(MetaflowException):
    headline = "Nvidia job killed"


# Redirect structured logs to $PWD/.logs/
LOGS_DIR = "$PWD/.logs"
STDOUT_FILE = "mflog_stdout"
STDERR_FILE = "mflog_stderr"
STDOUT_PATH = os.path.join(LOGS_DIR, STDOUT_FILE)
STDERR_PATH = os.path.join(LOGS_DIR, STDERR_FILE)


class Nvcf(object):
    def __init__(self, metadata, datastore, environment):
        self.metadata = metadata
        self.datastore = datastore
        self.environment = environment

    def launch_job(
        self,
        step_name,
        step_cli,
        task_spec,
        code_package_sha,
        code_package_url,
        code_package_ds,
        env={},
    ):
        mflog_expr = export_mflog_env_vars(
            datastore_type=code_package_ds,
            stdout_path=STDOUT_PATH,
            stderr_path=STDERR_PATH,
            **task_spec,
        )
        init_cmds = self.environment.get_package_commands(
            code_package_url, code_package_ds
        )
        init_expr = " && ".join(init_cmds)
        heartbeat_expr = f'python -m metaflow_extensions.outerbounds.plugins.nvcf.heartbeat_store "$MAIN_PID" {code_package_ds} nvcf_heartbeats & HEARTBEAT_PID=$!;'
        step_expr = bash_capture_logs(
            " && ".join(
                self.environment.bootstrap_commands(step_name, code_package_ds)
                + [step_cli + " & MAIN_PID=$!; " + heartbeat_expr + " wait $MAIN_PID"]
            )
        )

        # construct an entry point that
        # 1) initializes the mflog environment (mflog_expr)
        # 2) bootstraps a metaflow environment (init_expr)
        # 3) executes a task (step_expr)

        cmd_str = "mkdir -p %s && %s && %s && %s; " % (
            LOGS_DIR,
            mflog_expr,
            init_expr,
            step_expr,
        )
        # after the task has finished, we save its exit code (fail/success)
        # and persist the final logs. The whole entrypoint should exit
        # with the exit code (c) of the task.
        #
        # Note that if step_expr OOMs, this tail expression is never executed.
        # We lose the last logs in this scenario.
        cmd_str += (
            "c=$?; kill $HEARTBEAT_PID; wait $HEARTBEAT_PID; %s; exit $c"
            % BASH_SAVE_LOGS
        )
        cmd_str = (
            '${METAFLOW_INIT_SCRIPT:+eval \\"${METAFLOW_INIT_SCRIPT}\\"} && %s'
            % cmd_str
        )
        self.job = Job(
            'bash -c "%s"' % cmd_str, env, task_spec, self.datastore._storage_impl
        )
        self.job.submit()

    def wait(self, stdout_location, stderr_location, echo=None):
        def wait_for_launch(job):
            status = job.status
            echo(
                "Task status: %s..." % status,
                "stderr",
                _id=job.id,
            )

        prefix = b"[%s] " % util.to_bytes(self.job.id)
        stdout_tail = get_log_tailer(stdout_location, self.datastore.TYPE)
        stderr_tail = get_log_tailer(stderr_location, self.datastore.TYPE)

        # 1) Loop until the job has started
        wait_for_launch(self.job)

        # 2) Tail logs until the job has finished
        tail_logs(
            prefix=prefix,
            stdout_tail=stdout_tail,
            stderr_tail=stderr_tail,
            echo=echo,
            has_log_updates=lambda: self.job.is_running,
        )

        echo(
            "Task finished with exit code %s." % self.job.result.get("exit_code"),
            "stderr",
            _id=self.job.id,
        )
        if self.job.has_failed:
            raise NvcfException("This could be a transient error. Use @retry to retry.")


class JobStatus(object):
    SUBMITTED = "SUBMITTED"
    RUNNING = "RUNNING"
    SUCCESSFUL = "SUCCESSFUL"
    FAILED = "FAILED"


nvcf_url = "https://api.nvcf.nvidia.com"
submit_endpoint = f"{nvcf_url}/v2/nvcf/pexec/functions"
result_endpoint = f"{nvcf_url}/v2/nvcf/pexec/status"


class Job(object):
    def __init__(self, command, env, task_spec, backend):
        self._payload = {
            "command": command,
            "env": {k: v for k, v in env.items() if v is not None},
        }
        self._result = {}

        conf = init_config()
        if "OBP_AUTH_SERVER" in conf:
            auth_host = conf["OBP_AUTH_SERVER"]
        else:
            auth_host = "auth." + urlparse(SERVICE_URL).hostname.split(".", 1)[1]

        # NOTE: reusing the same auth_host as the one used in NimMetadata,
        # however, user should not need to use nim container to use @nvidia.
        # May want to refactor this to a common endpoint.
        nim_info_url = "https://" + auth_host + "/generate/nim"

        if "METAFLOW_SERVICE_AUTH_KEY" in conf:
            headers = {"x-api-key": conf["METAFLOW_SERVICE_AUTH_KEY"]}
            res = requests.get(nim_info_url, headers=headers)
        else:
            headers = json.loads(os.environ.get("METAFLOW_SERVICE_HEADERS"))
            res = requests.get(nim_info_url, headers=headers)

        res.raise_for_status()
        self._ngc_api_key = res.json()["nvcf"]["api_key"]

        for f in res.json()["nvcf"]["functions"]:
            if f["model_key"] == "metaflow_task_executor":
                self._function_id = f["id"]

        flow_name = task_spec.get("flow_name")
        run_id = task_spec.get("run_id")
        step_name = task_spec.get("step_name")
        task_id = task_spec.get("task_id")
        retry_count = task_spec.get("retry_count")

        heartbeat_prefix = "/".join(
            (flow_name, str(run_id), step_name, str(task_id), str(retry_count))
        )

        ## import is done here to avoid the following warning:
        # RuntimeWarning: 'metaflow_extensions.outerbounds.plugins.nvcf.heartbeat_store' found in sys.modules
        # after import of package 'metaflow_extensions.outerbounds.plugins.nvcf', but prior to execution of
        # 'metaflow_extensions.outerbounds.plugins.nvcf.heartbeat_store'; this may result in unpredictable behaviour
        from metaflow_extensions.outerbounds.plugins.nvcf.heartbeat_store import (
            HeartbeatStore,
        )

        store = HeartbeatStore(
            main_pid=None,
            storage_backend=backend,
        )

        self.heartbeat_thread = threading.Thread(
            target=store.emit_heartbeat,
            args=(
                heartbeat_prefix,
                "nvcf_heartbeats",
            ),
            daemon=True,
        )
        self.heartbeat_thread.start()

    def submit(self):
        try:
            headers = {
                "Authorization": f"Bearer {self._ngc_api_key}",
                "Content-Type": "application/json",
            }
            request_data = json.dumps(self._payload).encode()
            request = Request(
                f"{submit_endpoint}/{self._function_id}",
                data=request_data,
                headers=headers,
            )
            response = urlopen(request)
            self._invocation_id = response.headers.get("NVCF-REQID")
            if response.getcode() == 200:
                data = json.loads(response.read())
                if data.get("exit_code") == 0:
                    self._status = JobStatus.SUCCESSFUL
                else:
                    self._status = JobStatus.FAILED
                self._result = data
            elif response.getcode() == 202:
                self._status = JobStatus.SUBMITTED
            else:
                self._status = JobStatus.FAILED
            # TODO: Handle 404s nicely
        except (HTTPError, URLError) as e:
            self._state = JobStatus.FAILED
            raise e

    @property
    def status(self):
        if self._status not in [JobStatus.SUCCESSFUL, JobStatus.FAILED]:
            self._poll()
        return self._status

    @property
    def id(self):
        return self._invocation_id

    @property
    def is_running(self):
        return self.status == JobStatus.SUBMITTED

    @property
    def has_failed(self):
        return self.status == JobStatus.FAILED

    @property
    def result(self):
        return self._result

    def _poll(self):
        try:
            headers = {
                "Authorization": f"Bearer {self._ngc_api_key}",
                "Content-Type": "application/json",
            }
            request = Request(
                f"{result_endpoint}/{self._invocation_id}", headers=headers
            )
            response = urlopen(request)
            if response.getcode() == 200:
                data = json.loads(response.read())
                # TODO: Propagate the internal error forward
                if data.get("exit_code") == 0:
                    self._status = JobStatus.SUCCESSFUL
                else:
                    self._status = JobStatus.FAILED
                self._result = data
            elif response.getcode() in [400, 500]:
                self._status = JobStatus.FAILED
        except (HTTPError, URLError) as e:
            print(f"Error occurred while polling for result: {e}")
