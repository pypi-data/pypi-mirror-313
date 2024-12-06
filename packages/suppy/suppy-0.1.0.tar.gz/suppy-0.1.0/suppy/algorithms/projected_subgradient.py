# from suppy.utils.func_wrapper import func_wrapper
# from suppy.utils.decorators import ensure_float_array
# from typing import Callable


# class Projected_subgradient:
#     """
#     """
#     def __init__(self,
#                 func:Callable,
#                 grad:Callable, #what if gradient free?
#                 projection:Callable,
#                 func_args = (),
#                 grad_args = ()):

#         self.wrapped_func = func_wrapper(func,func_args)
#         self.wrapped_grad = func_wrapper(grad,grad_args)


#     def step(self,x):
#         """
#         """
#         x_new = x - self.wrapped_grad(x) #TODO: Gradient step size
#         x_new = self.projection.solve(x_new) #need the full projection
#         return x_new

#     def solve(self,x):
#         """
#         """
#         x_new = x
#         for i in range(1000):
#             x_new = self.step(x_new)
#         return x_new
