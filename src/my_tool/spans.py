"""Span check: a list in, a verdict per item and a summary out."""

from collections import namedtuple

SpanReport = namedtuple("SpanReport", "ok failures worst")


def check_spans(spans, limit):
    """Which spans are within limit, how many are not, and the longest.

    Parameters
    ----------
    spans : list[float]
        Span lengths in metres. Each positive; at least one.
    limit : float
        The longest span allowed. Positive.

    Returns
    -------
    SpanReport
        ok: one bool per span, in order. failures: how many are over the limit.
        worst: the longest span.
    """
    spans = list(spans)
    if not spans:
        raise ValueError("no spans to check")
    if limit <= 0:
        raise ValueError(f"limit must be positive, got {limit}")
    if any(s <= 0 for s in spans):
        raise ValueError("every span must be positive")
    ok = [s <= limit for s in spans]
    return SpanReport(ok, ok.count(False), max(spans))
