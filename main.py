import tkinter as tk
import math
from threading import Thread

from playsound import playsound

import levels
from rules import *
from board import *

CELL = 64

PLAYING = "PLAYING"
DESIGNING = "DESIGNING"

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
        self.state = PLAYING
        # self.state = DESIGNING

        from play import PlayerCanvas
        from design import DesignerCanvas

        # TODO this is an awful line of code
        self.board_class = {PLAYING: PlayerCanvas, DESIGNING: DesignerCanvas}[self.state]

    def new_board(self):
        self.level_text.destroy()
        self.master.unbind('<Return>', self.key[0])
        self.master.unbind('<ButtonRelease-3>', self.key[1])

        domain, rules, starts, wh = levels.level(0, self.level)

        self.board = self.board_class(board=Board(*domain, rules, starts), app=self, wr=wh)

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
