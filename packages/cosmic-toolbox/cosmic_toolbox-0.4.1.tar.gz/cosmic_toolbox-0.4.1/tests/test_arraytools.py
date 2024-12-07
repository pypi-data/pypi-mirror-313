import numpy as np
import pytest

from cosmic_toolbox.arraytools import (
    add_cols,
    arr2rec,
    arr_to_rec,
    delete_cols,
    dict2class,
    dict2rec,
    rec2arr,
    rec2dict,
)


@pytest.fixture
def example_array():
    return np.array([[1, 2], [3, 4], [5, 6]])


@pytest.fixture
def example_names():
    return ["col1", "col2"]


@pytest.fixture
def example_dict():
    return {"col1": [1, 2, 3], "col2": [4, 5, 6]}


@pytest.fixture
def example_dtype():
    return np.dtype([("col1", int), ("col2", int)])


def compare_dict(dict1, dict2):
    return np.all([dict1[key] == dict2[key] for key in dict1.keys() if key in dict2])


def test_arr2rec(example_array, example_names):
    expected = np.rec.array([(1, 2), (3, 4), (5, 6)], names=example_names)
    assert np.array_equal(arr2rec(example_array, example_names), expected)


def test_rec2arr(example_array, example_names):
    rec_array = np.rec.array([(1, 2), (3, 4), (5, 6)], names=example_names)
    expected = np.array([[1, 2], [3, 4], [5, 6]])
    assert np.array_equal(rec2arr(rec_array), expected)


def test_dict2rec(example_dict):
    expected = np.rec.array([(1, 4), (2, 5), (3, 6)], names=["col1", "col2"])
    assert np.array_equal(dict2rec(example_dict), expected)


def test_dict2rec_extended():
    x = {"a": np.zeros(5), "b": 3}
    x = dict2rec(x)
    assert np.all(x["a"] == np.zeros(5))
    assert np.all(x["b"] == np.array([3, 3, 3, 3, 3]))

    x = {"a": np.zeros(5), "b": np.ones((5, 2))}
    x = dict2rec(x)
    assert np.all(x["a"] == np.zeros(5))
    assert np.all(x["b"] == np.ones((5, 2)))


def test_rec2dict(example_dtype):
    rec_array = np.rec.array([(1, 4), (2, 5), (3, 6)], dtype=example_dtype)
    expected = {"col1": np.array([1, 2, 3]), "col2": np.array([4, 5, 6])}
    predicted = rec2dict(rec_array)
    assert compare_dict(expected, predicted)


def test_dict2class():
    # Test case 1
    d1 = {"a": [1, 2, 3], "b": 4}
    c1 = dict2class(d1)
    assert c1.a == [1, 2, 3]
    assert c1.b == 4

    # Test case 2
    d2 = {"x": "hello", "y": {"a": 5, "b": 6, "c": 7}}
    c2 = dict2class(d2)
    assert c2.x == "hello"
    assert c2.y == {"a": 5, "b": 6, "c": 7}

    # Test case 3: Empty dictionary
    d3 = {}
    c3 = dict2class(d3)
    assert hasattr(c3, "a") is False
    assert hasattr(c3, "b") is False


@pytest.fixture
def sample_data():
    data = np.array(
        [(1, 2, 3), (4, 5, 6), (7, 8, 9)], dtype=[("A", int), ("B", int), ("C", int)]
    )
    return data


# Define the tests using the fixture
def test_delete_cols_single_column(sample_data):
    result = delete_cols(sample_data, ["B"])
    expected_result = np.array([(1, 3), (4, 6), (7, 9)], dtype=[("A", int), ("C", int)])
    assert np.array_equal(result, expected_result)


def test_delete_cols_multiple_columns(sample_data):
    result = delete_cols(sample_data, ["B", "C"])
    expected_result = np.array([(1,), (4,), (7,)], dtype=[("A", int)])
    assert np.array_equal(result, expected_result)


def test_delete_cols_non_existent_column(sample_data):
    result = delete_cols(sample_data, ["D"])
    assert np.array_equal(result, sample_data)  # Should not modify the original data


def test_delete_cols_all_columns(sample_data):
    result = delete_cols(sample_data, ["A", "B", "C"])
    expected_result = np.array([], dtype=[])
    assert np.array_equal(result, expected_result)


def test_add_cols_single_scalar(sample_data):
    # Test case 1: Adding a single column with scalar data
    result = add_cols(sample_data, ["D"], data=0)
    assert "D" in result.dtype.names
    assert np.array_equal(result["D"], np.zeros_like(result["A"]))


def test_add_cols_multiple_scalars(sample_data):
    # Test case 2: Adding multiple columns with scalar data
    result = add_cols(sample_data, ["D", "E"], data=1)
    assert "D" in result.dtype.names
    assert "E" in result.dtype.names
    assert np.array_equal(result["D"], np.ones_like(result["A"]))
    assert np.array_equal(result["E"], np.ones_like(result["A"]))


def test_add_cols_single_1d_array(sample_data):
    # Test case 3: Adding a single column with 1D array data
    data_array = np.array([10, 20, 30])
    result = add_cols(sample_data, ["F"], data=data_array)
    assert "F" in result.dtype.names
    assert np.array_equal(result["F"], data_array)


def test_add_cols_multiple_2d_array(sample_data):
    # Test case 4: Adding multiple columns with 2D array data
    data_array = np.array([[10, 40, 70], [20, 50, 80]])
    result = add_cols(sample_data, ["F", "G"], data=data_array)
    assert "F" in result.dtype.names
    assert "G" in result.dtype.names
    assert np.array_equal(result["F"], data_array[0])
    assert np.array_equal(result["G"], data_array[1])


def test_arr_to_rec():
    arr = np.array([[1, 2], [3, 4]])
    dtype = [("a", np.int64), ("b", np.int64)]
    newrecarray = arr_to_rec(arr, dtype)
    assert np.all(newrecarray["a"] == arr[:, 0])
    assert np.all(newrecarray["b"] == arr[:, 1])
