from iccore import runtime
from iccore import logging_utils


def launch_common(args):
    runtime.ctx.set_is_dry_run(args.dry_run)
    logging_utils.setup_default_logger()


def serialize_args(cli_args: dict[str, str | None], delimiter="--") -> str:
    """
    Convert command line args given as dict key, value pairs
    to a string format.
    """
    ret = ""
    for key, value in cli_args.items():
        if value is None:
            value = ""
        ret += f" {delimiter}{key} {value}"
    return ret
