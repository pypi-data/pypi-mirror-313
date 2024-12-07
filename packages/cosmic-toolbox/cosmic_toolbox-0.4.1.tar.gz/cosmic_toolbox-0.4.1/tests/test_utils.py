import numpy as np

from cosmic_toolbox.utils import arg_str_to_dict, is_between, parse_list, parse_sequence


def test_arg_str_to_dict():
    arg_str = "{arg1:10, arg2:3.14, arg3:value}"
    expected_result = {"arg1": 10, "arg2": 3.14, "arg3": "value"}
    result = arg_str_to_dict(arg_str)
    assert result == expected_result, f"Expected {expected_result}, but got {result}"

    arg_str = "{arg:value}"
    expected_result = {"arg": "value"}
    result = arg_str_to_dict(arg_str)
    assert result == expected_result, f"Expected {expected_result}, but got {result}"

    arg_str = "{arg1:1,arg2:2,arg3:3}"
    expected_result = {"arg1": 1, "arg2": 2, "arg3": 3}
    result = arg_str_to_dict(arg_str)
    assert result == expected_result, f"Expected {expected_result}, but got {result}"

    arg_str = "{batch_size:10000,epochs:1000,hidden_units:(512,512,512)}"
    expected_result = {
        "batch_size": 10000,
        "epochs": 1000,
        "hidden_units": (512, 512, 512),
    }
    result = arg_str_to_dict(arg_str)
    assert result == expected_result, f"Expected {expected_result}, but got {result}"


def test_parse_sequence():
    s = "(1,2,3)"
    assert parse_sequence(s) == (1, 2, 3)
    s = "(1,2,3,)"
    assert parse_sequence(s) == (1, 2, 3)
    s = "[1,2,3,4]"
    assert parse_sequence(s) == [1, 2, 3, 4]


def test_parse_list():
    s = "(1,2,3)"
    assert parse_list(s) == [1, 2, 3]
    s = "(1,2,3,)"
    assert parse_list(s) == [1, 2, 3]
    s = "[1,2,3,4]"
    assert parse_list(s) == [1, 2, 3, 4]


def test_is_between():
    # Test case 1: x is between min and max
    assert is_between(5, 2, 10)

    # Test case 2: x is equal to min
    assert not is_between(2, 2, 10)

    # Test case 3: x is equal to max
    assert not is_between(10, 2, 10)

    # Test case 4: x is smaller than min
    assert not is_between(1, 2, 10)

    # Test case 5: x is greater than max
    assert not is_between(15, 2, 10)

    # Test case 6: Test with negative values
    assert is_between(-5, -10, -2)

    # Test case 7: Test with floating-point values
    assert is_between(3.5, 2.0, 5.0)

    # Test case 8: Test with min and max swapped
    assert not is_between(7, 10, 2)

    # Test case 9: Test with equal min and max
    assert not is_between(5, 5, 5)

    # Test case 10: Test with numpy array input
    np_array = np.arange(10)
    expected_result = np.array(
        [False, False, False, True, True, True, False, False, False, False]
    )
    assert np.array_equal(is_between(np_array, 2, 6), expected_result)
