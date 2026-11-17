"""Floor area: a closed outline in, its area and centroid out."""

from compas.geometry import Point


def floor_area(outline):
    """Area and centroid of a closed floor outline, measured in plan (x, y).

    Parameters
    ----------
    outline : list of (x, y, z)
        The corners in order, the first repeated at the end: a closed polyline.

    Returns
    -------
    (float, Point)
        The area, and the centroid at the outline's average height.
    """
    points = [tuple(p) for p in outline]
    if len(points) < 4 or points[0] != points[-1]:
        raise ValueError("the outline must be closed: its last corner is its first")
    corners = points[:-1]
    twice_area = cx = cy = 0.0
    for (x0, y0, _), (x1, y1, _) in zip(corners, corners[1:] + corners[:1]):
        cross = x0 * y1 - x1 * y0
        twice_area += cross
        cx += (x0 + x1) * cross
        cy += (y0 + y1) * cross
    if abs(twice_area) < 1e-12:
        raise ValueError("the outline encloses no area in plan")
    z = sum(p[2] for p in corners) / len(corners)
    return abs(twice_area) / 2, Point(cx / (3 * twice_area), cy / (3 * twice_area), z)
