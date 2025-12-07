import math

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"({self.x:.3f},{self.y:.3f})"

    def __eq__(self, other):
        return abs(self.x - other.x) < 1e-9 and abs(self.y - other.y) < 1e-9

    def __lt__(self, other):
        return (self.x, self.y) < (other.x, other.y)


class Segment:
    _counter = 0  # для стабильного порядка при равных координатах

    def __init__(self, p1, p2, name=None):
        if (p1.x, p1.y) > (p2.x, p2.y):
            p1, p2 = p2, p1
        self.p1 = p1
        self.p2 = p2
        self.name = name or f"S({p1.x:.1f},{p1.y:.1f})-({p2.x:.1f},{p2.y:.1f})"
        self._order_id = Segment._counter
        Segment._counter += 1

    def __repr__(self):
        return f"Segment({self.p1}, {self.p2})"

    def __lt__(self, other):
        # Сначала по левому концу (p1), затем по правому (p2), затем по порядку создания
        if (self.p1.x, self.p1.y) != (other.p1.x, other.p1.y):
            return (self.p1.x, self.p1.y) < (other.p1.x, other.p1.y)
        if (self.p2.x, self.p2.y) != (other.p2.x, other.p2.y):
            return (self.p2.x, self.p2.y) < (other.p2.x, other.p2.y)
        return self._order_id < other._order_id


def cross(o, a, b):
    return (a.x - o.x) * (b.y - o.y) - (a.y - o.y) * (b.x - o.x)


def orientation(a, b, c):
    val = cross(a, b, c)
    if abs(val) < 1e-9:
        return 0
    return 1 if val > 0 else -1


def on_segment(p, q, r):
    return (q.x <= max(p.x, r.x) + 1e-9 and q.x >= min(p.x, r.x) - 1e-9 and
            q.y <= max(p.y, r.y) + 1e-9 and q.y >= min(p.y, r.y) - 1e-9)


def segments_intersect(seg1, seg2):
    p1, q1 = seg1.p1, seg1.p2
    p2, q2 = seg2.p1, seg2.p2

    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)

    if o1 != o2 and o3 != o4:
        return True

    if o1 == 0 and on_segment(p1, p2, q1): return True
    if o2 == 0 and on_segment(p1, q2, q1): return True
    if o3 == 0 and on_segment(p2, p1, q2): return True
    if o4 == 0 and on_segment(p2, q1, q2): return True

    return False


def intersection_point(seg1, seg2):
    x1, y1 = seg1.p1.x, seg1.p1.y
    x2, y2 = seg1.p2.x, seg1.p2.y
    x3, y3 = seg2.p1.x, seg2.p1.y
    x4, y4 = seg2.p2.x, seg2.p2.y

    denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if abs(denom) < 1e-12:
        return None  # параллельны/коллинеарны — не обрабатываем подробно

    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom
    ix = x1 + t * (x2 - x1)
    iy = y1 + t * (y2 - y1)
    return Point(ix, iy)


def seg_y_at_x(seg, x):
    if abs(seg.p2.x - seg.p1.x) < 1e-12:
        return seg.p1.y
    t = (x - seg.p1.x) / (seg.p2.x - seg.p1.x)
    return seg.p1.y + t * (seg.p2.y - seg.p1.y)


def seg_less(seg1, seg2, sweep_x):
    y1 = seg_y_at_x(seg1, sweep_x)
    y2 = seg_y_at_x(seg2, sweep_x)
    if abs(y1 - y2) < 1e-9:
        dy1 = seg1.p2.y - seg1.p1.y
        dx1 = seg1.p2.x - seg1.p1.x
        dy2 = seg2.p2.y - seg2.p1.y
        dx2 = seg2.p2.x - seg2.p1.x
        slope1 = dy1 / dx1 if abs(dx1) > 1e-12 else float('inf')
        slope2 = dy2 / dx2 if abs(dx2) > 1e-12 else float('inf')
        return slope1 < slope2
    return y1 < y2