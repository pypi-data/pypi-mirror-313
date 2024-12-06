.. _projections_api:

suppy.projections
=========================

This module implements a framework for general projection methods.

Underlying classes
------------------

.. autoclass:: suppy.projections._projections.Projection
   :members:
   :undoc-members:
   :show-inheritance:

BasicProjection
---------------
Classes derived from the BASICPROJECTION class. They represent the projection onto a single constraint.

.. autoclass:: suppy.projections._projections.BasicProjection
   :members:
   :undoc-members:
   :show-inheritance:

Projection methods
------------------

Methods to project onto the intersection of a constraint set.

Base class for all projection methods:

.. autoclass:: suppy.projections._projection_methods.ProjectionMethod
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: suppy.projections.SequentialProjection
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: suppy.projections.SimultaneousProjection
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: suppy.projections.StringAveragedProjection
   :members:
   :undoc-members:
   :inherited-members:
   :show-inheritance:

.. autoclass:: suppy.projections.BlockIterativeProjection
   :members:
   :undoc-members:
   :show-inheritance:
