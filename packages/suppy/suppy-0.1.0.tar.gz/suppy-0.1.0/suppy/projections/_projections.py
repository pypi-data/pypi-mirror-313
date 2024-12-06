from abc import ABC, abstractmethod
import numpy as np
import numpy.typing as npt


class Projection(ABC):
    """
    Abstract base class for projections used in feasibility algorithms.

    Parameters
    ----------
    relaxation : float, optional
        Relaxation parameter for the projection, by default 1.
    proximity_flag : bool
        Flag to indicate whether to take this object into account when calculating proximity, by default True.

    Attributes
    ----------
    relaxation : float
        Relaxation parameter for the projection.
    proximity_flag : bool
        Flag to indicate whether to take this object into account when calculating proximity.
    """

    def __init__(self, relaxation=1, proximity_flag=True, _use_gpu=False):
        self.relaxation = relaxation
        self.proximity_flag = proximity_flag
        self._use_gpu = _use_gpu

    #    @ensure_float_array
    # removed decorator since it leads to unwanted behavior

    def step(self, x: npt.ArrayLike) -> npt.ArrayLike:
        """
        Perform the (possibly relaxed) projection of input array 'x' onto
        the constraint.

        Parameters
        ----------
        x : npt.ArrayLike
            The input array to be projected.

        Returns
        -------
        npt.ArrayLike
            The (possibly relaxed) projection of 'x' onto the constraint.
        """
        return self.project(x)

    def project(self, x: npt.ArrayLike) -> npt.ArrayLike:
        """
        Perform the (possibly relaxed) projection of input array 'x' onto
        the constraint.

        Parameters
        ----------
        x : npt.ArrayLike
            The input array to be projected.

        Returns
        -------
        npt.ArrayLike
            The (possibly relaxed) projection of 'x' onto the constraint.
        """
        if self.relaxation == 1:
            return self._project(x)
        else:
            return x.copy() * (1 - self.relaxation) + self.relaxation * (self._project(x))

    @abstractmethod
    def _project(self, x: npt.ArrayLike) -> npt.ArrayLike:
        """Internal method to project the point x onto the set."""

    def proximity(self, x: npt.ArrayLike) -> float:
        """
        Calculate the proximity of point `x` to the set.

        Parameters
        ----------
        x : npt.ArrayLike
            Input array for which the proximity measure is to be calculated.

        Returns
        -------
        float
            The proximity measure of the input array `x`.
        """
        if self.proximity_flag:
            return self._proximity(x)
        else:
            return 0

    @abstractmethod
    def _proximity(self, x: npt.ArrayLike) -> float:
        """
        Abstract function to calculate the proximity of `x`to the set.
        Needs to be implemented by subclasses.

        Parameters
        ----------
        x : npt.ArrayLike
            The input array.

        Returns
        -------
        float
            The calculated proximity value.
        """


class BasicProjection(Projection, ABC):
    """
    BasicProjection is an abstract base class that extends the Projection
    class.
    It allows for projecting onto a subset of the input array based on provided
    indices.

    Parameters
    ----------
    idx : npt.ArrayLike or None, optional
        Indices to apply the projection, by default None.
    relaxation : float, optional
        Relaxation parameter for the projection, by default 1.
    proximity_flag : bool
        Flag to indicate whether to take this object into account when calculating proximity, by default True.

    Attributes
    ----------
    relaxation : float
        Relaxation parameter for the projection.
    proximity_flag : bool
        Flag to indicate whether to take this object into account when calculating proximity.
    idx : npt.ArrayLike
        Subset of the input vector to apply the projection on.
    """

    def __init__(
        self, relaxation=1, idx: npt.ArrayLike | None = None, proximity_flag=True, _use_gpu=False
    ):
        super().__init__(relaxation, proximity_flag, _use_gpu)
        self.idx = idx if idx is not None else np.s_[:]

    # NOTE: This method should not be required since the base class implementation is sufficient
    # def project(self, x: npt.ArrayLike) -> npt.ArrayLike:
    #     """
    #     Perform the (possibly relaxed) projection of input array 'x' onto the constraint.

    #     Parameters
    #     ----------
    #     x : npt.ArrayLike
    #         The input array to be projected.

    #     Returns
    #     -------
    #     npt.ArrayLike
    #         The (possibly relaxed) projection of 'x' onto the constraint.
    #     """

    #     if self.relaxation == 1:
    #         return self._project(x)
    #     else:
    #         x[self.idx] = x[self.idx] * (1 - self.relaxation) + self.relaxation * (
    #             self._project(x)[self.idx]
    #         )
    #         return x

    def _proximity(self, x: npt.ArrayLike) -> float:
        """
        Calculate the proximity of point `x` to set.

        Parameters
        ----------
        x : npt.ArrayLike
            Input array for which the proximity measure is to be calculated.

        Returns
        -------
        float
            The proximity measure of the input array `x`.
        """

        # probably should have some option to choose the distance
        return ((x - self._project(x.copy())) ** 2).sum()
