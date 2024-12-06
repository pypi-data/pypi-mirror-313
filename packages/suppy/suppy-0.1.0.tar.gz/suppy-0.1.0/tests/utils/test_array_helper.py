import warnings
import numpy as np
import scipy.sparse as sp
from suppy.utils import LinearMapping
import pytest


def test_array_helper():

    # Create an array of incorrect type
    dense_arr = np.array([[1, 2], [0, 3]], dtype=np.float64)
    sp_arr = sp.csr_matrix(dense_arr)

    # Test the linear mapping function
    dense_map = LinearMapping(dense_arr)
    sp_map = LinearMapping(sp_arr)

    # Test the dense linear mapping function
    assert str(dense_arr) == str(dense_map)
    assert np.array_equal(1 + dense_arr, 1 + dense_map)
    assert np.array_equal(1 - dense_arr, 1 - dense_map)

    assert np.array_equal(dense_arr + dense_arr, dense_map + dense_map)
    assert np.array_equal(dense_arr**2, dense_map**2)

    x = np.array([1, 1])
    assert np.array_equal(dense_arr @ x, dense_map @ x)

    assert len(dense_map) == len(dense_arr)

    # do the same for sp_arr
    assert str(dense_arr) == str(dense_map)

    # addition of e.g. scalars is not defined on sparse arrays
    with pytest.raises(NotImplementedError):
        sp_map + 1

    assert np.array_equal(sp_map.todense() + sp_map, 2 * sp_map.todense())
