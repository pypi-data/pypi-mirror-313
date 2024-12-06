from typing import Callable


class FuncWrapper:
    """
    A callable class for a function that keeps track of the number of times
    it is called.

    Parameters
    ----------
    func : Callable
        The function to be wrapped.
    args : list
        The arguments to be passed to the function.

    Attributes
    ----------
    func : Callable
        The function to be wrapped.
    args : list
        The arguments to be passed to the function.
    fcount : int
        The number of times the function has been called.
    """

    def __init__(self, func: Callable, args=[]):
        self.func = func
        self.args = args
        self.fcount = 0

    def __call__(self, x):
        self.fcount += 1
        return self.func(x, *self.args)
