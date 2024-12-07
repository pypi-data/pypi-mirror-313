from functools import cache

from union_runtime._lib.constants import UNION_SERVE_CONFIG_ENV_VAR


@cache
def get_input(name: str) -> str:
    """Get inputs for application or endpoint."""
    import json
    import os

    config_file = os.getenv(UNION_SERVE_CONFIG_ENV_VAR)

    with open(config_file, "r") as f:
        inputs = json.load(f)["inputs"]

    return inputs[name]
