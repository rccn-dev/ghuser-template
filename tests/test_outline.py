"""The spec for floor_area: a closed outline in, its area and centroid out."""

import pytest

from my_tool import floor_area

SQUARE = [(0, 0, 3), (10, 0, 3), (10, 10, 3), (0, 10, 3), (0, 0, 3)]
L_SHAPE = [(0, 0, 0), (2, 0, 0), (2, 1, 0), (1, 1, 0), (1, 2, 0), (0, 2, 0), (0, 0, 0)]


def test_a_square_has_its_side_squared_and_its_centre():
    area, centroid = floor_area(SQUARE)
    assert area == pytest.approx(100.0)
    assert tuple(centroid) == pytest.approx((5.0, 5.0, 3.0))


def test_the_direction_the_outline_runs_does_not_matter():
    assert floor_area(SQUARE[::-1])[0] == pytest.approx(floor_area(SQUARE)[0])
    assert tuple(floor_area(SQUARE[::-1])[1]) == pytest.approx(tuple(floor_area(SQUARE)[1]))


def test_an_l_shape_is_three_squares_and_leans_to_its_corner():
    area, centroid = floor_area(L_SHAPE)
    assert area == pytest.approx(3.0)
    assert centroid.x == pytest.approx(centroid.y) and centroid.x < 1.0


@pytest.mark.parametrize("outline", [SQUARE[:-1], [(0, 0, 0), (1, 0, 0), (0, 0, 0)], [(0, 0, 0), (1, 0, 0), (2, 0, 0), (0, 0, 0)]],
                         ids=["open", "too few corners", "no area"])
def test_rejects_an_outline_that_is_not_a_floor(outline):
    with pytest.raises(ValueError):
        floor_area(outline)
