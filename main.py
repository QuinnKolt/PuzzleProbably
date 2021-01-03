import tkinter as tk
import math
from rules import *
from playsound import playsound
from threading import Thread
from board import *
from solver import Path

HEI = 7
WID = 5
CELL = 64


PLAYING = "PLAYING"
DESIGNING = "DESIGNING"

# Start the app in the design state
CURRENT_STATE = PLAYING


class GameApp(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.level = 1
        self.board = None
        self.rule_board = None
        self.buttons = []
        self.bindings = {}
        self.cell_size = CELL
        from play import PlayerCanvas
        from design import DesignerCanvas

        # TODO this is an awful line of code
        self.board_class = {PLAYING: PlayerCanvas, DESIGNING: DesignerCanvas}[CURRENT_STATE]

    def new_board(self):
        self.level_text.destroy()
        self.master.unbind('<Return>', self.key[0])
        self.master.unbind('<ButtonRelease-3>', self.key[1])

        domain = random_domain_path(WID, HEI, [])

        rules = [EdgesGreaterThanRule(12), CellExactlyNVertex((3, 1), 2),
                 EdgeExactlyOneVertex((3, 0), (3, 1)), CellExactlyNEdge((1, 4), 3),
                 IncludeVertex((1, 4)), IncludeEdge((2, 3), (2, 4)),
                 FinishVertex((3, 3)), GroupCell((0, 1), 2), GroupCell((3, 5), 1),
                 ColorCell((1, 5)), ColorCell((3, 0), color="steel blue")]

        self.board = self.board_class(board=Board(*domain, rules, [(0, 0), (3, 5)]), app=self, wr=(WID, HEI))

        self.level += 1

    def new_level(self):
        if self.board is not None:
            self.board.destroy()
            if self.board.rule_board is not None:
                self.board.rule_board.destroy()

        self.key = [self.master.bind('<Return>', lambda e: self.new_board()),
                    self.master.bind('<ButtonRelease-3>', lambda e: self.new_board())]
        self.level_text = tk.Canvas(self.master, state=tk.DISABLED, width=400, height=400)
        self.level_text.create_text(200, 200, fill="darkblue", font="Courier 20 bold", text="Level " + str(self.level))

        self.level_text.pack(anchor=tk.CENTER)


def dist_real_to_coord(coord1, coord2):
    return math.sqrt((coord1[0] - (coord2[0] + 0.5) * CELL) ** 2 +
                     (coord1[1] - (coord2[1] + 0.5) * CELL) ** 2)


def bounds(canvas, item):
    coords = canvas.bbox(item)
    bounds = coords[2] - coords[0], coords[3] - coords[1]
    return bounds


def main():
    root = tk.Tk()
    root.geometry("1000x800")
    app = GameApp(master=root)
    app.focus_set()
    app.new_level()
    app.mainloop()


if __name__ == "__main__":
    main()
