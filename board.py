from rules.area_rules import *
from rules.cell_rules import *
from rules.edge_rules import *
from rules.vertex_rules import *
from rules.text_rules import *
from random import random


class Board:
    def __init__(self, vertices, edges, cells, rules, starts):
        self.cells = cells
        self.edges = edges
        self.rules = rules
        self.starts = starts
        if vertices is not None:
            self.vertices = vertices
        else:
            self.vertices = set()
            for edge in self.edges:
                self.vertices.add(edge[0])
                self.vertices.add(edge[1])

    def cell_rule_at(self, pos):
        for obj in self.rules:
            if isinstance(obj, CellRule) and obj.pos == pos:
                return obj
        return None

    def vertex_rule_at(self, pos):
        for obj in self.rules:
            if isinstance(obj, VertexRule) and obj.pos == pos:
                return obj
        return None

    def edge_rule_at(self, p, q):
        for obj in self.rules:
            if isinstance(obj, EdgeRule) and (obj.p == p and obj.q == q) or (obj.p == q and obj.q == p):
                return obj
        return None

    def is_satisfied(self, path):
        for rule in self.rules:
            if not rule.is_satisfied(self, path):
                return False

        return True

    def partition_rules(self, types=(VertexRule, EdgeRule, CellRule, TextRule)):
        return {cl: [rule for rule in self.rules if isinstance(rule, cl)] for cl in types}

    def draw(self, state):
        for cell in self.cells:
            state.create_rectangle((cell[0] + 0.5)*state.app.cell_size, (cell[1] + 0.5)*state.app.cell_size,
                                   (cell[0] + 1.5)*state.app.cell_size, (cell[1] + 1.5)*state.app.cell_size,
                                   fill="gray93", outline="light grey", dash=(4, 4), width=2)
        for segment in self.edges:
            state.create_line((segment[0][0] + 0.5)*state.app.cell_size, (segment[0][1] + 0.5)*state.app.cell_size,
                              (segment[1][0] + 0.5)*state.app.cell_size, (segment[1][1] + 0.5)*state.app.cell_size,
                              fill="gainsboro", width=5)
        for s in self.starts:
            state.create_oval((s[0] + 0.5)*64 - 5, (s[1] + 0.5)*64 - 5,
                              (s[0] + 0.5)*64 + 5, (s[1] + 0.5)*64 + 5,
                              fill="white", outline="black")

        for rule in self.rules:
            rule.draw(state)


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


def collect_vertices_from_edges(edges):
    vertices = set()
    for edge in edges:
        vertices.add(edge[0])
        vertices.add(edge[1])
    return vertices


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

class Path:
    def __init__(self, connections, visited=None, cur=None, start=None):
        self.visited = visited
        self.connections = connections
        self.cur = cur
        self.start = start