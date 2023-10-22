class GameRule:
    def __init__(self, essential_data=None):
        self.shapes = []
        if essential_data is None:
            essential_data = list()
        self.essential_data = essential_data

    def is_satisfied(self, board, solution):
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

    def draw(self, state):
        pass

    def bulletin(self):
        return ""

