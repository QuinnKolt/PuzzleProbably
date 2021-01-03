from rules import *
from solver import Solution


class Board:
    def __init__(self, connections, cells, rules, starts, vertices=None):
        self.cells = cells
        self.connections = connections
        self.rules = rules
        self.starts = starts
        if vertices is not None:
            self.vertices = vertices
        else:
            self.vertices = set()
            for cell in self.cells:
                self.vertices.add(cell)
                self.vertices.add((cell[0]+1, cell[1]))
                self.vertices.add((cell[0], cell[1]+1))
                self.vertices.add((cell[0]+1, cell[1]+1))

    def __contains__(self, item):
        return item in self.connections

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

    def satisfied(self, visited, connections, cur, start):
        for rule in self.rules:
            if not rule.is_satisfied(Solution(visited, connections, cur, start), self):
                return False

        return True

