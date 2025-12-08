class Point:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def __repr__(self):
        return f"Point({self.x:.3f}, {self.y:.3f})"

    def __eq__(self, other):
        return abs(self.x - other.x) < 1e-9 and abs(self.y - other.y) < 1e-9


class Segment:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def __repr__(self):
        return f"Segment({self.p1}, {self.p2})"


def orientation(a, b, c):
    # 1 — против ЧС, -1 — по ЧС, 0 — коллинеарны
    val = (b.y - a.y) * (c.x - b.x) - (b.x - a.x) * (c.y - b.y)
    if abs(val) < 1e-12:
        return 0
    return 1 if val > 0 else -1


def on_segment(a, b, c):
    # лежит ли b между a и c
    return (min(a.x, c.x) - 1e-9 <= b.x <= max(a.x, c.x) + 1e-9 and
            min(a.y, c.y) - 1e-9 <= b.y <= max(a.y, c.y) + 1e-9)


def point_on_segment(p, seg):
    # истина, если точка p лежит на отрезке seg
    if orientation(seg.p1, p, seg.p2) != 0:
        return False
    return on_segment(seg.p1, p, seg.p2)