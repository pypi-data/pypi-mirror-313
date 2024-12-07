"""Entrypoint for serving."""

import json
import os
import signal
from argparse import ArgumentParser
from subprocess import Popen

from union_runtime._lib.constants import UNION_SERVE_CONFIG_ENV_VAR, UNION_SERVE_CONFIG_FILE_NAME


def main():
    parser = ArgumentParser()
    parser.add_argument("--config", type=str)
    parser.add_argument("command", nargs="*")

    args = parser.parse_args()

    serve_config = {}
    env_vars = {}

    if args.config:
        config = json.loads(args.config)

        if config["code_uri"] is not None:
            from union_runtime._bin.download import download_code

            download_code(config["code_uri"], os.getcwd())

        if config["inputs"]:
            from union_runtime._bin.download import download_inputs

            serve_config["inputs"], env_vars = download_inputs(config["inputs"], os.getcwd())

    for name, value in env_vars.items():
        os.environ[name] = value

    serve_file = os.path.join(os.getcwd(), UNION_SERVE_CONFIG_FILE_NAME)
    with open(serve_file, "w") as f:
        json.dump(serve_config, f)

    os.environ[UNION_SERVE_CONFIG_ENV_VAR] = serve_file
    p = Popen(args.command)

    def handle_sigterm(signum, frame):
        p.send_signal(signum)

    signal.signal(signal.SIGTERM, handle_sigterm)
    returncode = p.wait()
    exit(returncode)


if __name__ == "__main__":
    main()
