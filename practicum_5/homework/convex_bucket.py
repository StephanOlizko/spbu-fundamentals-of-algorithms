from time import perf_counter

import numpy as np
from numpy.typing import NDArray

from src.plotting import plot_points

import math


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance_to(self, other_point):
        dx = self.x - other_point.x
        dy = self.y - other_point.y
        return math.sqrt(dx ** 2 + dy ** 2)

    def is_above(self, line):
        value = line.a * self.x + line.b * self.y + line.c
        return value <= 0

    def __str__(self):
        return f"({self.x}, {self.y})"


class Line:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    @classmethod
    def from_points(cls, point1, point2):
        a = point2.y - point1.y
        b = point1.x - point2.x
        c = -a * point1.x - b * point1.y
        return cls(a, b, c)

    def distance_to(self, point):
        return abs(self.a * point.x + self.b * point.y + self.c) / math.sqrt(self.a ** 2 + self.b ** 2)

    def __str__(self):
        return f"{self.a}x + {self.b}y + {self.c} = 0"


def quickhull_recursion_below(left_point, right_point, points):
    line = Line.from_points(left_point, right_point)
    points_below = [point for point in points if not point.is_above(line)]

    if len(points_below) == 0:
        return [left_point, right_point]

    farthest_point = max(reversed(points_below), key=lambda point: line.distance_to(point))

    print(line, end=" | ")
    for i in points_below:
        print(i, end=" ")
    print(" | ", end="")
    print(farthest_point)

    return quickhull_recursion_below(left_point, farthest_point, points_below) + quickhull_recursion_below(
        farthest_point, right_point, points_below)


def convex_bucket(points: NDArray) -> NDArray:
    """Complexity: O(n log n)"""
    # Используем нижнюю итерацию алгоритма QuickHull
    clockwise_sorted_ch = []

    point_objects = sorted([Point(*point) for point in points], key=lambda point: point.x)

    left_point = point_objects[0]
    right_point = point_objects[-1]

    # Здесь обрабатываются точки с одинаковой координатой y
    for i in point_objects:
        if i.x == left_point.x and i.y > left_point.y:
            left_point = i
        if i.x == right_point.x and i.y > right_point.y:
            right_point = i

    line = Line.from_points(left_point, right_point)

    clockwise_sorted_ch_p = list(set(quickhull_recursion_below(left_point, right_point, point_objects)))

    # Здесь точки распределяются в необходимом порядке по координате y для правильного отображения
    left_column = []
    right_column = []
    for point in clockwise_sorted_ch_p:
        if point.x == left_point.x:
            left_column.append([point.x, point.y])
        elif point.x == right_point.x:
            right_column.append([point.x, point.y])
        else:
            clockwise_sorted_ch.append([point.x, point.y])

    left_column = sorted(left_column, key=lambda point: point[1])
    right_column = sorted(right_column, key=lambda point: point[1], reverse=True)
    clockwise_sorted_ch = sorted(clockwise_sorted_ch, key=lambda point: point[0], reverse=True)

    clockwise_sorted_ch = right_column + clockwise_sorted_ch + left_column

    return np.array(clockwise_sorted_ch)


if __name__ == "__main__":
    for i in range(1, 11):
        txtpath = f"../points_{i}.txt"
        points = np.loadtxt(txtpath)
        print(f"Processing {txtpath}")
        print("-" * 32)
        t_start = perf_counter()
        ch = convex_bucket(points)
        t_end = perf_counter()
        print(f"Elapsed time: {t_end - t_start} sec")
        plot_points(points, convex_hull=ch, markersize=20)
        print()
