from gameplay.constraints import *
from gameplay.board import Board
from random import random


def get_level(lev):
    if lev == 1:
        return level1()
    if lev == 2:
        return level2()
    if lev == 3:
        return level3()

    return levelhard()


class Level:
    def __init__(self, board, num, hint):
        self.board = board
        self.num = num
        self.hint = hint


def level1():
    domain = basic_domain(3, 3)

    rules = []

    starts = [(1, 1)]

    return Level(Board(*domain, rules, starts), 1, "Press Enter to complete the level.")


def level2():
    domain = basic_domain(3, 3)

    rules = [FinishVertex((2, 2))]

    starts = [(0, 0)]

    return Level(Board(*domain, rules, starts), 2, "Be sure to read the constraints.")


def level3():
    domain = list(basic_domain(3, 3))

    domain[1] = [((0, 0), (0, 1)), ((0, 1), (1, 1)), ((1, 1), (2, 1)),
                 ((2, 1), (2, 2))]

    rules = [FinishVertex((2, 2))]

    starts = [(0, 0)]

    return Level(Board(*domain, rules, starts), 3, "There may be edges that cannot be travelled through.")


def levelhard():
    domain = basic_domain(5, 7)

    rules = [EdgesExactly(32), CellExactlyNVertex((3, 1), 2),
             EdgeExactlyOneVertex((3, 0), (3, 1)), CellExactlyNEdge((1, 4), 3), CellExactlyNEdge((0, 2), 2),
             IncludeVertex((1, 4)), IncludeEdge((2, 3), (2, 4)), IncludeEdge((0, 0), (0, 1)),
             FinishVertex((3, 3)), GroupCell((0, 1), 2), GroupCell((3, 5), 1),
             ColorCell((1, 5)), ColorCell((3, 0), color="steel blue")]

    starts = [(0, 0), (3, 5)]

    return Level(Board(*domain, rules, starts), 99, "Can you solve the last level?")


def basic_domain(n, m):
    vertices = []
    edges = []
    cells = []
    for i in range(n):
        for j in range(m):
            vertices.append((i, j))
            if i != n-1:
                edges.append(((i, j), (i+1, j)))
            if j != m-1:
                edges.append(((i, j), (i, j+1)))
            if i != n-1 and j != m-1:
                cells.append((i, j))

    return vertices, edges, cells


def random_domain_path(n, m, path, likelihood=.9):
    edges = [*path]
    cells = []
    for i in range(n):
        for j in range(m):
            if i != n-1 and j != m-1:
                cells.append((i, j))
            if i != n-1:
                if random() <= likelihood and ((i, j), (i+1, j)) not in path:
                    edges.append(((i, j), (i+1, j)))
            if j != m-1:
                if random() <= likelihood and ((i, j), (i, j+1)) not in path:
                    edges.append(((i, j), (i, j+1)))

    return collect_vertices_from_edges(edges), edges, cells


def collect_vertices_from_edges(edges):
    vertices = set()
    for edge in edges:
        vertices.add(edge[0])
        vertices.add(edge[1])
    return vertices

