import argparse
import os

from accelerate.utils import ComputeEnvironment

from .config_args import cache_dir, default_config_file, default_yaml_config_file, load_config_from_file  # noqa: F401
from .config_utils import _ask_field, _ask_options, _convert_compute_environment  # noqa: F401


description = "Launches a series of prompts to create and save a `default_config.yaml` configuration file for your training system. Should always be ran first on your machine"


def config_command_parser(subparsers=None):
    if subparsers is not None:
        parser = subparsers.add_parser("config", description=description)
    else:
        parser = argparse.ArgumentParser("Accelerate config command", description=description)

    parser.add_argument(
        "--config_file",
        default=None,
        help=(
            "The path to use to store the config file. Will default to a file named default_config.yaml in the cache "
            "location, which is the content of the environment `HF_HOME` suffixed with 'accelerate', or if you don't have "
            "such an environment variable, your cache directory ('~/.cache' or the content of `XDG_CACHE_HOME`) suffixed "
            "with 'huggingface'."
        ),
    )

    if subparsers is not None:
        parser.set_defaults(func=config_command)
    return parser


def config_command(args):
    config = load_config_from_file(default_config_file)
    if args.config_file is not None:
        config_file = args.config_file
    else:
        if not os.path.isdir(cache_dir):
            os.makedirs(cache_dir)
        config_file = default_yaml_config_file

    if config_file.endswith(".json"):
        config.to_json_file(config_file)
    else:
        config.to_yaml_file(config_file)
    print(f"accelerate configuration saved at {config_file}")


def main():
    parser = config_command_parser()
    args = parser.parse_args()
    config_command(args)


if __name__ == "__main__":
    main()