import enum
from numpy import array, cross, sign, column_stack
from numpy.linalg import solve
from operator import mul
from typing import Tuple, Union


class Orientation(enum.IntEnum):
    """
    Enum representing orientation.
    """
    COUNTER_CLOCKWISE = 1
    CLOCKWISE = -1
    NONE = 0


Point2D = Tuple[float, float]
Segment = Tuple[Point2D, Point2D]


def orientation(A: Point2D, B: Point2D, C: Point2D) -> Orientation:
    """
    Given three points in a plane compute their orientation. The method makes
    use of numpy sign and cross functions.

    Returns:
        1 when points are oriented counter-clockwise, -1 when they are
        oriented clockwise and 0 when they are colinear.
    """
    vectors = (array(p) - A for p in (B, C))
    return Orientation(sign(cross(*vectors)))


def intersection(
            A: Point2D, B: Point2D,
            C: Point2D, D: Point2D
        ) -> Union[Point2D, Segment, None]:
    # Do points intersect at all?
    points = [array(p) for p in (A, B, C, D)]
    to_check = ((A, B, C), (A, B, D), (C, D, A), (C, D, B))
    orientations = [orientation(*e) for e in to_check]
    tests = (mul(*orientations[:2]), mul(*orientations[2:]))
    if all([e == -1 for e in tests]):
        # Intersection is a single point inside line segments
        s1, s2 = points[1] - points[0], points[3] - points[2]
        k, l = solve(column_stack((s1, -s2)), points[2] - points[0])
        assert (points[0] + k*s1 == points[2] + l*s2).all()
        return tuple(points[0] + k*s1)  # type: ignore
    elif any([e == 1 for e in tests]):
        # No intersection
        return None
    elif all([e == 0 for e in orientations]):
        ordered_points = sorted((A, B, C, D))  # Order first by x, then by y
        ss = ((A, B), (C, D))
        # the first and the third ordered point must belong to the
        # same segment in order to have an intersection
        if any((all([p in s for p in ordered_points[0::2]]) for s in ss)):
            p1, p2 = ordered_points[1:3]
            return p1 if p1 == p2 else (p1, p2)
        else:
            return None
    elif any([e == 0 for e in orientations]):
        # Touching in one point, must necessary
        # be endpoint of one of the segments.
        i = orientations.index(Orientation.NONE)
        return to_check[i][2]
    raise Exception("This line should not be reached")
