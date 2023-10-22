from rules.rules import GameRule


class VertexRule(GameRule):
    def __init__(self, pos):
        super().__init__()
        self.pos = pos
        self.essential_data.append(pos)


class IncludeVertex(VertexRule):
    def __init__(self, pos):
        super().__init__(pos)

    def draw(self, state):
        self.shapes = [state.create_oval(
            (self.pos[0] + 7/16)*state.app.cell_size, (self.pos[1] + 7/16)*state.app.cell_size,
            (self.pos[0] + 9/16)*state.app.cell_size, (self.pos[1] + 9/16)*state.app.cell_size,
            fill="purple")]

    def success(self, board):
        board.itemconfig(self.shapes[0], fill="green")

    def error(self, board):
        board.itemconfig(self.shapes[0], fill="red")

    def normal(self, board):
        board.itemconfig(self.shapes[0], fill="purple")

    def is_satisfied(self, board, solution):
        return self.pos in solution.visited

    def bulletin(self):
        return "Pass through the purple vertices if they are on a vertex"


class FinishVertex(VertexRule):
    def __init__(self, pos):
        super().__init__(pos)

    def draw(self, state):
        self.shapes = [state.create_oval(
            (self.pos[0] + 7/16)*state.app.cell_size, (self.pos[1] + 7/16)*state.app.cell_size,
            (self.pos[0] + 9/16)*state.app.cell_size, (self.pos[1] + 9/16)*state.app.cell_size,
            fill="blue")]

    def success(self, board):
        board.itemconfig(self.shapes[0], fill="green")

    def error(self, board):
        board.itemconfig(self.shapes[0], fill="red")

    def normal(self, board):
        board.itemconfig(self.shapes[0], fill="blue")

    def is_satisfied(self, board, solution):
        return solution.cur == self.pos

    def bulletin(self):
        return "End at the blue vertex"