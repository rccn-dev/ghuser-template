"""The spec for check_spans: a list in, a verdict per item and a summary out."""

import pytest

from my_tool import check_spans


def test_one_verdict_per_span_in_order():
    assert check_spans([4.0, 9.0, 6.0], limit=7.5).ok == [True, False, True]


def test_a_span_exactly_at_the_limit_passes():
    assert check_spans([7.5], limit=7.5).ok == [True]


def test_failures_count_the_spans_over_the_limit():
    assert check_spans([8.0, 9.0, 6.0], limit=7.5).failures == 2


def test_worst_is_the_longest_span():
    assert check_spans([4.0, 9.5, 6.0], limit=12.0).worst == pytest.approx(9.5)


@pytest.mark.parametrize("spans, limit", [([], 7.5), ([4.0], 0.0), ([4.0, -1.0], 7.5)])
def test_rejects_nonsense_input(spans, limit):
    with pytest.raises(ValueError):
        check_spans(spans, limit)
