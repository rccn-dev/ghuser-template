"""The spec for area_schedule: groups in, totals, shares and a report out."""

import pytest

from my_tool import area_schedule

FLOORS = [[20.0, 30.0, 50.0], [40.0, 40.0]]


def test_one_total_per_floor():
    totals, _, _ = area_schedule(FLOORS)
    assert totals == pytest.approx([100.0, 80.0])


def test_shares_keep_the_shape_and_add_up_to_one_per_floor():
    _, shares, _ = area_schedule(FLOORS)
    assert [len(s) for s in shares] == [3, 2]
    assert [sum(s) for s in shares] == pytest.approx([1.0, 1.0])
    assert shares[0][2] == pytest.approx(0.5)


def test_an_empty_floor_totals_zero_and_has_no_shares():
    totals, shares, _ = area_schedule([[10.0], []])
    assert totals == pytest.approx([10.0, 0.0]) and shares[1] == []


def test_the_report_has_a_line_per_floor_and_the_total():
    report = area_schedule(FLOORS)[2].splitlines()
    assert len(report) == 3
    assert report[-1] == "Total: 180.0 m2"


def test_rejects_a_room_without_area():
    with pytest.raises(ValueError):
        area_schedule([[10.0, 0.0]])
