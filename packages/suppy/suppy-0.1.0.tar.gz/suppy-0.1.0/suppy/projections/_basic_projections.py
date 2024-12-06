import math
import numpy as np
import numpy.typing as npt

import matplotlib.pyplot as plt
from suppy.utils import Bounds
from matplotlib import patches

from suppy.projections._projections import BasicProjection

try:
    import cupy as cp

    no_gpu = False
except ImportError:
    no_gpu = True
    cp = np

# from suppy.utils.decorators import ensure_float_array


# Class for basic projections


class BoxProjection(BasicProjection):
    """
    BoxProjection class for projecting points onto a box defined by lower
    and upper bounds.

    Parameters
    ----------
    lb : npt.ArrayLike
        Lower bounds of the box.
    ub : npt.ArrayLike
        Upper bounds of the box.
    idx : npt.ArrayLike or None
        Subset of the input vector to apply the projection on.
    relaxation : float, optional
        Relaxation parameter for the projection, by default 1.
    proximity_flag : bool
        Flag to indicate whether to take this object into account when calculating proximity, by default True.

    Attributes
    ----------
    lb : npt.ArrayLike
        Lower bounds of the box.
    ub : npt.ArrayLike
        Upper bounds of the box.
    relaxation : float
        Relaxation parameter for the projection.
    proximity_flag : bool
        Flag to indicate whether to take this object into account when calculating proximity.
    idx : npt.ArrayLike
        Subset of the input vector to apply the projection on.
    """

    def __init__(
        self,
        lb: npt.ArrayLike,
        ub: npt.ArrayLike,
        relaxation: float = 1,
        idx: npt.ArrayLike | None = None,
        proximity_flag=True,
        use_gpu=False,
    ):

        super().__init__(relaxation, idx, proximity_flag, use_gpu)
        self.lb = lb
        self.ub = ub

    def _project(self, x: npt.ArrayLike) -> npt.ArrayLike:
        """
        Projects the input array `x` onto the bounds defined by `self.lb`
        and `self.ub`.

        Parameters
        ----------
        x : npt.ArrayLike
            Input array to be projected. Can be a NumPy array or a CuPy array.

        Returns
        -------
        npt.ArrayLike
            The projected array with values clipped to the specified bounds.

        Notes
        -----
        This method modifies the input array `x` in place.
        """
        xp = cp if isinstance(x, cp.ndarray) else np
        x[self.idx] = xp.maximum(self.lb, xp.minimum(self.ub, x[self.idx]))
        return x

    def _proximity(self, x: npt.ArrayLike) -> float:
        """
        Calculate the proximity measure for the given array.

        Parameters
        ----------
        x : npt.ArrayLike
            Input array for which the proximity is to be calculated.

        Returns
        -------
        float
            The calculated proximity measure.
        """
        # probably should have some option to choose the distance
        return 1 / len(x) * ((x - self._project(x.copy())) ** 2).sum()

    def visualize(self, ax: plt.Axes | None = None, color=None):
        """
        Visualize the box if it is 2D on a given matplotlib Axes.

        Parameters
        ----------
        ax : plt.Axes, optional
            The matplotlib Axes to plot on. If None, a new figure and axes are created.
        color : str or None, optional
            The color to fill the box with. If None, the box will be filled with the default color.

        Raises
        ------
        ValueError
            If the box is not 2-dimensional.
        """
        if len(self.lb) != 2:
            raise ValueError("Visualization only possible for 2D boxes")

        if ax is None:
            _, ax = plt.subplots()
        box = patches.Rectangle(
            (self.lb[0], self.lb[1]),
            self.ub[0] - self.lb[0],
            self.ub[1] - self.lb[1],
            linewidth=1,
            edgecolor="black",
            facecolor=color,
            alpha=0.5,
        )
        ax.add_patch(box)

    def get_xy(self):
        """
        Generate the coordinates for the edges of a box if it is 2D.

        This method creates four edges of a 2D box defined by the lower bounds (lb) and upper bounds (ub).
        The edges are generated using 100 points each.

        Returns
        -------
        np.ndarray
            A 2D array of shape (2, 400) containing the concatenated coordinates of the four edges.

        Raises
        ------
        ValueError
            If the box is not 2-dimensional.
        """
        if len(self.lb) != 2:
            raise ValueError("Visualization only possible for 2D boxes")
        edge_1 = np.array([np.linspace(self.lb[0], self.ub[0], 100), np.ones(100) * self.lb[1]])
        edge_2 = np.array([np.ones(100) * self.ub[0], np.linspace(self.lb[1], self.ub[1], 100)])
        edge_3 = np.array([np.linspace(self.lb[0], self.ub[0], 100), np.ones(100) * self.ub[1]])
        edge_4 = np.array([np.ones(100) * self.lb[0], np.linspace(self.lb[1], self.ub[1], 100)])
        return np.concatenate((edge_1, edge_2, edge_3[:, ::-1], edge_4[:, ::-1]), axis=1)


class WeightedBoxProjection(BasicProjection):
    """
    WeightedBoxProjection applies a weighted projection on a box defined by
    lower and upper bounds.
    The idea is a "simultaneous" variant to the "sequential" BoxProjection.

    Parameters
    ----------
    lb : npt.ArrayLike
        Lower bounds of the box.
    ub : npt.ArrayLike
        Upper bounds of the box.
    weights : npt.ArrayLike
        Weights for the projection.
    relaxation : float, optional
        Relaxation parameter, by default 1.
    idx : npt.ArrayLike or None
        Subset of the input vector to apply the projection on.
    proximity_flag : bool, optional
        Flag to indicate if proximity should be calculated, by default True.
    use_gpu : bool, optional
        Flag to indicate if GPU should be used, by default False.

    Attributes
    ----------
    lb : npt.ArrayLike
        Lower bounds of the box.
    ub : npt.ArrayLike
        Upper bounds of the box.
    relaxation : float
        Relaxation parameter for the projection.
    proximity_flag : bool
        Flag to indicate whether to take this object into account when calculating proximity.
    idx : npt.ArrayLike
        Subset of the input vector to apply the projection on.
    """

    def __init__(
        self,
        lb: npt.ArrayLike,
        ub: npt.ArrayLike,
        weights: npt.ArrayLike,
        relaxation: float = 1,
        idx: npt.ArrayLike | None = None,
        proximity_flag=True,
        use_gpu=False,
    ):

        super().__init__(relaxation, idx, proximity_flag, use_gpu)
        self.lb = lb
        self.ub = ub
        self.weights = weights / weights.sum()

    def _project(self, x: npt.ArrayLike) -> npt.ArrayLike:
        """
        Projects the input array `x`.

        Parameters
        ----------
        x : npt.ArrayLike
            The input array to be projected.

        Returns
        -------
        npt.ArrayLike
            The projected array.

        Notes
        -----
        This method modifies the input array `x` in place.
        """
        xp = cp if isinstance(x, cp.ndarray) else np
        x[self.idx] += self.weights * (
            xp.maximum(self.lb, xp.minimum(self.ub, x[self.idx])) - x[self.idx]
        )
        return x

    def _full_project(self, x: npt.ArrayLike) -> npt.ArrayLike:
        """
        Projects the elements of the input array `x` within the specified
        bounds.

        Parameters
        ----------
        x : npt.ArrayLike
            Input array to be projected.

        Returns
        -------
        npt.ArrayLike
            The projected array with elements constrained within the bounds.
        """
        xp = cp if isinstance(x, cp.ndarray) else np
        x[self.idx] = xp.maximum(self.lb, xp.minimum(self.ub, x[self.idx]))

        return x

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
        return (self.weights * ((x[self.idx] - self._full_project(x.copy())[self.idx]) ** 2)).sum()

    def visualize(self, ax: plt.Axes | None = None, color=None):
        """
        Visualize the box if it is 2D on a given matplotlib Axes.

        Parameters
        ----------
        ax : plt.Axes, optional
            The matplotlib Axes to plot on. If None, a new figure and axes are created.
        color : str or None, optional
            The color to fill the box with. If None, the box will be filled with the default color.

        Raises
        ------
        ValueError
            If the box is not 2-dimensional.
        """
        if len(self.lb) != 2:
            raise ValueError("Visualization only possible for 2D boxes")

        if ax is None:
            _, ax = plt.subplots()
        box = patches.Rectangle(
            (self.lb[0], self.lb[1]),
            self.ub[0] - self.lb[0],
            self.ub[1] - self.lb[1],
            linewidth=1,
            edgecolor="black",
            facecolor=color,
            alpha=0.5,
        )
        ax.add_patch(box)

    def get_xy(self):
        """
        Generate the coordinates for the edges of a box if it is 2D.

        This method creates four edges of a 2D box defined by the lower bounds (lb) and upper bounds (ub).
        The edges are generated using 100 points each.

        Returns
        -------
        np.ndarray
            A 2D array of shape (2, 400) containing the concatenated coordinates of the four edges.

        Raises
        ------
        ValueError
            If the box is not 2-dimensional.
        """
        if len(self.lb) != 2:
            raise ValueError("Visualization only possible for 2D boxes")
        edge_1 = np.array([np.linspace(self.lb[0], self.ub[0], 100), np.ones(100) * self.lb[1]])
        edge_2 = np.array([np.ones(100) * self.ub[0], np.linspace(self.lb[1], self.ub[1], 100)])
        edge_3 = np.array([np.linspace(self.lb[0], self.ub[0], 100), np.ones(100) * self.ub[1]])
        edge_4 = np.array([np.ones(100) * self.lb[0], np.linspace(self.lb[1], self.ub[1], 100)])
        return np.concatenate((edge_1, edge_2, edge_3[:, ::-1], edge_4[:, ::-1]), axis=1)


# Projection onto a single halfspace
class HalfspaceProjection(BasicProjection):
    """
    A class used to represent a projection onto a halfspace.

    Parameters
    ----------
    a : npt.ArrayLike
        The normal vector defining the halfspace.
    b : float
        The offset value defining the halfspace.
    relaxation : float, optional
        The relaxation parameter, by default 1.
    idx : npt.ArrayLike or None
        Subset of the input vector to apply the projection on.
    proximity_flag : bool, optional
        Flag to indicate whether to take this object into account when calculating proximity, by default True.
    use_gpu : bool, optional
        Flag to indicate if GPU should be used, by default False.

    Attributes
    ----------
    a : npt.ArrayLike
        The normal vector defining the halfspace.
    a_norm : npt.ArrayLike
        The normalized normal vector.
    b : float
        The offset value defining the halfspace.
    relaxation : float
        The relaxation parameter for the projection.
    proximity_flag : bool
        Flag to indicate whether to take this object into account when calculating proximity.
    idx : npt.ArrayLike
        Subset of the input vector to apply the projection on.
    """

    def __init__(
        self,
        a: npt.ArrayLike,
        b: float,
        relaxation: float = 1,
        idx: npt.ArrayLike | None = None,
        proximity_flag=True,
        use_gpu=False,
    ):

        super().__init__(relaxation, idx, proximity_flag, use_gpu)
        self.a = a
        self.a_norm = self.a / (self.a @ self.a)
        self.b = b

    def _linear_map(self, x):
        return self.a @ x

    def _project(self, x: npt.ArrayLike) -> npt.ArrayLike:
        """
        Projects the input array `x`.

        Parameters
        ----------
        x : npt.ArrayLike
            The input array to be projected.

        Returns
        -------
        npt.ArrayLike
            The projected array.

        Notes
        -----
        This method modifies the input array `x` in place.
        """

        # TODO: dtype check!
        y = self._linear_map(x[self.idx])

        if y > self.b:
            x[self.idx] -= (y - self.b) * self.a_norm

        return x

    def get_xy(self, x: npt.ArrayLike | None = None):
        """
        Generate x and y coordinates for visualization of 2D halfspaces.

        Parameters
        ----------
        x : npt.ArrayLike or None, optional
            The x-coordinates for which to compute the corresponding y-coordinates.
            If None, a default range of x values from -10 to 10 is used.

        Returns
        -------
        np.ndarray
            A 2D array where the first row contains the x-coordinates and the second row contains the corresponding y-coordinates.

        Raises
        ------
        ValueError
            If the halfspace is not 2-dimensional.
        """
        if len(self.a) != 2:
            raise ValueError("Visualization only possible for 2D halfspaces")

        if x is None:
            x = np.linspace(-10, 10, 100)

        if self.a[1] == 0:
            y = np.array([np.ones(100) * self.b, np.linspace(-10, 10, 100)])
        else:
            y = (self.b - self.a[0] * x) / self.a[1]

        return np.array([x, y])

    def visualize(
        self,
        ax: plt.Axes | None = None,
        x: npt.ArrayLike | None = None,
        y_fill: npt.ArrayLike | None = None,
        color=None,
    ):
        """
        Visualize the halfspace if it is 2D on a given matplotlib Axes.

        Parameters
        ----------
        ax : plt.Axes, optional
            The matplotlib Axes to plot on. If None, a new figure and axes are created.
        color : str or None, optional
            The color to fill the box with. If None, the halfspace will be filled with the default color.

        Raises
        ------
        ValueError
            If the halfspace is not 2-dimensional.
        """

        if len(self.a) != 2:
            raise ValueError("Visualization only possible for 2D halfspaces")

        if ax is None:
            _, ax = plt.subplots()

        if x is None:
            x = np.linspace(-10, 10, 100)

        if self.a[1] == 0:
            ax.axvline(x=self.b / self.a[0], label="Halfspace", color=color)
            if np.sign(self.a[0]) == 1:
                ax.fill_betweenx(
                    x,
                    ax.get_xlim()[0],
                    self.b,
                    color=color,
                    label="Halfspace",
                    alpha=0.5,
                )
            else:
                ax.fill_betweenx(
                    x,
                    self.b,
                    ax.get_xlim()[1],
                    color=color,
                    label="Halfspace",
                    alpha=0.5,
                )

        else:
            y = (self.b - self.a[0] * x) / self.a[1]
            ax.plot(x, y, color="xkcd:black")
            if y_fill is None:
                y_fill = np.min(y) if self.a[1] > 0 else np.max(y)

            ax.fill_between(x, y, y_fill, color=color, label="Halfspace", alpha=0.5)


class BandProjection(BasicProjection):
    """
    A class used to represent a projection onto a band.

    Parameters
    ----------
    a : npt.ArrayLike
        The normal vector defining the halfspace.
    lb : float
        The lower bound of the band.
    ub : float
        The upper bound of the band.
    idx : npt.ArrayLike or None
        Subset of the input vector to apply the projection on.
    relaxation : float, optional
        The relaxation parameter, by default 1.
    idx : npt.ArrayLike or None
        Subset of the input vector to apply the projection on.

    Attributes
    ----------
    a : npt.ArrayLike
        The normal vector defining the halfspace.
    a_norm : npt.ArrayLike
        The normalized normal vector.
    lb : float
        The lower bound of the band.
    ub : float
        The upper bound of the band.
    relaxation : float
        The relaxation parameter for the projection.
    proximity_flag : bool
        Flag to indicate whether to take this object into account when calculating proximity.
    idx : npt.ArrayLike
        Subset of the input vector to apply the projection on.
    """

    def __init__(
        self,
        a: npt.ArrayLike,
        lb: float,
        ub: float,
        relaxation: float = 1,
        idx: npt.ArrayLike | None = None,
        proximity_flag=True,
        use_gpu=False,
    ):

        super().__init__(relaxation, idx, proximity_flag, use_gpu)
        self.a = a
        self.a_norm = self.a / (self.a @ self.a)
        self.lb = lb
        self.ub = ub

    def _project(self, x: npt.ArrayLike) -> npt.ArrayLike:
        """
        Projects the input array `x`.

        Parameters
        ----------
        x : npt.ArrayLike
            The input array to be projected.

        Returns
        -------
        npt.ArrayLike
            The projected array.

        Notes
        -----
        This method modifies the input array `x` in place.
        """
        y = self.a @ x[self.idx]

        if y > self.ub:
            x[self.idx] -= (y - self.ub) * self.a_norm
        elif y < self.lb:
            x[self.idx] -= (y - self.lb) * self.a_norm

        return x

    def get_xy(self, x: npt.ArrayLike | None = None):
        """
        Calculate the x and y coordinates for the lower and upper bounds of
        a 2D band.

        Parameters
        ----------
        x : npt.ArrayLike or None, optional
            The x-coordinates at which to evaluate the bounds. If None, a default range
            from -10 to 10 with 100 points is used.

        Returns
        -------
        tuple of np.ndarray
            A tuple containing two numpy arrays:
            - The first array represents the x and y coordinates for the lower bound.
            - The second array represents the x and y coordinates for the upper bound.

        Raises
        ------
        ValueError
            If the band is not 2-dimensional.
        """

        if len(self.a) != 2:
            raise ValueError("Visualization only possible for 2D bands")

        if x is None:
            x = np.linspace(-10, 10, 100)
        if self.a[1] == 0:
            y_lb = np.array([np.ones(100) * self.lb, np.linspace(-10, 10, 100)])
            y_ub = np.array([np.ones(100) * self.ub, np.linspace(-10, 10, 100)])
        else:
            y_lb = (self.lb - self.a[0] * x) / self.a[1]
            y_ub = (self.ub - self.a[0] * x) / self.a[1]
        return np.array([x, y_lb]), np.array([x, y_ub])

    def visualize(self, ax: plt.Axes | None = None, x: npt.ArrayLike | None = None, color=None):
        """
        Visualize the band if it is 2D on a given matplotlib Axes.

        Parameters
        ----------
        ax : plt.Axes, optional
            The matplotlib Axes to plot on. If None, a new figure and axes are created.
        color : str or None, optional
            The color to fill the box with. If None, the band will be filled with the default color.

        Raises
        ------
        ValueError
            If the band is not 2-dimensional.
        """

        if len(self.a) != 2:
            raise ValueError("Visualization only possible for 2D bands")

        if ax is None:
            _, ax = plt.subplots()

        if x is None:
            x = np.linspace(-10, 10, 100)

        if self.a[1] == 0:
            ax.plot(np.ones(100) * self.lb, x, color="xkcd:black")
            ax.plot(np.ones(100) * self.ub, x, color="xkcd:black")
            # ax.axvline(x = self.b/self.a[0],label='Halfspace',color = color)
            if np.sign(self.a[0]) == 1:
                ax.fill_betweenx(x, self.lb, self.ub, color=color, label="Band", alpha=0.5)
            else:
                ax.fill_betweenx(x, self.lb, self.ub, color=color, label="Band", alpha=0.5)
        else:
            y_lb = (self.lb - self.a[0] * x) / self.a[1]
            y_ub = (self.ub - self.a[0] * x) / self.a[1]
            ax.plot(x, y_lb, color="xkcd:black")
            ax.plot(x, y_ub, color="xkcd:black")
            ax.fill_between(x, y_lb, y_ub, color=color, label="Band", alpha=0.5)


class BallProjection(BasicProjection):
    """
    A class used to represent a projection onto a ball.

    Parameters
    ----------
    center : npt.ArrayLike
        The center of the ball.
    radius : float
        The radius of the ball.
    relaxation : float, optional
        The relaxation parameter (default is 1).
    idx : npt.ArrayLike or None
        Subset of the input vector to apply the projection on.
    proximity_flag : bool, optional
        Flag to indicate whether to take this object into account when calculating proximity, by default True.
    use_gpu : bool, optional
        Flag to indicate if GPU should be used, by default False.

    Attributes
    ----------
    center : npt.ArrayLike
        The center of the ball.
    radius : float
        The radius of the ball.
    relaxation : float
        The relaxation parameter for the projection.
    proximity_flag : bool
        Flag to indicate whether to take this object into account when calculating proximity.
    idx : npt.ArrayLike
        Subset of the input vector to apply the projection on.
    """

    def __init__(
        self,
        center: npt.ArrayLike,
        radius: float,
        relaxation: float = 1,
        idx: npt.ArrayLike | None = None,
        proximity_flag=True,
        use_gpu=False,
    ):

        super().__init__(relaxation, idx, proximity_flag, use_gpu)
        self.center = center
        self.radius = radius

    def _project(self, x: npt.ArrayLike) -> npt.ArrayLike:
        """
        Projects the input array `x` onto the surface of the ball.

        Parameters
        ----------
        x : npt.ArrayLike
            The input array to be projected.

        Returns
        -------
        npt.ArrayLike
            The projected array.
        """

        if np.linalg.norm(x[self.idx] - self.center) > self.radius:
            x[self.idx] -= (x[self.idx] - self.center) * (
                1 - self.radius / np.linalg.norm(x[self.idx] - self.center)
            )

        return x

    def visualize(self, ax: plt.Axes | None = None, color=None, edgecolor=None):
        """
        Visualize the halfspace if it is 2D on a given matplotlib Axes.

        Parameters
        ----------
        ax : plt.Axes, optional
            The matplotlib Axes to plot on. If None, a new figure and axes are created.
        color : str or None, optional
            The color to fill the box with. If None, the halfspace will be filled with the default color.

        Raises
        ------
        ValueError
            If the halfspace is not 2-dimensional.
        """

        if len(self.center) != 2:
            raise ValueError("Visualization only possible for 2D balls")

        if ax is None:
            _, ax = plt.subplots()

        circle = plt.Circle(
            (self.center[0], self.center[1]),
            self.radius,
            facecolor=color,
            alpha=0.5,
            edgecolor=edgecolor,
        )
        ax.add_artist(circle)

    def get_xy(self):
        """
        Generate x and y coordinates for a 2D ball visualization.

        Returns
        -------
        np.ndarray
            A 2x50 array where the first row contains the x coordinates and the
            second row contains the y coordinates of the points on the circumference
            of the 2D ball.

        Raises
        ------
        ValueError
            If the center does not have exactly 2 dimensions.
        """
        if len(self.center) != 2:
            raise ValueError("Visualization only possible for 2D balls")

        theta = np.linspace(0, 2 * np.pi, 50)
        x = self.center[0] + self.radius * np.cos(theta)
        y = self.center[1] + self.radius * np.sin(theta)
        return np.array([x, y])


class DVHProjection(BasicProjection):
    """
    Class for dose-volume histogram projections.

    Parameters
    ----------
    d_max : float
        The maximum dose value.
    max_percentage : float
        The maximum percentage of elements allowed to exceed d_max.
    idx : npt.ArrayLike or None
        Subset of the input vector to apply the projection on.

    Attributes
    ----------
    d_max : float
        The maximum dose value.
    max_percentage : float
        The maximum percentage of elements allowed to exceed d_max.
    """

    def __init__(
        self,
        d_max: float,
        max_percentage: float,
        idx: npt.ArrayLike | None = None,
        proximity_flag=True,
        use_gpu=False,
    ):
        super().__init__(1, idx, proximity_flag, use_gpu)

        # max percentage of elements that are allowed to exceed d_max
        self.max_percentage = max_percentage
        self.d_max = d_max

    def _project(self, x: npt.ArrayLike) -> npt.ArrayLike:
        """
        Projects the input array `x` onto the DVH constraint.

        Parameters
        ----------
        x : npt.ArrayLike
            The input array to be projected.

        Returns
        -------
        npt.ArrayLike
            The projected array.

        Notes
        -----
        - The method calculates the number of elements that should receive a dose lower than `d_max` based on `max_percentage`.
        - It then determines how many elements in the input array exceed `d_max`.
        - If the number of elements exceeding `d_max` is greater than the allowed maximum, it reduces the highest values to `d_max`.
        """
        # percentage of elements that should receive a dose lower than d_max
        n = len(x) if isinstance(self.idx, slice) else self.idx.sum()
        am = math.floor(self.max_percentage * n)

        # number of elements in structure with dose greater than d_max
        l = (x[self.idx] > self.d_max).sum()

        z = l - am  # number of elements that need to be reduced

        if z > 0:
            x[x[self.idx].argsort()[n - l : n - am]] = self.d_max

        return x

    def _proximity(self, x: npt.ArrayLike) -> float:
        """
        Calculate the proximity of the given array to a specified maximum
        percentage.

        Parameters
        ----------
        x : npt.ArrayLike
            Input array to be evaluated.

        Returns
        -------
        float
            The proximity value as a percentage.
        """
        n = len(x) if isinstance(self.idx, slice) else self.idx.sum()
        return abs((1 / n * (x[self.idx] > self.d_max).sum()) - self.max_percentage) * 100

    # def _project_argpartition(self, x: npt.ArrayLike) -> npt.ArrayLike:
    # print(WARNING: This function is not working properly!)
    #         # percentage of elements that should receive a dose lower than d_max
    # n = self.idx.sum()
    # am = math.floor(self.max_percentage * n)

    # # number of elements in structure with dose greater than d_max
    # l = (x[self.idx] > self.d_max).sum()

    # z = l - am  # number of elements that need to be reduced

    # if z > 0:
    #     x[x.argpartition(-z)[-z:]] = self.d_max

    # return x
