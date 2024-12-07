from functools import partial
from metaflow.decorators import FlowDecorator
from metaflow import current
from .nim_manager import NimManager


class NimDecorator(FlowDecorator):
    """
    This decorator is used to run NIM containers in Metaflow tasks as sidecars.

    User code call
    -----------
    @nim(
        models=['meta/llama3-8b-instruct', 'meta/llama3-70b-instruct'],
        backend='managed'
    )

    Valid backend options
    ---------------------
    - 'managed': Outerbounds selects a compute provider based on the model.
    - 🚧 'dataplane': Run in your account.

    Valid model options
    ----------------
        - 'meta/llama3-8b-instruct': 8B parameter model
        - 'meta/llama3-70b-instruct': 70B parameter model
        - Upon request, any model here: https://nvcf.ngc.nvidia.com/functions?filter=nvidia-functions

    Parameters
    ----------
    models: list[NIM]
        List of NIM containers running models in sidecars.
    backend: str
        Compute provider to run the NIM container.
    """

    name = "nim"
    defaults = {
        "models": [],
        "backend": "managed",
    }

    def flow_init(
        self, flow, graph, environment, flow_datastore, metadata, logger, echo, options
    ):
        current._update_env(
            {
                "nim": NimManager(
                    models=self.attributes["models"], backend=self.attributes["backend"]
                )
            }
        )
