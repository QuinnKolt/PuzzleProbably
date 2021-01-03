from math import *



class GameRule:
    def __init__(self):
        self.shapes = []

    def is_satisfied(self, solution, board):
        return True

    def error(self, board):
        for shape in self.shapes:
            board.itemconfig(shape, fill="red")

    def success(self, board):
        for shape in self.shapes:
            board.itemconfig(shape, fill="green")

    def normal(self, board):
        for shape in self.shapes:
            board.itemconfig(shape, fill="black")

    def draw(self, board):
        pass


class VertexRule(GameRule):
    def __init__(self, pos):
        super().__init__()
        self.pos = pos


class CellRule(GameRule):
    def __init__(self, pos):
        super().__init__()
        self.pos = pos


class EdgeRule(GameRule):
    def __init__(self, p, q):
        super().__init__()
        self.p = p
        self.q = q


class TextRule(GameRule):
    def __init__(self, text, rule):
        super().__init__()
        self.text = text
        self.rule = rule

    def is_satisfied(self, solution, board):
        return self.rule(solution, board)


def EdgesLessThanRule(n):
    return TextRule("Complete the board in less than " + str(n) + " connections",
                    lambda solution, board: len(solution.connections) < n)


def EdgesGreaterThanRule(n):
    return TextRule("Complete the board in more than " + str(n) + " connections",
                    lambda solution, board: len(solution.connections) > n)


def EdgesExactlyRule(n):
    return TextRule("Complete the board in exactly " + str(n) + " connections",
                    lambda solution, board: len(solution.connections) == n)


# TODO: Make this more general
def EveryVertexRule():
    return TextRule("Visit every vertex on the board",
                    lambda solution, board: len(solution.visited) == len(board.vertices))


class IncludeVertex(VertexRule):
    def __init__(self, pos):
        super().__init__(pos)

    def draw(self, board):
        self.shapes = [board.create_oval(
            (self.pos[0] + 7/16)*board.cell_size, (self.pos[1] + 7/16)*board.cell_size,
            (self.pos[0] + 9/16)*board.cell_size, (self.pos[1] + 9/16)*board.cell_size,
            fill="purple")]

    def success(self, board):
        board.itemconfig(self.shapes[0], fill="green")

    def error(self, board):
        board.itemconfig(self.shapes[0], fill="red")

    def normal(self, board):
        board.itemconfig(self.shapes[0], fill="purple")

    def is_satisfied(self, solution, board):
        return self.pos in solution.visited


class EdgeExactlyOneVertex(EdgeRule):
    def __init__(self, p, q):
        super().__init__(p, q)

    def draw(self, board):
        self.shapes = [board.create_oval(
            ((self.p[0] + self.q[0])/2 + 7/16)*board.cell_size, ((self.p[1] + self.q[1])/2 + 7/16)*board.cell_size,
            ((self.p[0] + self.q[0])/2 + 9/16)*board.cell_size, ((self.p[1] + self.q[1])/2 + 9/16)*board.cell_size,
            fill="purple")]

    def success(self, board):
        board.itemconfig(self.shapes[0], fill="green")

    def error(self, board):
        board.itemconfig(self.shapes[0], fill="red")

    def normal(self, board):
        board.itemconfig(self.shapes[0], fill="purple")

    def is_satisfied(self, solution, board):
        return (self.p in solution.visited) != (self.q in solution.visited)


class CellExactlyNVertex(CellRule):
    def __init__(self, pos, n):
        super().__init__(pos)
        self.n = n

    def draw(self, board):
        if self.n == 0:
            self.shapes = [board.create_oval((self.pos[0]+7/8)*board.cell_size,
                           (self.pos[1]+7/8)*board.cell_size,
                           (self.pos[0]+9/8)*board.cell_size,
                           (self.pos[1]+9/8)*board.cell_size,
                           outline="purple", fill=None, width=3)]
        elif self.n == 1:
            self.shapes = [board.create_oval((self.pos[0]+15/16)*board.cell_size,
                           (self.pos[1]+15/16)*board.cell_size,
                           (self.pos[0]+17/16)*board.cell_size,
                           (self.pos[1]+17/16)*board.cell_size,
                           fill="purple")]
        elif self.n == 2:
            self.shapes = [board.create_oval((self.pos[0] + 13/16)*board.cell_size,
                                             (self.pos[1] + 15/16)*board.cell_size,
                                             (self.pos[0] + 15/16)*board.cell_size,
                                             (self.pos[1] + 17/16)*board.cell_size,
                                             fill="purple"),
                           board.create_oval((self.pos[0] + 17/16)*board.cell_size,
                                             (self.pos[1] + 15/16)*board.cell_size,
                                             (self.pos[0] + 19/16)*board.cell_size,
                                             (self.pos[1] + 17/16)*board.cell_size,
                                             fill="purple")]
        elif self.n == 3:
            self.shapes = [board.create_oval((self.pos[0] + 1 + 1/16*(3*sin(0)-1))*board.cell_size,
                                             (self.pos[1] + 1 + 1/16*(3*cos(0)-1))*board.cell_size,
                                             (self.pos[0] + 1 + 1/16*(3*sin(0) + 1))*board.cell_size,
                                             (self.pos[1] + 1 + 1/16*(3*cos(0)+1))*board.cell_size,
                                             fill="purple"),
                           board.create_oval((self.pos[0] + 1 + 1/16*(3*sin(2*pi/3) - 1))*board.cell_size,
                                             (self.pos[1] + 1 + 1/16*(3*cos(2*pi/3) - 1))*board.cell_size,
                                             (self.pos[0] + 1 + 1/16*(3*sin(2*pi/3) + 1))*board.cell_size,
                                             (self.pos[1] + 1 + 1/16*(3*cos(2*pi/3) + 1))*board.cell_size,
                                             fill="purple"),
                           board.create_oval((self.pos[0] + 1 + 1/16*(3*sin(4*pi/3) - 1))*board.cell_size,
                                             (self.pos[1] + 1 + 1/16*(3*cos(4*pi/3) - 1))*board.cell_size,
                                             (self.pos[0] + 1 + 1/16*(3*sin(4*pi/3) + 1))*board.cell_size,
                                             (self.pos[1] + 1 + 1/16*(3*cos(4*pi/3) + 1))*board.cell_size,
                                             fill="purple"),
                           ]
        elif self.n == 4:
            self.shapes = [board.create_oval((self.pos[0] + 13/16)*board.cell_size,
                                             (self.pos[1] + 13/16)*board.cell_size,
                                             (self.pos[0] + 15/16)*board.cell_size,
                                             (self.pos[1] + 15/16)*board.cell_size,
                                             fill="purple"),
                           board.create_oval((self.pos[0] + 13/16)*board.cell_size,
                                             (self.pos[1] + 17/16)*board.cell_size,
                                             (self.pos[0] + 15/16)*board.cell_size,
                                             (self.pos[1] + 19/16)*board.cell_size,
                                             fill="purple"),
                           board.create_oval((self.pos[0] + 17/16)*board.cell_size,
                                             (self.pos[1] + 13/16)*board.cell_size,
                                             (self.pos[0] + 19/16)*board.cell_size,
                                             (self.pos[1] + 15/16)*board.cell_size,
                                             fill="purple"),
                           board.create_oval((self.pos[0] + 17/16)*board.cell_size,
                                             (self.pos[1] + 17/16)*board.cell_size,
                                             (self.pos[0] + 19/16)*board.cell_size,
                                             (self.pos[1] + 19/16)*board.cell_size,
                                             fill="purple")]

    def error(self, board):
        if self.n == 0:
            board.itemconfig(self.shapes[0], outline="red")
        else:
            for shape in self.shapes:
                board.itemconfig(shape, fill="red")

    def success(self, board):
        if self.n == 0:
            board.itemconfig(self.shapes[0], outline="green")
        else:
            for shape in self.shapes:
                board.itemconfig(shape, fill="green")

    def normal(self, board):
        if self.n == 0:
            board.itemconfig(self.shapes[0], outline="purple")
        else:
            for shape in self.shapes:
                board.itemconfig(shape, fill="purple")

    def is_satisfied(self, solution, board):
        return len([None for p in [(self.pos[0], self.pos[1]),
                          (self.pos[0], self.pos[1]+1),
                          (self.pos[0]+1, self.pos[1]),
                          (self.pos[0]+1, self.pos[1]+1)] if p in solution.visited]) == self.n


class CellExactlyNEdge(CellRule):
    def __init__(self, pos, n):
        super().__init__(pos)
        self.n = n

    def draw(self, board):
        if self.n == 1:
            self.shapes = [board.create_line((self.pos[0]+3/4)*board.cell_size,
                           (self.pos[1]+3/4)*board.cell_size,
                           (self.pos[0]+5/4)*board.cell_size,
                           (self.pos[1]+5/4)*board.cell_size,
                           fill="turquoise", width=3)]
        elif self.n == 2:
            self.shapes = [board.create_line((self.pos[0] + 1)*board.cell_size,
                                             (self.pos[1] + 3/4)*board.cell_size,
                                             (self.pos[0] + 3/4)*board.cell_size,
                                             (self.pos[1] + 5/4)*board.cell_size,
                                             fill="turquoise", width=3),
                           board.create_line((self.pos[0] + 1)*board.cell_size,
                                             (self.pos[1] + 3/4)*board.cell_size,
                                             (self.pos[0] + 5/4)*board.cell_size,
                                             (self.pos[1] + 5/4)*board.cell_size,
                                             fill="turquoise", width=3)]
        elif self.n == 3:
            self.shapes = [board.create_line((self.pos[0] + 1 + 1/3*sin(0))*board.cell_size,
                                             (self.pos[1] + .95 + 1/3*cos(0))*board.cell_size,
                                             (self.pos[0] + 1 + 1/3*sin(2*pi/3))*board.cell_size,
                                             (self.pos[1] + .95 + 1/3*cos(2*pi/3))*board.cell_size,
                                             fill="turquoise", width=3),
                           board.create_line((self.pos[0] + 1 + 1/3*sin(4*pi/3))*board.cell_size,
                                             (self.pos[1] + .95 + 1/3*cos(4*pi/3))*board.cell_size,
                                             (self.pos[0] + 1 + 1/3*sin(2*pi/3))*board.cell_size,
                                             (self.pos[1] + .95 + 1/3*cos(2*pi/3))*board.cell_size,
                                             fill="turquoise", width=3),
                           board.create_line((self.pos[0] + 1 + 1/3*sin(0))*board.cell_size,
                                             (self.pos[1] + .95 + 1/3*cos(0))*board.cell_size,
                                             (self.pos[0] + 1 + 1/3*sin(4*pi/3))*board.cell_size,
                                             (self.pos[1] + .95 + 1/3*cos(4*pi/3))*board.cell_size,
                                             fill="turquoise", width=3),
                           ]

    def error(self, board):
        for shape in self.shapes:
            board.itemconfig(shape, fill="red")

    def success(self, board):
        for shape in self.shapes:
            board.itemconfig(shape, fill="green")

    def normal(self, board):
        for shape in self.shapes:
            board.itemconfig(shape, fill="turquoise")

    def is_satisfied(self, solution, board):
        return len([None for p in [((self.pos[0], self.pos[1]), (self.pos[0]+1, self.pos[1])),
                                   ((self.pos[0]+1, self.pos[1]), (self.pos[0], self.pos[1])),
                                   ((self.pos[0], self.pos[1]), (self.pos[0], self.pos[1]+1)),
                                   ((self.pos[0], self.pos[1]+1), (self.pos[0], self.pos[1])),
                                   ((self.pos[0]+1, self.pos[1]), (self.pos[0]+1, self.pos[1]+1)),
                                   ((self.pos[0]+1, self.pos[1]+1), (self.pos[0]+1, self.pos[1])),
                                   ((self.pos[0], self.pos[1]+1), (self.pos[0]+1, self.pos[1]+1)),
                                   ((self.pos[0]+1, self.pos[1]+1), (self.pos[0], self.pos[1]+1))]
                    if p in solution.connections]) == self.n


class IncludeEdge(EdgeRule):
    def __init__(self, p, q):
        super().__init__(p, q)

    def draw(self, board):
        if self.p[0] == self.q[0]:
            self.shapes = [board.create_line((self.p[0] + 1/2)*board.cell_size,
                                             (self.p[1] + 3/4)*board.cell_size,
                                             (self.p[0] + 1/2)*board.cell_size,
                                             (self.p[1] + 5/4)*board.cell_size,
                                             fill="turquoise", width=7),
                           ]
        else:
            self.shapes = [board.create_line((self.p[0] + 3/4)*board.cell_size,
                                             (self.p[1] + 1/2)*board.cell_size,
                                             (self.p[0] + 5/4)*board.cell_size,
                                             (self.p[1] + 1/2)*board.cell_size,
                                             fill="turquoise", width=7),
                           ]

    def error(self, board):
        for shape in self.shapes:
            board.itemconfig(shape, fill="red")

    def success(self, board):
        for shape in self.shapes:
            board.itemconfig(shape, fill="green")

    def normal(self, board):
        for shape in self.shapes:
            board.itemconfig(shape, fill="turquoise")

    def is_satisfied(self, solution, board):
        return (self.p, self.q) in solution.connections or (self.q, self.p) in solution.connections


class FinishVertex(VertexRule):
    def __init__(self, pos):
        super().__init__(pos)

    def draw(self, board):
        self.shapes = [board.create_oval(
            (self.pos[0] + 7/16)*board.cell_size, (self.pos[1] + 7/16)*board.cell_size,
            (self.pos[0] + 9/16)*board.cell_size, (self.pos[1] + 9/16)*board.cell_size,
            fill="blue")]

    def success(self, board):
        board.itemconfig(self.shapes[0], fill="green")

    def error(self, board):
        board.itemconfig(self.shapes[0], fill="red")

    def normal(self, board):
        board.itemconfig(self.shapes[0], fill="blue")

    def is_satisfied(self, solution, board):
        return solution.connections[-1][1] == self.pos


def cell_in_domain(board, pos):
    return pos in board.cells


def vertex_in_domain(board, pos):
    pass


def get_area(board, solution, pos):
    area = [pos]
    to_visit = [pos]

    while len(to_visit) != 0:
        cur = to_visit.pop()

        if ((cur[0], cur[1]), (cur[0]+1, cur[1])) not in solution.connections and \
           ((cur[0]+1, cur[1]), (cur[0], cur[1])) not in solution.connections and \
           cell_in_domain(board, (cur[0], cur[1]-1)) and (cur[0], cur[1]-1) not in area:
            area.append((cur[0], cur[1]-1))
            to_visit.append((cur[0], cur[1]-1))
        if ((cur[0], cur[1]), (cur[0], cur[1]+1)) not in solution.connections and \
           ((cur[0], cur[1]+1), (cur[0], cur[1])) not in solution.connections and \
           cell_in_domain(board, (cur[0]-1, cur[1])) and (cur[0]-1, cur[1]) not in area:
            area.append((cur[0]-1, cur[1]))
            to_visit.append((cur[0]-1, cur[1]))
        if ((cur[0]+1, cur[1]+1), (cur[0], cur[1]+1)) not in solution.connections and \
           ((cur[0], cur[1]+1), (cur[0]+1, cur[1]+1)) not in solution.connections and \
           cell_in_domain(board, (cur[0], cur[1]+1)) and (cur[0], cur[1]+1) not in area:
            area.append((cur[0], cur[1]+1))
            to_visit.append((cur[0], cur[1]+1))
        if ((cur[0]+1, cur[1]+1), (cur[0]+1, cur[1])) not in solution.connections and \
           ((cur[0]+1, cur[1]), (cur[0]+1, cur[1]+1)) not in solution.connections and \
           cell_in_domain(board, (cur[0]+1, cur[1])) and (cur[0]+1, cur[1]) not in area:
            area.append((cur[0]+1, cur[1]))
            to_visit.append((cur[0]+1, cur[1]))

    return area


class GroupCell(CellRule):
    def __init__(self, pos, n, color="orange"):
        super().__init__(pos)
        self.n = n
        self.color = color

    def draw(self, board):
        self.shapes = [board.create_text((self.pos[0]+1)*board.cell_size, (self.pos[1]+1)*board.cell_size, fill=self.color, width=3, text=str(self.n), font="Times 20")]

    def error(self, board):
        board.itemconfig(self.shapes[0], fill="red")

    def success(self, board):
        board.itemconfig(self.shapes[0], fill="green")

    def normal(self, board):
        board.itemconfig(self.shapes[0], fill=self.color)

    def is_satisfied(self, solution, board):
        cols = 0
        for cell in get_area(board, solution, self.pos):
            obj = board.cell_rule_at(cell)
            if isinstance(obj, GroupCell) or isinstance(obj, ColorCell) and obj.color == self.color:
                cols += 1

        return self.n == cols


class ColorCell(CellRule):
    def __init__(self, pos, color="orange"):
        super().__init__(pos)
        self.color = color

    def draw(self, board):
        self.shapes = [board.create_rectangle((self.pos[0]+3/4)*board.cell_size, (self.pos[1]+3/4)*board.cell_size,
                                              (self.pos[0]+5/4)*board.cell_size, (self.pos[1]+5/4)*board.cell_size,
                                              fill=self.color, outline="")]

    def error(self, board):
        board.itemconfig(self.shapes[0], fill="red")

    def success(self, board):
        board.itemconfig(self.shapes[0], fill="green")

    def normal(self, board):
        board.itemconfig(self.shapes[0], fill=self.color)

    def is_satisfied(self, solution, board):
        for cell in get_area(board, solution, self.pos):
            obj = board.cell_rule_at(cell)
            if isinstance(obj, ColorCell) and obj.color != self.color:
                return False

        return True


class ConstructedAreaRule(CellRule):
    def __init__(self, pos, grpkey=None):
        super().__init__(pos)
        self.grpkey = grpkey

    def chomp(self, area, solution, board):
        yield area

    def satisfied_rec(self, board, solution, area, chomped, group_rules):
        for a in self.chomp(chomped, solution, board):
            if len(group_rules) == 1 or group_rules[1].satisfied_rec(board, area, a, group_rules[1:]):
                return True
        return False

    def is_satisfied(self, solution, board):
        area = get_area(board, solution, self.pos)
        group_rules = [self]
        for cell in area:
            obj = board.cell_rule_at(cell)
            if isinstance(obj, ConstructedAreaRule) and obj.grpkey == self.grpkey and obj is not self:
                group_rules.append(obj)

        return self.satisfied_rec(board, solution, area, area, group_rules)


CLASS_RULES = {IncludeVertex: "Pass through the purple vertices if they are on a vertex",
               EdgeExactlyOneVertex: "Pass through exactly one vertex adjacent to edges marked with purple dots",
               CellExactlyNVertex: "Pass through as equally many vertices adjacent to cells as marked if marked with purple dots",
               IncludeEdge: "Pass through cyan edges if they are on an edge",
               CellExactlyNEdge: "Pass through as equally many edges adjacent to cells as marked if marked with cyan lines",
               FinishVertex: "End at the blue vertex",
               ColorCell: "Separate cells with different colored rectangles",
               GroupCell: "Include equally many colored cells as indicated by colored numbers (both squares and numbers count)"}
