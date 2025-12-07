from heapq import heappush, heappop
from geometry import segments_intersect, intersection_point, seg_less


def bentley_ottmann(segments):
    #каждому сегменту отрезка присваиваем id
    for i, seg in enumerate(segments):
        seg.id = i

    # очередь событий: (x, y, тип, данные)
    events = []
    for seg in segments:
        heappush(events, (seg.p1.x, seg.p1.y, 'left', seg))
        heappush(events, (seg.p2.x, seg.p2.y, 'right', seg))

    active = []  # список активных отрезков, упорядочен по y в sweep_x)
    intersections = []
    processed = set()  # (min_id, max_id, round(x,9), round(y,9))

    while events:
        x, y, etype, data = heappop(events)
        sweep_x = x

        if etype == 'left':
            seg = data
            # Вставка в active
            i = 0
            while i < len(active) and seg_less(active[i], seg, sweep_x):
                i += 1
            active.insert(i, seg)

            # Проверка с соседями
            for nb in [active[i-1] if i > 0 else None,
                       active[i+1] if i < len(active)-1 else None]:
                if nb is None:
                    continue
                if segments_intersect(seg, nb):
                    pt = intersection_point(seg, nb)
                    if pt is None:
                        continue
                    key = (min(seg.id, nb.id), max(seg.id, nb.id),
                           round(pt.x, 9), round(pt.y, 9))
                    if key not in processed:
                        processed.add(key)
                        intersections.append((seg, nb, pt))
                        if pt.x >= sweep_x - 1e-9:
                            heappush(events, (pt.x, pt.y, 'cross', (seg, nb, pt)))

        elif etype == 'right':
            seg = data
            if seg in active:
                i = active.index(seg)
                above = active[i-1] if i > 0 else None
                below = active[i+1] if i < len(active)-1 else None
                active.pop(i)
                if above and below:
                    if segments_intersect(above, below):
                        pt = intersection_point(above, below)
                        if pt and pt.x >= sweep_x - 1e-9:
                            key = (min(above.id, below.id), max(above.id, below.id),
                                   round(pt.x, 9), round(pt.y, 9))
                            if key not in processed:
                                processed.add(key)
                                intersections.append((above, below, pt))
                                heappush(events, (pt.x, pt.y, 'cross', (above, below, pt)))

        elif etype == 'cross':
            seg1, seg2, pt = data
            if seg1 in active and seg2 in active:
                i1 = active.index(seg1)
                i2 = active.index(seg2)
                if abs(i1 - i2) == 1:
                    # Меняем местами
                    active[i1], active[i2] = active[i2], active[i1]
                    # Проверяем новых соседей
                    for seg, idx in [(seg1, i2), (seg2, i1)]:
                        for nb in [active[idx-1] if idx > 0 else None,
                                   active[idx+1] if idx < len(active)-1 else None]:
                            if nb is None or nb in (seg1, seg2):
                                continue
                            if segments_intersect(seg, nb):
                                ipt = intersection_point(seg, nb)
                                if ipt and ipt.x >= sweep_x - 1e-9:
                                    key = (min(seg.id, nb.id), max(seg.id, nb.id),
                                           round(ipt.x, 9), round(ipt.y, 9))
                                    if key not in processed:
                                        processed.add(key)
                                        intersections.append((seg, nb, ipt))
                                        heappush(events, (ipt.x, ipt.y, 'cross', (seg, nb, ipt)))

    return intersections