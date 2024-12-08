import numpy as np
from cs307pl import repr_array_pl


def test_repr_array_pl_2d_array():
    arr = np.array([[1, 2], [3, 4]])
    expected = "X = np.array([[1, 2],\n              [3, 4]])"
    assert repr_array_pl(arr) == expected


def test_repr_array_pl_2d_array_with_name():
    arr = np.array([[1.1, 2.1], [3.1, 4.1]])
    expected = "A = np.array([[1.1, 2.1],\n              [3.1, 4.1]])"
    assert repr_array_pl(arr, "A") == expected


def test_repr_array_pl_1d_array():
    arr = np.array([1, 2, 3, 4])
    expected = "y = np.array([1, 2, 3, 4])"
    assert repr_array_pl(arr) == expected


def test_repr_array_pl_1d_array_with_name():
    arr = np.array([1, 2, 3, 4])
    expected = "b = np.array([1, 2, 3, 4])"
    assert repr_array_pl(arr, "b") == expected


def test_repr_array_pl_with_nan():
    arr = np.array([[1.1, np.nan], [3.3, 4.4]])
    expected = "X = np.array([[1.1, np.nan],\n              [3.3, 4.4]])"
    assert repr_array_pl(arr) == expected
