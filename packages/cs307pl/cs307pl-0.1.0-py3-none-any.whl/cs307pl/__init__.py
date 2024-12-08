import numpy as np


def main() -> None:
    print("Hello from cs307pl!")


def repr_array_pl(arr: np.ndarray, name: str = None) -> str:
    """
    Create a PrairieLearn usable representation of a NumPy array as a string
    with a specified variable name.

    Parameters
    ----------
    arr : np.ndarray
        The input NumPy array to be represented as a string.
    name : str, optional
        The variable name to be used in the string representation. If not
        provided, 'X' is used for 2D arrays and 'y' is used for 1D arrays.

    Returns
    -------
    str
        A string representation of the NumPy array with assignment to the
        specified variable name.
    """
    dim = arr.ndim
    if dim == 2:
        if name is None:
            name = "X"
        arr = repr(arr)
        spaces = arr.find("[", arr.find("[")) + len(name)
        arr = arr.replace("       ", "       " + " " * spaces)
        arr = arr.replace("nan", "np.nan")
    if dim == 1:
        if name is None:
            name = "y"
        arr = repr(arr)
        arr = "".join(arr.split())
        arr = arr.replace(",", ", ")
    return f"{name} = np." + arr


def repr_X_pl(X):
    return repr_array_pl(X, name="X")


def repr_x_pl(x):
    return repr_array_pl(x, name="x")


def repr_y_pl(y):
    return repr_array_pl(y, name="y")
