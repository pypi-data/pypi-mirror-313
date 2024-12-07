from iccore.project import version, Version


def test_version():

    ver_str = "1.2.345"
    parsed = version.parse(ver_str)

    incremented = version.increment(parsed)
    assert incremented.as_string() == "1.2.346"
