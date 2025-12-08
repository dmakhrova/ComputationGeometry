from geometry import Point
from algorythm import point_in_polygon
from visualize import demo_visualizations

def example_usage():

    # 1. Простой невыпуклый многоугольник (буква L)
    poly = [
        Point(0, 0), Point(4, 0), Point(4, 1),
        Point(1, 1), Point(1, 3), Point(0, 3)
    ]

    tests = [
        Point(0.5, 0.5),  # внутри
        Point(2, 0.5),    # внутри "ножки"
        Point(0.5, 2),    # внутри "стойки"
        Point(2, 2),      # снаружи
        Point(1, 1),      # на углу (граница)
        Point(4, 0),      # вершина (граница)
        Point(2.5, 0),    # на нижнем ребре (граница)
    ]

    for pt in tests:
        res = point_in_polygon(pt, poly)
        print(f"Точка {pt} - {res}")


if __name__ == "__main__":
    example_usage()
    demo_visualizations()