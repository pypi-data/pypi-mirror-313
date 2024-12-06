import numpy as np
import numpy.typing as npt
from suppy.utils import ensure_float_array
from suppy.perturbations import Perturbation
from ._sup import FeasibilityPerturbation

try:
    import cupy as cp
except ImportError:
    cp = np


class Superiorization(FeasibilityPerturbation):
    """
    Superiorization algorithm for constrained optimization problems.

    Parameters
    ----------
    basic : Callable
        The underlying feasibility seeking algorithm.
    perturbation_scheme : Perturbation
        The perturbation scheme to be used for superiorization.
    objective_tol : float, optional
        Tolerance for the objective function value change to determine stopping criteria, by default 1e-4.
    constr_tol : float, optional
        Tolerance for the constraint proximity value change to determine stopping criteria, by default 1e-6.

    Attributes
    ----------
    basic : Callable
        The underlying feasibility seeking algorithm.
    perturbation_scheme : Perturbation
        The perturbation scheme to be used for superiorization.
    objective_tol : float
        Tolerance for the objective function value change to determine stopping criteria.
    constr_tol : float
        Tolerance for the constraint proximity value change to determine stopping criteria.
    f_k : float
        The last value of the objective function.
    p_k : float
        The last value of the constraint function.
    _k : int
        The current iteration number.
    all_x : list | None
        List of all points achieved during the optimization process, only stored if requested by the user.
    all_function_values : list | None
        List of all objective function values achieved during the optimization process, only stored if requested by the user.
    all_x_function_reduction : list | None
        List of all points achieved via the function reduction step, only stored if requested by the user.
    all_function_values_function_reduction : list | None
        List of all objective function values achieved via the function reduction step, only stored if requested by the user.
    all_x_basic : list | None
        List of all points achieved via the basic feasibility seeking algorithm, only stored if requested by the user.
    all_function_values_basic : list | None
        List of all objective function values achieved via the basic feasibility seeking algorithm, only stored if requested by the user.
    """

    def __init__(
        self,
        basic,
        perturbation_scheme: Perturbation,
        objective_tol: float = 1e-4,
        constr_tol: float = 1e-6,
    ):

        super().__init__(basic)
        self.perturbation_scheme = perturbation_scheme
        self.objective_tol = objective_tol
        self.constr_tol = constr_tol

        # initialize some variables for the algorithms
        self.f_k = None
        self.p_k = None
        self._k = 0

        self.all_x = []
        self.all_function_values = []  # array storing all objective function values

        self.all_x_function_reduction = (
            []
        )  # array storing all points achieved via the function reduction step
        self.all_function_values_function_reduction = (
            []
        )  # array storing all objective function values achieved via the function reduction step

        self.all_x_basic = []  # array storing all points achieved via the basic algorithm
        self.all_function_values_basic = (
            []
        )  # array storing all objective function values achieved via the basic algorithm

    @ensure_float_array
    def solve(self, x_0: npt.ArrayLike, max_iter: int = 10, storage=False) -> npt.ArrayLike:
        """
        Solve the optimization problem using the superiorization method.

        Parameters
        ----------
        x_0 : npt.ArrayLike
            Initial guess for the solution.
        max_iter : int, optional
            Maximum number of iterations to perform (default is 10).
        storage : bool, optional
            If True, store intermediate results (default is False).

        Returns
        -------
        npt.ArrayLike
            The optimized solution.
        """

        # initialization of variables
        x = x_0
        self._k = 0  # reset counter if necessary
        stop = False

        # initial function and proximity values
        self.f_k = self.perturbation_scheme.func(x_0)
        self.p_k = self.basic.proximity(x_0)

        if storage:
            self._initial_storage(x_0, self.perturbation_scheme.func(x_0))

        while self._k < max_iter and not stop:
            self.perturbation_scheme.pre_step()
            # check if a restart should be performed

            # perform the perturbation schemes update step
            x = self.perturbation_scheme.perturbation_step(x)

            if storage:
                self._storage_function_reduction(x, self.perturbation_scheme.func(x))
            if self._k % 10 == 0:
                print(f"Current iteration: {self._k}")
            # perform basic step
            x = self.basic.step(x)

            if storage:
                self._storage_basic_step(x, self.perturbation_scheme.func(x))

            self._k += 1

            # check current function and proximity values
            f_temp = self.perturbation_scheme.func(x)
            p_temp = self.basic.proximity(x)

            # enable different stopping criteria for different superiorization algorithms
            stop = self._stopping_criteria(f_temp, p_temp)

            # update function and proximity values
            self.f_k = f_temp
            self.p_k = p_temp

            self._additional_action(x)

        self._post_step(x)

        return x

    def _stopping_criteria(self, f_temp, p_temp) -> bool:
        """
        Determine if the stopping criteria for the optimization process are
        met.

        Parameters
        ----------
        f_temp : float
            The current value of the objective function.
        p_temp : float
            The current value of the constraint function.

        Returns
        -------
        bool
            True if the stopping criteria are met, False otherwise.

        Notes
        -----
        The stopping criteria are based on the absolute differences between the
        current values and the previous values of the objective and constraint
        functions. If both differences are less than their respective tolerances
        (`objective_tol` and `constr_tol`), the criteria are considered met.
        """
        stop = (
            np.abs(f_temp - self.f_k) < self.objective_tol
            and np.abs(p_temp - self.p_k) < self.constr_tol
        )
        return stop

    def _additional_action(self, x):
        """
        Perform an additional action on the input, in case it is needed.

        Parameters
        ----------
        x : any
            The input on which the additional action is performed.

        Returns
        -------
        None
        """
        pass

    def _initial_storage(self, x, f):
        """
        Initializes storage for objective values and appends initial values.

        Parameters
        ----------
        x : array-like
            Initial values of the variables.
        f : array-like
            Initial values of the objective function.
        """
        # reset objective values
        self.all_x = []
        self.all_function_values = []  # array storing all objective function values

        self.all_x_function_reduction = []
        self.all_function_values_function_reduction = []

        self.all_x_basic = []
        self.all_function_values_basic = []

        # append initial values
        self.all_x.append(x)
        self.all_function_values.append(f)

    def _storage_function_reduction(self, x, f):
        """
        Stores the given values of x and f into the corresponding lists.

        Parameters
        ----------
        x : array-like
            The current value of the variable x to be stored.
        f : float
            The current value of the function f to be stored.

        Notes
        -----
        This method appends the given values of x and f to the lists
        `all_x`, `all_function_values`, `all_x_function_reduction`,
        and `all_function_values_function_reduction`.
        """
        self.all_x.append(x.copy())
        self.all_function_values.append(f)
        self.all_x_function_reduction.append(x.copy())
        self.all_function_values_function_reduction.append(f)

    def _storage_basic_step(self, x, f):
        """
        Stores the current values of x and f in the respective lists.

        Parameters
        ----------
        x : array-like
            The current value of the variable x.
        f : float
            The current value of the function f.

        Notes
        -----
        This method appends the current values of x and f to both the basic and
        general lists of x values and function values.
        """
        self.all_x_basic.append(x.copy())
        self.all_function_values_basic.append(f)
        self.all_x.append(x.copy())
        self.all_function_values.append(f)

    def _post_step(self, x: npt.ArrayLike):
        """
        Perform an action after the optimization process has finished.

        Parameters
        ----------
        x : array-like
            The current value of the variable x.

        Returns
        -------
        None
        """
        xp = cp if isinstance(x, cp.ndarray) else np
        self.all_x = xp.array(self.all_x)
        self.all_function_values = xp.array(self.all_function_values)
        self.all_x_function_reduction = xp.array(self.all_x_function_reduction)
        self.all_function_values_function_reduction = xp.array(
            self.all_function_values_function_reduction
        )
        self.all_x_basic = xp.array(self.all_x_basic)
        self.all_function_values_basic = xp.array(self.all_function_values_basic)
