"""Column axes: points and a direction in, lines out."""

from compas.geometry import Line, Point, Vector


def column_axes(bases, height, direction=(0.0, 0.0, 1.0)):
    """One axis line per column, from its base along direction.

    Parameters
    ----------
    bases : list of (x, y, z)
        Column bases, as points or any sequence of three numbers.
    height : float
        Length of each axis. Positive.
    direction : (x, y, z)
        Which way the columns go; any length but zero.

    Returns
    -------
    list[Line]
    """
    if height <= 0:
        raise ValueError(f"height must be positive, got {height}")
    axis = Vector(*direction)
    if axis.length == 0:
        raise ValueError("direction must not be zero")
    axis = axis.unitized().scaled(height)
    return [Line(Point(*b), Point(*b) + axis) for b in bases]
