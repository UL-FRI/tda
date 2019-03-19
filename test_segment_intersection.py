import pytest
from segment_intersection import intersection, Orientation, orientation


def test_orientation():
    cases = (((0, 0), (1, 0), (0, 1), Orientation.COUNTER_CLOCKWISE),
             ((0, 0), (0, 1), (1, 0), Orientation.CLOCKWISE),
             ((0, 0), (1, 0), (2, 0), Orientation.NONE))
    for test in cases:
        assert orientation(*test[:3]) == test[-1]


def test_intersection():
    cases = (((-1, 1), (1, -1), (1, 1), (-1, -1), (0, 0)),
             ((1, 1), (1, 2), (0, 1), (0, 2), None),
             ((1, 1), (1, 2), (1, 3), (1, 4), None),
             ((1, 1), (1, 3), (1, 3), (1, 4), (1, 3)),
             ((1, 1), (1, 3), (1, 2), (1, 4), ((1, 2), (1, 3))),
             ((1, 1), (1, 4), (1, 2), (1, 4), ((1, 2), (1, 4))),
             ((1, 4), (1, 2), (1, 2), (1, 4), ((1, 2), (1, 4))),
             ((-1, 0), (1, 0), (0, 1), (0, 0), (0, 0)))
    for case in cases:
        assert intersection(*case[:-1]) == case[-1]


def test_intersection_student():
    case = ((1, 0), (0, 0), (1, 1), (0, 0), (0, 0))
    assert intersection(*case[:-1]) == case[-1]
