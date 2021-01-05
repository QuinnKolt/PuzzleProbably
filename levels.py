from rules import *
from main import WID, HEI
from board import Board


def levelhard():
    domain = basic_domain(WID, HEI)

    rules = [EdgesExactlyRule(32), CellExactlyNVertex((3, 1), 2),
             EdgeExactlyOneVertex((3, 0), (3, 1)), CellExactlyNEdge((1, 4), 3), CellExactlyNEdge((0, 2), 2),
             IncludeVertex((1, 4)), IncludeEdge((2, 3), (2, 4)), IncludeEdge((0, 0), (0, 1)),
             FinishVertex((3, 3)), GroupCell((0, 1), 2), GroupCell((3, 5), 1),
             ColorCell((1, 5)), ColorCell((3, 0), color="steel blue")]

    return Board(*domain, rules, [(0, 0), (3, 5)])


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
