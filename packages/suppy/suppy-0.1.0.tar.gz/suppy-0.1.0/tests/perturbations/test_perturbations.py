import pytest
import numpy as np
from suppy.utils import FuncWrapper
from suppy.perturbations import PowerSeriesGradientPerturbation


@pytest.fixture
def get_test_func():
    def func(x, a):
        return a * np.sum(x**2)

    return func


@pytest.fixture
def get_test_grad():
    def grad(x, a):
        return a * 2 * x

    return grad


@pytest.fixture
def get_test_func_args():
    return [2.0]


@pytest.fixture
def get_test_grad_args():
    return [2.0]


@pytest.fixture
def get_test_perturbation(get_test_func, get_test_grad, get_test_func_args, get_test_grad_args):
    return PowerSeriesGradientPerturbation(
        get_test_func, get_test_grad, get_test_func_args, get_test_grad_args
    )


def test_PowerSeriesGradientPerturbation_constructor(get_test_perturbation):
    pert = get_test_perturbation

    # test objective and gradient
    assert isinstance(pert.func, FuncWrapper)
    assert isinstance(pert.grad, FuncWrapper)
    # make sure that they produce the correct results
    assert pert.func(np.array([1, 1])) == 4.0
    assert np.all(pert.grad(np.array([1, 1])) == [4.0, 4.0])

    assert pert.n_red == 1
    assert pert._k == 0
    assert pert._l == -1
    assert pert.step_size == 0.5
    assert pert.n_restart == np.inf


def test_PowerSeriesGradientPerturbation_pre_step(get_test_perturbation):
    pert = get_test_perturbation

    pert.pre_step()

    assert pert._l == -1

    pert._l = 10
    pert._k = 3
    pert.n_restart = 3
    pert.pre_step()
    assert pert._l == 1


def test_PowerSeriesGradientPerturbation_function_reduction_step(get_test_perturbation):
    pert = get_test_perturbation

    x = np.array([1, 1])
    x = pert._function_reduction_step(x)

    assert np.all(x == (1 - 1 / np.sqrt(2) * np.array([1, 1])))
    assert pert._l == 0
    assert pert._k == 0


def test_PowerSeriesGradientPerturbation_single_perturbation_step(
    get_test_perturbation,
):

    pert = get_test_perturbation

    x = np.array([1, 1])
    x = pert.perturbation_step(x)

    assert np.all(x == (1 - 1 / np.sqrt(2) * np.array([1, 1])))
    assert pert._l == 0


def test_PowerSeriesGradientPerturbation_multiple_perturbation_step(
    get_test_perturbation,
):
    pert = get_test_perturbation
    assert pert._l == -1
    pert.n_red = 2
    x = np.array([1, 1])
    x = pert.perturbation_step(x)
    assert np.all(x == (1 - 1 / np.sqrt(2) - 1 / np.sqrt(8)) * np.array([1, 1]))
    assert pert._l == 1
    assert pert._k == 1
