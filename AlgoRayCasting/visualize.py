import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MplPolygon
from geometry import Point
from algorythm import point_in_polygon


def plot_polygon_with_points(polygon, test_points,
                             title= "", ax=None):

    if ax is None:
        fig, ax = plt.subplots(1, 1, figsize=(7, 7))

    # Координаты многоугольника
    xs = [p.x for p in polygon]
    ys = [p.y for p in polygon]

    xs.append(xs[0])
    ys.append(ys[0])

    # Рисуем границу
    ax.plot(xs, ys, 'b-', linewidth=2, label='Граница')
    ax.fill(xs[:-1], ys[:-1], color='lightblue', alpha=0.4, label='Область')

    # Цвета и маркеры
    color_map = {'inside': 'green', 'outside': 'red', 'boundary': 'orange'}
    marker_map = {'inside': 'o', 'outside': 's', 'boundary': '^'}

    for pt in test_points:
        status = point_in_polygon(pt, polygon)
        ax.scatter([pt.x], [pt.y],
                   color=color_map[status], edgecolor='k', s=120,
                   marker=marker_map[status], zorder=5)
        ax.text(pt.x + 0.07, pt.y + 0.07, f"{status[:3]}", fontsize=9)

    ax.set_title(title, fontsize=12)
    ax.grid(True)
    ax.set_aspect('equal', adjustable='box')
    ax.set_xlabel('x')
    ax.set_ylabel('y')

    # Легенда
    handles, labels = ax.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax.legend(by_label.values(), by_label.keys())

    return ax


def demo_visualizations():
    # Пример 1: звезда (невыпуклая)
    star = [
        Point(0, 3), Point(0.8, 0.8), Point(3, 0.8),
        Point(1.3, -0.5), Point(2, -3), Point(0, -1.2),
        Point(-2, -3), Point(-1.3, -0.5), Point(-3, 0.8), Point(-0.8, 0.8)
    ]
    pts1 = [Point(0, 0), Point(1, 1), Point(0, 3), Point(4, 0), Point(1.5, 0.8)]

    # Пример 2: буква "Г"
    gamma = [Point(0,0), Point(4,0), Point(4,1), Point(1,1), Point(1,3), Point(0,3)]
    pts2 = [Point(0.5, 0.5), Point(2, 0.5), Point(0.5, 2), Point(2, 2), Point(1,1)]

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    plot_polygon_with_points(star, pts1, "Невыпуклый (звезда)", axes[0])
    plot_polygon_with_points(gamma, pts2, "Невыпуклый ('Г'-образный)", axes[1])
    plt.tight_layout()
    plt.show()