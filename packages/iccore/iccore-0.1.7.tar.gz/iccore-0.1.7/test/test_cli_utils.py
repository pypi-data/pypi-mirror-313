from iccore.cli_utils import serialize_args


def test_cli_utils():

    cli_args = {"arg1": "val1", "arg2": "val2", "arg3": None}
    serialized = serialize_args(cli_args)
    assert serialized == " --arg1 val1 --arg2 val2 --arg3 "
