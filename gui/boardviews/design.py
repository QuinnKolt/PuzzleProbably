from main import *
from gui.boardviews.bulletin import RuleBulletin


class DesignerCanvas(tk.Canvas):
    def __init__(self, board, app: GameApp):
        super().__init__(app.master, width=board.wid*app.cell_size, height=board.hei*app.cell_size)
        self.rules = []
        self.app = app
        self.vrule_list = [lambda pos: FinishVertex(pos)]
        self.erule_list = [lambda p, q: EdgeExactlyOneVertex(p, q)]
        self.crule_list = [lambda pos: CellExactlyNEdge(pos, 1)]
        self.vtool = 0
        self.etool = 0
        self.crule = 0
        self.board = board
        self.dmode = True

        self.rule_board = RuleBulletin(app, board.constraints, board.hei)

        self.board.draw(self)
        self.draw_dots()
        self.master.minsize((board.wid + 1)*app.cell_size+500, (board.hei + 1)*app.cell_size)
        self.place(relx=0.25, rely=0.5, anchor=tk.CENTER)

    def draw_dots(self):
        for i in range(self.board.wid):
            for j in range(self.board.hei):
                self.create_oval((i + 15/32) * self.app.cell_size, (j + 15/32) * self.app.cell_size,
                                 (i + 17/32) * self.app.cell_size, (j + 17/32) * self.app.cell_size,
                                 fill="slate gray")

    def add_rule(self, e):
        pass

    def add_domain(self, e):
        pass

    def remove_rule(self, e):
        pass

    def remove_domain(self, e):
        pass
