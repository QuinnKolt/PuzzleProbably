from gameplay.constraints import *
from gameplay.board import Board
from random import random
import json
from os import path as pathos

PREPPED_LEVELS = {}


def preload_level(lev):
    if pathos.exists("levels/level" + str(lev) + ".json"):
        PREPPED_LEVELS[lev] = open_level("levels/level" + str(lev) + ".json")
    else:
        PREPPED_LEVELS[lev] = open_level("levels/hard.json")


def close_level(lev):
    if lev in PREPPED_LEVELS.keys():
        PREPPED_LEVELS.pop(lev)


def get_level(lev):
    if lev in PREPPED_LEVELS.keys():
        return PREPPED_LEVELS[lev]

    if pathos.exists("levels/level" + str(lev) + ".json"):
        return open_level("levels/level" + str(lev) + ".json")

    return open_level("levels/hard.json")


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


class Level:
    def __init__(self, board, levelno, flavortext):
        self.board = board
        self.levelno = levelno
        self.flavortext = flavortext

    def deconstruct(self):
        return LevelBuilder(self.board.vertices, self.board.edges, self.board.cells, self.board.starts,
                            {(type(ca), ca.get_args()) for ca in self.board.constraints}, self.levelno, self.flavortext)


class LevelBuilder:
    def __init__(self, vertices, edges, cells, starts, constraintargs, levelno=-1, flavortext=""):
        self.vertices = vertices
        self.edges = edges
        self.cells = cells
        self.constraintargs = constraintargs
        self.starts = starts
        self.levelno = levelno
        self.flavortext = flavortext

    def board(self):
        return Board(self.vertices, self.edges, self.cells, self.starts,
                     {ca[0](*ca[1]) for ca in self.constraintargs})

    def level(self):
        return Level(self.board(), self.levelno, self.flavortext)

    def to_json(self):
        return json.dumps({"vertices": self.vertices,
                           "edges": self.edges,
                           "cells": self.cells,
                           "starts": self.starts,
                           "constraintargs": [(ca[0].__name__, ca[1]) for ca in self.constraintargs],
                           "levelno": self.levelno,
                           "flavortext": self.flavortext})


def builder_from_json(s):
    d = json.loads(s)
    vertices = tuple((v[0], v[1]) for v in d["vertices"])
    edges = tuple(((e[0][0], e[0][1]), (e[1][0], e[1][1])) for e in d["edges"])
    cells = tuple((c[0], c[1]) for c in d["cells"])
    starts = tuple((v[0], v[1]) for v in d["starts"])
    constraintargs = tuple((eval(cas[0]), cas[1]) for cas in d["constraintargs"])
    levelno = d["levelno"]
    flavortext = d["flavortext"]

    return LevelBuilder(vertices, edges, cells, starts, constraintargs, levelno, flavortext)


def level1():
    domain = basic_domain(3, 3)
    rules = []
    starts = [(1, 1)]

    board = Board(*domain, starts, rules)

    builder = Level(board, 1, "Press enter to complete the level.").deconstruct()
    with open("levels/level1.json", "w") as f:
        f.write(builder.to_json())

    return builder.level()


def level2():
    domain = basic_domain(3, 3)
    rules = [FinishVertex((2, 2),)]
    starts = [(0, 0)]

    board = Board(*domain, starts, rules)

    builder = Level(board, 2, "Be sure to read the constraints.").deconstruct()
    with open("levels/level2.json", "w") as f:
        f.write(builder.to_json())

    return builder.level()


def level3():
    domain = list(basic_domain(3, 3))
    domain[1] = [((0, 0), (0, 1)), ((0, 1), (1, 1)), ((1, 1), (2, 1)),
                 ((2, 1), (2, 2))]
    rules = [FinishVertex((2, 2))]

    starts = [(0, 0)]

    builder = Level(Board(*domain, starts, rules), 3, "There may be edges that cannot be travelled through.").deconstruct()
    with open("levels/level3.json", "w") as f:
        f.write(builder.to_json())

    return builder.level()


def open_level(file_name):
    with open(file_name, "r") as f:
        bst = f.read()
        builder = builder_from_json(bst)
        return builder.level()
