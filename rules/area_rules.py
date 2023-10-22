from rules.cell_rules import CellRule


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
        self.essential_data.extend([n, color])

    def draw(self, state):
        self.shapes = [state.create_text((self.pos[0] + 1)*state.app.cell_size, (self.pos[1] + 1)*state.app.cell_size, fill=self.color, width=3, text=str(self.n), font="Times 20")]

    def error(self, board):
        board.itemconfig(self.shapes[0], fill="red")

    def success(self, board):
        board.itemconfig(self.shapes[0], fill="green")

    def normal(self, board):
        board.itemconfig(self.shapes[0], fill=self.color)

    def is_satisfied(self, board, solution):
        cols = 0
        for cell in get_area(board, solution, self.pos):
            obj = board.cell_rule_at(cell)
            if isinstance(obj, GroupCell) or isinstance(obj, ColorCell) and obj.color == self.color:
                cols += 1

        return self.n == cols

    def bulletin(self):
        return "Include equally many colored cells as indicated by colored numbers (both squares and numbers count)"


class ColorCell(CellRule):
    def __init__(self, pos, color="orange"):
        super().__init__(pos)
        self.color = color
        self.essential_data.append(color)

    def draw(self, state):
        self.shapes = [state.create_rectangle((self.pos[0] + 3/4)*state.app.cell_size, (self.pos[1] + 3/4)*state.app.cell_size,
                                              (self.pos[0]+5/4)*state.app.cell_size, (self.pos[1] + 5/4)*state.app.cell_size,
                                              fill=self.color, outline="")]

    def error(self, board):
        board.itemconfig(self.shapes[0], fill="red")

    def success(self, board):
        board.itemconfig(self.shapes[0], fill="green")

    def normal(self, board):
        board.itemconfig(self.shapes[0], fill=self.color)

    def is_satisfied(self, board, solution):
        for cell in get_area(board, solution, self.pos):
            obj = board.cell_rule_at(cell)
            if isinstance(obj, ColorCell) and obj.color != self.color:
                return False

        return True

    def bulletin(self):
        return "Separate cells with different colored squares"


class ConstructedAreaRule(CellRule):
    def __init__(self, pos, grpkey=None):
        super().__init__(pos)
        self.grpkey = grpkey
        self.essential_data.append(grpkey)

    def chomp(self, area, solution, board):
        yield area

    def satisfied_rec(self, board, solution, area, chomped, group_rules):
        for a in self.chomp(chomped, solution, board):
            if len(group_rules) == 1 or group_rules[1].satisfied_rec(board, area, a, group_rules[1:]):
                return True
        return False

    def is_satisfied(self, board, solution):
        area = get_area(board, solution, self.pos)
        group_rules = [self]
        for cell in area:
            obj = board.cell_rule_at(cell)
            if isinstance(obj, ConstructedAreaRule) and obj.grpkey == self.grpkey and obj is not self:
                group_rules.append(obj)

        return self.satisfied_rec(board, solution, area, area, group_rules)
