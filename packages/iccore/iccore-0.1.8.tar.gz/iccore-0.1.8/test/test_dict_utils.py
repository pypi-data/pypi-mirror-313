from iccore import dict_utils


def test_merge_dicts():

    a = {"a": 1, "b": 2}
    b = {"c": 3, "d": 4}
    merged = dict_utils.merge_dicts(a, b)
    assert merged == {"a": 1, "b": 2, "c": 3, "d": 4}


def test_copy_without_type():

    content = {"a": 1, "b": [2, 3, 4], "c": 5}
    without_t = dict_utils.copy_without_type(content, list)
    assert without_t == {"a": 1, "c": 5}


def test_split_dict_on_type():

    content = {"a": 1, "b": [2, 3, 4], "c": 5}
    without_t, with_t = dict_utils.split_dict_on_type(content, list)
    assert with_t == {"b": [2, 3, 4]}
    assert without_t == {"a": 1, "c": 5}
