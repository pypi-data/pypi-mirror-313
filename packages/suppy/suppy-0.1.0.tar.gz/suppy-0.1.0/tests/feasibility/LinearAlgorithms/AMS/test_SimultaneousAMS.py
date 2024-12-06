import numpy as np
import pytest
import scipy.sparse as sparse
from suppy.feasibility import SimultaneousAMS
from suppy.utils import LinearMapping


@pytest.fixture
def get_full_variables():
    A = np.array([[1, 1], [-1, 1], [1, 0], [0, 1]])
    lb = np.array([-2, -2, -3 / 2, -3 / 2])
    ub = -1 * lb
    return A, lb, ub


@pytest.fixture
def get_sparse_variables():
    A = sparse.csr_matrix([[1, 1], [-1, 1], [1, 0], [0, 1]])
    lb = np.array([-2, -2, -3 / 2, -3 / 2])
    ub = -1 * lb
    return A, lb, ub


def test_SimultaneousAMS_no_relaxation_no_weights_constructor_full(get_full_variables):
    """
    Test the SimultaneousAMS constructor with no relaxation and a full
    matrix.
    """
    A, lb, ub = get_full_variables
    alg = SimultaneousAMS(A, lb, ub)

    assert isinstance(alg.A, LinearMapping)
    assert np.array_equal(alg.A, A)
    assert np.array_equal(alg.Bounds.l, lb)
    assert np.array_equal(alg.Bounds.u, ub)
    assert np.array_equal(alg.weights, np.ones(len(A)) / len(A))
    assert alg.relaxation == 1.0
    assert alg.algorithmic_relaxation == 1.0


def test_SimultaneousAMS_no_relaxation_no_weights_constructor_sparse(
    get_sparse_variables,
):
    """
    Test the SimultaneousAMS constructor with no relaxation and a sparse
    matrix.
    """
    A, lb, ub = get_sparse_variables
    alg = SimultaneousAMS(A, lb, ub)

    assert isinstance(alg.A, LinearMapping)
    assert np.array_equal(alg.A.todense(), A.todense())
    assert np.array_equal(alg.Bounds.l, lb)
    assert np.array_equal(alg.Bounds.u, ub)
    assert np.array_equal(alg.weights, np.ones(A.shape[0]) / A.shape[0])
    assert alg.relaxation == 1.0
    assert alg.algorithmic_relaxation == 1.0


def testSimultaneousAMS_relaxation_weights_constructor_full(get_full_variables):
    """
    Test the SimultaneousAMS constructor with relaxation and custom
    weights.
    """
    A, lb, ub = get_full_variables
    alg = SimultaneousAMS(
        A, lb, ub, algorithmic_relaxation=1.5, relaxation=1.5, weights=np.ones(len(A))
    )

    assert isinstance(alg.A, LinearMapping)
    assert np.array_equal(alg.A, A)
    assert np.array_equal(alg.Bounds.l, lb)
    assert np.array_equal(alg.Bounds.u, ub)
    assert np.array_equal(alg.weights, np.ones(len(A)) / A.shape[0])
    assert alg.algorithmic_relaxation == 1.5
    assert alg.relaxation == 1.5


def testSimultaneousAMS_relaxation_weights_constructor_sparse(get_sparse_variables):
    """
    Test the SimultaneousAMS constructor with relaxation and custom
    weights.
    """
    A, lb, ub = get_sparse_variables
    alg = SimultaneousAMS(
        A,
        lb,
        ub,
        algorithmic_relaxation=1.5,
        relaxation=1.5,
        weights=np.ones(A.shape[0]),
    )

    assert isinstance(alg.A, LinearMapping)
    assert np.array_equal(alg.A.todense(), A.todense())
    assert np.array_equal(alg.Bounds.l, lb)
    assert np.array_equal(alg.Bounds.u, ub)
    assert np.array_equal(alg.weights, np.ones(A.shape[0]) / A.shape[0])
    assert alg.algorithmic_relaxation == 1.5
    assert alg.relaxation == 1.5


def test_SimultaneousAMS_step_full(get_full_variables):
    """Test the step function of the SimultaneousAMS class."""
    A, lb, ub = get_full_variables
    alg = SimultaneousAMS(A, lb, ub, weights=np.ones(len(A)) / A.shape[0])

    x_1 = np.array([1.2, 1.2])
    x_2 = np.array([2.0, 2.0])
    x_3 = np.array([-1.2, -1.2])
    x_4 = np.array([-2.0, -2.0])
    x_5 = np.array([2.0, -2.0])

    x_n = alg.step(x_1)
    assert np.all(np.abs(x_n - np.array([1.15, 1.15])) < 1e-10)
    assert np.array_equal(x_n, x_1)

    # check that project gives the same result as step
    x_1 = np.array([1.2, 1.2])
    x_proj = alg.project(x_1)
    assert np.all(np.abs(x_proj - np.array([1.15, 1.15])) < 1e-10)
    assert np.array_equal(x_proj, x_1)
    assert np.array_equal(x_proj, x_n)

    x_n = alg.step(x_2)
    assert np.all(np.abs(x_n - 1 / 4 * np.array([6.5, 6.5])) < 1e-10)
    assert np.array_equal(x_n, x_2)

    x_n = alg.step(x_3)
    assert np.all(np.abs(x_n - np.array([-1.15, -1.15])) < 1e-10)
    assert np.array_equal(x_n, x_3)

    x_n = alg.step(x_4)
    assert np.all(np.abs(x_n - 1 / 4 * np.array([-6.5, -6.5])) < 1e-10)
    assert np.array_equal(x_n, x_4)

    x_n = alg.step(x_5)
    assert np.all(np.abs(x_n - 1 / 4 * np.array([6.5, -6.5])) < 1e-10)
    assert np.array_equal(x_n, x_5)


def test_SimultaneousAMS_step_sparse(get_sparse_variables):
    """Test the step function of the SimultaneousAMS class."""
    A, lb, ub = get_sparse_variables

    alg = SimultaneousAMS(A, lb, ub, weights=np.ones(A.shape[0]))

    x_1 = np.array([1.2, 1.2])
    x_2 = np.array([2.0, 2.0])
    x_3 = np.array([-1.2, -1.2])
    x_4 = np.array([-2.0, -2.0])
    x_5 = np.array([2.0, -2.0])

    x_n = alg.step(x_1)
    assert np.all(np.abs(x_n - np.array([1.15, 1.15])) < 1e-10)
    assert np.array_equal(x_n, x_1)

    # check that project gives the same result as step
    x_1 = np.array([1.2, 1.2])
    x_proj = alg.project(x_1)
    assert np.all(np.abs(x_proj - np.array([1.15, 1.15])) < 1e-10)
    assert np.array_equal(x_proj, x_1)
    assert np.array_equal(x_proj, x_n)

    x_n = alg.step(x_2)
    assert np.all(np.abs(x_n - 1 / 4 * np.array([6.5, 6.5])) < 1e-10)
    assert np.array_equal(x_n, x_2)

    x_n = alg.step(x_3)
    assert np.all(np.abs(x_n - np.array([-1.15, -1.15])) < 1e-10)
    assert np.array_equal(x_n, x_3)

    x_n = alg.step(x_4)
    assert np.all(np.abs(x_n - 1 / 4 * np.array([-6.5, -6.5])) < 1e-10)
    assert np.array_equal(x_n, x_4)

    x_n = alg.step(x_5)
    assert np.all(np.abs(x_n - 1 / 4 * np.array([6.5, -6.5])) < 1e-10)
    assert np.array_equal(x_n, x_5)


def test_SimultaneousAMS_algorithmic_relaxation_step(get_sparse_variables):
    """Test the step function with relaxation of the SimultaneousAMS class."""
    A, lb, ub = get_sparse_variables

    alg = SimultaneousAMS(A, lb, ub, weights=np.ones(A.shape[0]), algorithmic_relaxation=2.0)

    x_1 = np.array([1.2, 1.2])
    x_2 = np.array([2.0, 2.0])
    x_3 = np.array([-1.2, -1.2])
    x_4 = np.array([-2.0, -2.0])
    x_5 = np.array([2.0, -2.0])

    x_n = alg.step(x_1)
    assert np.all(np.abs(x_n - np.array([1.1, 1.1])) < 1e-10)

    # check that project gives the same result as step
    x_1 = np.array([1.2, 1.2])
    x_proj = alg.project(x_1)
    assert np.all(np.abs(x_proj - np.array([1.1, 1.1])) < 1e-10)
    assert np.array_equal(x_proj, x_n)

    x_n = alg.step(x_2)
    assert np.all(np.abs(x_n - 1 / 4 * np.array([5, 5])) < 1e-10)

    x_n = alg.step(x_3)
    assert np.all(np.abs(x_n - np.array([-1.1, -1.1])) < 1e-10)

    x_n = alg.step(x_4)
    assert np.all(np.abs(x_n - 1 / 4 * np.array([-5, -5])) < 1e-10)

    x_n = alg.step(x_5)
    assert np.all(np.abs(x_n - 1 / 4 * np.array([5, -5])) < 1e-10)


def test_SimultaneousAMS_relaxation_step(get_sparse_variables):
    """Test the step function with relaxation of the SimultaneousAMS class."""
    A, lb, ub = get_sparse_variables

    alg = SimultaneousAMS(A, lb, ub, weights=np.ones(A.shape[0]), relaxation=2.0)

    x_1 = np.array([1.2, 1.2])
    x_2 = np.array([2.0, 2.0])
    x_3 = np.array([-1.2, -1.2])
    x_4 = np.array([-2.0, -2.0])
    x_5 = np.array([2.0, -2.0])

    x_n = alg.step(x_1)
    assert np.all(np.abs(x_n - np.array([1.1, 1.1])) < 1e-10)

    # check that project gives the same result as step
    x_1 = np.array([1.2, 1.2])
    x_proj = alg.project(x_1)
    assert np.all(np.abs(x_proj - np.array([1.1, 1.1])) < 1e-10)
    assert np.array_equal(x_proj, x_n)

    x_n = alg.step(x_2)
    assert np.all(np.abs(x_n - 1 / 4 * np.array([5, 5])) < 1e-10)

    x_n = alg.step(x_3)
    assert np.all(np.abs(x_n - np.array([-1.1, -1.1])) < 1e-10)

    x_n = alg.step(x_4)
    assert np.all(np.abs(x_n - 1 / 4 * np.array([-5, -5])) < 1e-10)

    x_n = alg.step(x_5)
    assert np.all(np.abs(x_n - 1 / 4 * np.array([5, -5])) < 1e-10)


def test_SimultaneousAMS_proximity(get_full_variables):
    """Test the proximity function of the SimultaneousAMS class."""
    A, lb, ub = get_full_variables
    alg = SimultaneousAMS(A, lb, ub, weights=np.ones(len(A)) / len(A))

    x_1 = np.array([1.2, 1.2])
    x_2 = np.array([2.0, 2.0])
    x_3 = np.array([-1.2, -1.2])
    x_4 = np.array([-2.0, -2.0])
    x_5 = np.array([2.0, -2.0])

    assert np.abs(alg.proximity(x_1) - 0.04) < 1e-10
    assert np.abs(alg.proximity(x_2) - 9 / 8) < 1e-10
    assert np.abs(alg.proximity(x_3) - 0.04) < 1e-10
    assert np.abs(alg.proximity(x_4) - 9 / 8) < 1e-10
    assert np.abs(alg.proximity(x_5) - 9 / 8) < 1e-10
