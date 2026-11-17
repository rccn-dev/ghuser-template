"""The spec for column_axes: points and a direction in, lines out."""

import pytest

from my_tool import column_axes


def test_one_axis_per_base_starting_at_it():
    lines = column_axes([(0, 0, 0), (6, 0, 0)], height=3.0)
    assert len(lines) == 2
    assert tuple(lines[1].start) == pytest.approx((6.0, 0.0, 0.0))


def test_every_axis_is_as_long_as_the_height_whatever_the_direction_length():
    lines = column_axes([(0, 0, 0), (1, 2, 3)], height=3.5, direction=(0, 0, 10))
    assert all(line.length == pytest.approx(3.5) for line in lines)


def test_axes_go_up_by_default_and_along_the_direction_given():
    assert tuple(column_axes([(0, 0, 0)], 2.0)[0].end) == pytest.approx((0.0, 0.0, 2.0))
    assert tuple(column_axes([(0, 0, 0)], 2.0, direction=(1, 0, 0))[0].end) == pytest.approx((2.0, 0.0, 0.0))


@pytest.mark.parametrize("height, direction", [(0.0, (0, 0, 1)), (-1.0, (0, 0, 1)), (3.0, (0, 0, 0))])
def test_rejects_nonsense_input(height, direction):
    with pytest.raises(ValueError):
        column_axes([(0, 0, 0)], height, direction)
