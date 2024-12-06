import warnings
import numpy as np
from suppy.utils import ensure_float_array
from suppy.utils import Bounds
import pytest


def test_ensure_float_array_warning():
    class MyClass:
        @ensure_float_array
        def my_method(self, arr):
            return arr

    # Test with an array of incorrect type (int32)
    arr = np.array([1, 2, 3], dtype=np.int32)

    # Capture the warning
    with warnings.catch_warnings(record=True) as w:
        result = MyClass().my_method(arr)

        # Check if the warning is thrown
        assert len(w) == 1
        assert issubclass(w[-1].category, UserWarning)
        assert (
            str(w[-1].message) == "Array is not of type float32 or float64, converting to float64"
        )

        # Check if the array is converted to float64
        assert result.dtype == np.float64


def test_ensure_float_array_no_warning():
    class MyClass:
        @ensure_float_array
        def my_method(self, arr):
            return arr

    # Test with an array of correct type (float32)
    arr = np.array([1.0, 2.0, 3.0], dtype=np.float32)

    # Capture the warning
    with warnings.catch_warnings(record=True) as w:
        result = MyClass().my_method(arr)

        # Check if no warning is thrown
        assert len(w) == 0

        # Check if the array remains unchanged
        assert result.dtype == np.float32


def test_ensure_float_array_conversion_failure():
    class MyClass:
        @ensure_float_array
        def my_method(self, arr):
            return arr

    # Create an array that cannot be converted to float64 (array of strings)
    arr = np.array(["a", "b", "c"], dtype=np.str_)

    # Check if TypeError is raised when conversion fails
    with pytest.raises(TypeError, match="Failed to convert array to float64"):
        MyClass().my_method(arr)
