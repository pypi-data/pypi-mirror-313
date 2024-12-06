.. _projections:

Projections
===========
For the api guide see :ref:`projections_api`.

The ``suppy.projections`` module contains simple structures for projection operations as well as projection methods for projecting onto intersections.
This guide covers the basic projection objects for the projection methods see :ref:`projection_methods`.

As of now there are 5 elemental projection objects. Each one can be set up with a relaxation parameter and a flag to indicate whether to use the GPU for calculations.
Furthermore indices can be set if the vector `x` to be projected and the constraint are not of the same dimension.
The elemental projections are:

.. _projections_BoxProjection:

BoxProjection
-------------

Projection onto box constraints of type :math:`\mathbf{a} \leq \mathbf{x} \leq \mathbf{b}`.
Mathematically the projection is computed as :math:`\mathbf{P}(\mathbf{x}) = \min(\max(\mathbf{x}, \mathbf{a}), \mathbf{b})`.
Setup of ``BoxProjection`` objects is as follows:

.. code-block:: python

    import numpy as np
    from suppy.projections import BoxProjection
    a = np.array([0, 0])
    b = np.array([1, 1])
    projection = BoxProjection(a, b)

where :math:`\mathbf{a}` and :math:`\mathbf{b}` are the lower and upper bounds of the constraint.


WeightedBoxProjection
---------------------

A "simultaneous" projection onto a box of type :math:`\mathbf{a} \leq \mathbf{x} \leq \mathbf{b}`.
The idea is an analogon to the "sequential" projection in :ref:`projections_BoxProjection`.

.. code-block:: python

    import numpy as np
    from suppy.projections import WeightedBoxProjection
    a = np.array([0, 0])
    b = np.array([1, 1])
    w = np.array([1/3,2/3])
    projection = WeightedBoxProjection(a, b, w)

where :math:`\mathbf{a}` and :math:`\mathbf{b}` are the lower and upper bounds of the constraint and :math:`\mathbf{w}` are the weights assigned to the individual bounds.


HalfspaceProjection
-------------------

Projection onto halfspaces of type :math:`\langle \mathbf{a},\mathbf{x} \rangle \leq \mathbf{b}`.

.. code-block:: python

    import numpy as np
    from suppy.projections import HalfspaceProjection
    a = np.array([1, 1])
    b = 1
    projection = HalfspaceProjection(a, b)

where :math:`\mathbf{a}` is the normal vector of the halfspace and :math:`\mathbf{b}` is the offset.
Mathematically the performed calculation for the unrelaxed projection is

.. math::

    P(\mathbf{x}) =
    \begin{cases}
        \mathbf{x} - \frac{\langle \mathbf{a},\mathbf{x} \rangle - \mathbf{ub}}{||\mathbf{a}||^2} \mathbf{a} & \text{if } \langle \mathbf{a},\mathbf{x} \rangle \geq \mathbf{b} \\
        \mathbf{x} & \text{otherwise}.\\
    \end{cases}

BandProjection
--------------

Projection onto a band/hyperslab of type :math:`\langle \mathbf{lb},\mathbf{x} \rangle \leq \mathbf{ub}`.

.. code-block:: python

    import numpy as np
    from suppy.projections import BandProjection
    a = np.array([1, 1])
    lb = np.array([0, 0])
    ub = np.array([1, 1])
    projection = BandProjection(a, lb, ub)

where :math:`\mathbf{lb}` and :math:`\mathbf{ub}` are the lower and upper bounds of the band/hyperslab and :math:`\mathbf{a}` is the normal vector.
The projection is calculated as

.. math::

   P_{C_i}(\mathbf{x}) =
   \begin{cases}
   \mathbf{x} - \frac{\langle \mathbf{a},\mathbf{x} \rangle - \mathbf{ub}}{||\mathbf{a}||^2} \mathbf{a} & \text{if } \langle a,x \rangle \geq ub \\
   \mathbf{x}\\
   \mathbf{x} - \frac{\langle \mathbf{a},\mathbf{x} \rangle - \mathbf{lb}}{||\mathbf{a}||^2} \mathbf{a} & \text{if } \langle a,x \rangle \geq lb \\
   \end{cases}


BallProjection
--------------

Projection onto a ball.

.. code-block:: python

    import numpy as np
    from suppy.projections import BallProjection
    c = np.array([0, 0])
    r = 1
    projection = BallProjection(c, r)

where :math:`\mathbf{c}` is the center of the ball and :math:`r` is the radius.
Mathematically this is calculated as:

.. math::

    P(\mathbf{x}) =
    \begin{cases}
        \mathbf{c} + r \frac{\mathbf{x} - \mathbf{c}}{||\mathbf{x} - \mathbf{c}||} & \text{if } ||\mathbf{x} - \mathbf{c}|| > r \\
        \mathbf{x} & \text{otherwise}.\\
    \end{cases}





.. _subgradient_projections:

Subgradient projections
=======================

If a constraint can be formulated as a convex continous function and its subgradient exist, a projection can be performed in the following way:

.. code-block:: python

    import numpy as np
    from suppy.projections import SubgradientProjection

    def f(x):
        return np.linalg.norm(x)

    def subgrad_f(x):
        return x / np.linalg.norm(x)

    projection = SubgradientProjection(f, subgrad_f,level = 5)
    x = np.array([1, 1])
    projection.project(x)

where `f` is the function, `subgrad_f` its subgradient and `level` the level :math:`\alpha` giving :math:`f(x) \leq \alpha`.
The projection is calculated as:

.. math::

    P(\mathbf{x}) =
    \begin{cases}
    \mathbf{x} - \frac{(f(\mathbf{x})-\alpha)_+}{||\nabla f(\mathbf{x})||^2} \nabla f(\mathbf{x}) & \text{if } f(\mathbf{x}) > \alpha \\
    \mathbf{x} & \text{otherwise}.\\
    \end{cases}
