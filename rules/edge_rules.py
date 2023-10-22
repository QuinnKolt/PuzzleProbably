from rules.rules import GameRule


class EdgeRule(GameRule):
    def __init__(self, p, q):
        super().__init__()
        self.p = p
        self.q = q
        self.essential_data.extend([p, q])


class IncludeEdge(EdgeRule):
    def __init__(self, p, q):
        super().__init__(p, q)

    def draw(self, state):
        if self.p[0] == self.q[0]:
            self.shapes = [state.create_line((self.p[0] + 1/2)*state.app.cell_size,
                                             (self.p[1] + 3/4)*state.app.cell_size,
                                             (self.p[0] + 1/2)*state.app.cell_size,
                                             (self.p[1] + 5/4)*state.app.cell_size,
                                             fill="turquoise", width=7),
                           ]
        else:
            self.shapes = [state.create_line((self.p[0] + 3/4)*state.app.cell_size,
                                             (self.p[1] + 1/2)*state.app.cell_size,
                                             (self.p[0] + 5/4)*state.app.cell_size,
                                             (self.p[1] + 1/2)*state.app.cell_size,
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

    def is_satisfied(self, board, solution):
        return (self.p, self.q) in solution.connections or (self.q, self.p) in solution.connections

    def bulletin(self):
        return "Pass through cyan edges if they are on an edge"


class EdgeExactlyOneVertex(EdgeRule):
    def __init__(self, p, q):
        super().__init__(p, q)

    def draw(self, state):
        self.shapes = [state.create_oval(
            ((self.p[0] + self.q[0])/2 + 7/16)*state.app.cell_size, ((self.p[1] + self.q[1])/2 + 7/16)*state.app.cell_size,
            ((self.p[0] + self.q[0])/2 + 9/16)*state.app.cell_size, ((self.p[1] + self.q[1])/2 + 9/16)*state.app.cell_size,
            fill="purple")]

    def success(self, board):
        board.itemconfig(self.shapes[0], fill="green")

    def error(self, board):
        board.itemconfig(self.shapes[0], fill="red")

    def normal(self, board):
        board.itemconfig(self.shapes[0], fill="purple")

    def is_satisfied(self, board, solution):
        return (self.p in solution.visited) != (self.q in solution.visited)

    def bulletin(self):
        return "Pass through exactly one vertex adjacent to edges marked with purple dots"

class OneWayEdge(EdgeRule):
    def __init__(self, p, q):
        super().__init__(p, q)

    def draw(self, state):
        if self.p[0] != self.q[0]:
            self.shapes = [state.create_polygon((3/5*self.p[0] + 2/5*self.q[0] + 0.5) * state.app.cell_size,
                                                (self.p[1] + 1/10 + 0.5) * state.app.cell_size,
                                                (3/5*self.p[0] + 2/5*self.q[0] + 0.5) * state.app.cell_size,
                                                (self.p[1] - 1/10 + 0.5) * state.app.cell_size,
                                                (2/5*self.p[0] + 3/5*self.q[0] + 0.5) * state.app.cell_size,
                                                (self.p[1] + 0.5) * state.app.cell_size,
                                                fill="grey")]
        else:
            self.shapes = [state.create_polygon((self.p[0] + 1 / 10 + 0.5) * state.app.cell_size,
                                                (3 / 5 * self.p[1] + 2 / 5 * self.q[1] + 0.5) * state.app.cell_size,
                                                (self.p[0] - 1 / 10 + 0.5) * state.app.cell_size,
                                                (3 / 5 * self.p[1] + 2 / 5 * self.q[1] + 0.5) * state.app.cell_size,
                                                (self.p[0] + 0.5) * state.app.cell_size,
                                                (2 / 5 * self.p[1] + 3 / 5 * self.q[1] + 0.5) * state.app.cell_size,
                                                fill="grey")]

    def success(self, board):
        board.itemconfig(self.shapes[0], fill="green")

    def error(self, board):
        board.itemconfig(self.shapes[0], fill="red")

    def normal(self, board):
        board.itemconfig(self.shapes[0], fill="grey")

    def is_satisfied(self, board, solution):
        return (self.q, self.p) not in solution.connections

    def bulletin(self):
        return "Any connection on edge with an arrow must be oriented in the arrow's direction"

