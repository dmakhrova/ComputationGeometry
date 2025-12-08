
from geometry import Point, Segment, point_on_segment
from typing import List

def segments_intersect_ray(seg, px, py):
    #Проверка, пересекает ли отрезок seg горизонтальный луч (px, py).
    #Возвращает:
    #  истина  — строгое пересечение,
    #  'on_edge' — точка лежит на этом отрезке
    #  ложь — не пересекает.
    a, b = seg.p1, seg.p2

    # приводим точку в начало координат
    x1, y1 = a.x - px, a.y - py
    x2, y2 = b.x - px, b.y - py

    if (y1 > 0 and y2 > 0) or (y1 < 0 and y2 < 0):
        return False

    if abs(y1) < 1e-12 and abs(y2) < 1e-12:
        if min(x1, x2) <= 0 <= max(x1, x2):
            return 'on_edge'
        return False

    if abs(y1) < 1e-12:
        return y2 > 0
    if abs(y2) < 1e-12:
        return y1 > 0

    t = -y1 / (y2 - y1)
    ix = x1 + t * (x2 - x1)
    return ix > 0


def point_in_polygon(point: Point, polygon: List[Point]) -> str:

   # Проверка положения точки относительно многоугольника.
   # Возвращает: 'inside' (внутри), 'outside' (снаружи), 'boundary' (на границе)
    if len(polygon) < 3:
        return 'outside'

    # Проверка на совпадение с вершиной
    for v in polygon:
        if point == v:
            return 'boundary'

    # Построение рёбер и проверка на принадлежность границе
    n = len(polygon)
    segments = []
    for i in range(n):
        p1 = polygon[i]
        p2 = polygon[(i + 1) % n]
        seg = Segment(p1, p2)
        segments.append(seg)
        if point_on_segment(point, seg):
            return 'boundary'

    # Ray casting: считаем пересечения с лучом
    count = 0
    for seg in segments:
        res = segments_intersect_ray(seg, point.x, point.y)
        if res == 'on_edge':
            return 'boundary'
        if res:
            count += 1

    return 'inside' if count % 2 == 1 else 'outside'