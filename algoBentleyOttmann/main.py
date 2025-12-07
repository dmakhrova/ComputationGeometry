from geometry import Point, Segment
from algorithm import bentley_ottmann

import matplotlib.pyplot as plt


def plot_result(segments, intersections, title="Пересечения отрезков"):
    plt.figure(figsize=(8, 8))
    colors = plt.cm.tab10.colors

    for i, seg in enumerate(segments):
        plt.plot([seg.p1.x, seg.p2.x], [seg.p1.y, seg.p2.y],
                 color=colors[i % len(colors)],
                 marker='o', linewidth=2,
                 label=getattr(seg, 'name', f'S{i}'))

    if intersections:
        xs = [pt.x for _, _, pt in intersections]
        ys = [pt.y for _, _, pt in intersections]
        plt.scatter(xs, ys, color='red', s=80, zorder=5,
                    edgecolors='black', label='Пересечения')

    plt.grid(True, linestyle='--', alpha=0.7)
    plt.axis('equal')
    plt.legend()
    plt.title(title)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":

    # примеры отрезков
    segments = [
        Segment(Point(0, 0), Point(4, 4), "A"),
        Segment(Point(0, 5), Point(4, 0), "B"),
        Segment(Point(1, 0), Point(1, 4), "C"),
        Segment(Point(0, 2), Point(4, 2), "D"),
    ]

    print("Отрезки:")
    for s in segments:
        print(f"  {s}")

    # запуск алгоритма
    intersections = bentley_ottmann(segments)

    print(f"\nНайдено {len(intersections)} пересечений:")
    for i, (s1, s2, pt) in enumerate(intersections, 1):
        name1 = getattr(s1, 'name', 'Seg?')
        name2 = getattr(s2, 'name', 'Seg?')
        print(f"{i:2}. {name1} × {name2} = {pt}")

    # построение графика (отрезки + пересечения)
    plot_result(segments, intersections)