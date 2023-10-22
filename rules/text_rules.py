from rules.rules import GameRule


class TextRule(GameRule):
    def __init__(self, text):
        super().__init__()
        self.text = text

    def bulletin(self):
        return self.text


class EdgesLessThanRule(TextRule):
    def __init__(self, n):
        super().__init__("Complete the board in less than " + str(n) + " connections")
        self.n = n
        self.essential_data.append(n)

    def is_satisfied(self, board, solution):
        return len(solution.connections) < self.n


class EdgesGreaterThanRule(TextRule):
    def __init__(self, n):
        super().__init__("Complete the board in more than " + str(n) + " connections")
        self.n = n
        self.essential_data.append(n)

    def is_satisfied(self, board, solution):
        return len(solution.connections) > self.n


class EdgesExactlyRule(TextRule):
    def __init__(self, n):
        super().__init__("Complete the board in exactly " + str(n) + " connections")
        self.n = n
        self.essential_data.append(n)

    def is_satisfied(self, board, solution):
        return len(solution.connections) == self.n


class EveryVertexRule(TextRule):
    def __init__(self):
        super().__init__("Visit every vertex on the board")

    def is_satisfied(self, board, solution):
        return len(solution.visited) == len(board.vertices)


class BulletinInfo(TextRule):
    def __init__(self,info):
        super().__init__(info)

    def is_satisfied(self, board, solution):
        return True
