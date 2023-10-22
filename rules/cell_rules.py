from math import sin, cos, pi

from rules.rules import GameRule


class CellRule(GameRule):
    def __init__(self, pos):
        super().__init__()
        self.pos = pos
        self.essential_data.append(pos)


class CellExactlyNVertex(CellRule):
    def __init__(self, pos, n):
        super().__init__(pos)
        self.n = n
        self.essential_data.append(n)

    def draw(self, state):
        if self.n == 0:
            self.shapes = [state.create_oval((self.pos[0]+7/8)*state.app.cell_size,
                                             (self.pos[1]+7/8)*state.app.cell_size,
                                             (self.pos[0]+9/8)*state.app.cell_size,
                                             (self.pos[1]+9/8)*state.app.cell_size,
                                             outline="purple", fill=None, width=3)]
        elif self.n == 1:
            self.shapes = [state.create_oval((self.pos[0] + 15/16)*state.app.cell_size,
                                             (self.pos[1]+15/16)*state.app.cell_size,
                                             (self.pos[0]+17/16)*state.app.cell_size,
                                             (self.pos[1]+17/16)*state.app.cell_size,
                                             fill="purple")]
        elif self.n == 2:
            self.shapes = [state.create_oval((self.pos[0] + 13/16)*state.app.cell_size,
                                             (self.pos[1] + 15/16)*state.app.cell_size,
                                             (self.pos[0] + 15/16)*state.app.cell_size,
                                             (self.pos[1] + 17/16)*state.app.cell_size,
                                             fill="purple"),
                           state.create_oval((self.pos[0] + 17/16)*state.app.cell_size,
                                             (self.pos[1] + 15/16)*state.app.cell_size,
                                             (self.pos[0] + 19/16)*state.app.cell_size,
                                             (self.pos[1] + 17/16)*state.app.cell_size,
                                             fill="purple")]
        elif self.n == 3:
            self.shapes = [state.create_oval((self.pos[0] + 1 + 1/16*(3*sin(0) - 1))*state.app.cell_size,
                                             (self.pos[1] + 1 + 1/16*(3*cos(0)-1))*state.app.cell_size,
                                             (self.pos[0] + 1 + 1/16*(3*sin(0) + 1))*state.app.cell_size,
                                             (self.pos[1] + 1 + 1/16*(3*cos(0)+1))*state.app.cell_size,
                                             fill="purple"),
                           state.create_oval((self.pos[0] + 1 + 1/16*(3*sin(2*pi/3) - 1))*state.app.cell_size,
                                             (self.pos[1] + 1 + 1/16*(3*cos(2*pi/3) - 1))*state.app.cell_size,
                                             (self.pos[0] + 1 + 1/16*(3*sin(2*pi/3) + 1))*state.app.cell_size,
                                             (self.pos[1] + 1 + 1/16*(3*cos(2*pi/3) + 1))*state.app.cell_size,
                                             fill="purple"),
                           state.create_oval((self.pos[0] + 1 + 1/16*(3*sin(4*pi/3) - 1))*state.app.cell_size,
                                             (self.pos[1] + 1 + 1/16*(3*cos(4*pi/3) - 1))*state.app.cell_size,
                                             (self.pos[0] + 1 + 1/16*(3*sin(4*pi/3) + 1))*state.app.cell_size,
                                             (self.pos[1] + 1 + 1/16*(3*cos(4*pi/3) + 1))*state.app.cell_size,
                                             fill="purple"),
                           ]
        elif self.n == 4:
            self.shapes = [state.create_oval((self.pos[0] + 13/16)*state.app.cell_size,
                                             (self.pos[1] + 13/16)*state.app.cell_size,
                                             (self.pos[0] + 15/16)*state.app.cell_size,
                                             (self.pos[1] + 15/16)*state.app.cell_size,
                                             fill="purple"),
                           state.create_oval((self.pos[0] + 13/16)*state.app.cell_size,
                                             (self.pos[1] + 17/16)*state.app.cell_size,
                                             (self.pos[0] + 15/16)*state.app.cell_size,
                                             (self.pos[1] + 19/16)*state.app.cell_size,
                                             fill="purple"),
                           state.create_oval((self.pos[0] + 17/16)*state.app.cell_size,
                                             (self.pos[1] + 13/16)*state.app.cell_size,
                                             (self.pos[0] + 19/16)*state.app.cell_size,
                                             (self.pos[1] + 15/16)*state.app.cell_size,
                                             fill="purple"),
                           state.create_oval((self.pos[0] + 17/16)*state.app.cell_size,
                                             (self.pos[1] + 17/16)*state.app.cell_size,
                                             (self.pos[0] + 19/16)*state.app.cell_size,
                                             (self.pos[1] + 19/16)*state.app.cell_size,
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

    def is_satisfied(self, board, solution):
        return len([None for p in [(self.pos[0], self.pos[1]),
                          (self.pos[0], self.pos[1]+1),
                          (self.pos[0]+1, self.pos[1]),
                          (self.pos[0]+1, self.pos[1]+1)] if p in solution.visited]) == self.n

    def bulletin(self):
        return "Pass through as equally many vertices adjacent to cells as marked if marked with purple dots"


class CellExactlyNEdge(CellRule):
    def __init__(self, pos, n):
        super().__init__(pos)
        self.n = n
        self.essential_data.append(n)

    def draw(self, state):
        if self.n == 1:
            self.shapes = [state.create_line((self.pos[0] + 3/4)*state.app.cell_size,
                                             (self.pos[1]+3/4)*state.app.cell_size,
                                             (self.pos[0]+5/4)*state.app.cell_size,
                                             (self.pos[1]+5/4)*state.app.cell_size,
                                             fill="turquoise", width=3)]
        elif self.n == 2:
            self.shapes = [state.create_line((self.pos[0] + 1)*state.app.cell_size,
                                             (self.pos[1] + 3/4)*state.app.cell_size,
                                             (self.pos[0] + 3/4)*state.app.cell_size,
                                             (self.pos[1] + 5/4)*state.app.cell_size,
                                             fill="turquoise", width=3),
                           state.create_line((self.pos[0] + 1)*state.app.cell_size,
                                             (self.pos[1] + 3/4)*state.app.cell_size,
                                             (self.pos[0] + 5/4)*state.app.cell_size,
                                             (self.pos[1] + 5/4)*state.app.cell_size,
                                             fill="turquoise", width=3)]
        elif self.n == 3:
            self.shapes = [state.create_line((self.pos[0] + 1 + 1/3*sin(0))*state.app.cell_size,
                                             (self.pos[1] + .95 + 1/3*cos(0))*state.app.cell_size,
                                             (self.pos[0] + 1 + 1/3*sin(2*pi/3))*state.app.cell_size,
                                             (self.pos[1] + .95 + 1/3*cos(2*pi/3))*state.app.cell_size,
                                             fill="turquoise", width=3),
                           state.create_line((self.pos[0] + 1 + 1/3*sin(4*pi/3))*state.app.cell_size,
                                             (self.pos[1] + .95 + 1/3*cos(4*pi/3))*state.app.cell_size,
                                             (self.pos[0] + 1 + 1/3*sin(2*pi/3))*state.app.cell_size,
                                             (self.pos[1] + .95 + 1/3*cos(2*pi/3))*state.app.cell_size,
                                             fill="turquoise", width=3),
                           state.create_line((self.pos[0] + 1 + 1/3*sin(0))*state.app.cell_size,
                                             (self.pos[1] + .95 + 1/3*cos(0))*state.app.cell_size,
                                             (self.pos[0] + 1 + 1/3*sin(4*pi/3))*state.app.cell_size,
                                             (self.pos[1] + .95 + 1/3*cos(4*pi/3))*state.app.cell_size,
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

    def is_satisfied(self, board, solution):
        return len([None for p in [((self.pos[0], self.pos[1]), (self.pos[0]+1, self.pos[1])),
                                   ((self.pos[0]+1, self.pos[1]), (self.pos[0], self.pos[1])),
                                   ((self.pos[0], self.pos[1]), (self.pos[0], self.pos[1]+1)),
                                   ((self.pos[0], self.pos[1]+1), (self.pos[0], self.pos[1])),
                                   ((self.pos[0]+1, self.pos[1]), (self.pos[0]+1, self.pos[1]+1)),
                                   ((self.pos[0]+1, self.pos[1]+1), (self.pos[0]+1, self.pos[1])),
                                   ((self.pos[0], self.pos[1]+1), (self.pos[0]+1, self.pos[1]+1)),
                                   ((self.pos[0]+1, self.pos[1]+1), (self.pos[0], self.pos[1]+1))]
                    if p in solution.connections]) == self.n

    def bulletin(self):
        return "Pass through as equally many edges adjacent to cells as marked if marked with cyan lines"