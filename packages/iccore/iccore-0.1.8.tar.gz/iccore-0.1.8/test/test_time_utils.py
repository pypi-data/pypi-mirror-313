import datetime
from iccore import time_utils


def test_timestamp_for_paths():

    test_time = datetime.datetime(2000, 5, 12, 14, 45, 23)

    time_str = time_utils.get_timestamp_for_paths(test_time)

    assert time_str == "20000512T14_45_23"
