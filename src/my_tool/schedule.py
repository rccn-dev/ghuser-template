"""Area schedule: groups in (one per floor), totals, shares and a report out."""


def area_schedule(floors):
    """Total area per floor, each room's share of its floor, and a text report.

    Parameters
    ----------
    floors : list[list[float]]
        Room areas, one list per floor. Areas are positive; a floor may be empty.

    Returns
    -------
    (list[float], list[list[float]], str)
        totals: one per floor. shares: each room's fraction of its floor, in the
        same shape as floors. report: one line per floor and a total.
    """
    floors = [list(rooms) for rooms in floors]
    if any(a <= 0 for rooms in floors for a in rooms):
        raise ValueError("every room area must be positive")
    totals = [sum(rooms) for rooms in floors]
    shares = [[a / total for a in rooms] for rooms, total in zip(floors, totals)]
    lines = [f"Floor {i + 1}: {len(rooms)} rooms, {total:.1f} m2" for i, (rooms, total) in enumerate(zip(floors, totals))]
    lines.append(f"Total: {sum(totals):.1f} m2")
    return totals, shares, "\n".join(lines)
