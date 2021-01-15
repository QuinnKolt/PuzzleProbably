import math
import tkinter as tk
from threading import Thread

from playsound import playsound

from gameplay.levels import get_level
from gui import controls
from gui.menus.levelscreen import LevelScreen
CELL = 64


class GameApp(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.levelnum = 1
        self.board = None
        self.levelscreen = None
        self.cell_size = CELL

    def new_board(self, board):
        from gui.boardviews.play import PlayerCanvas
        if self.levelscreen is not None:
            self.levelscreen.destroy()
            self.levelscreen = None
        for binding in controls.CONTINUE:
            binding.unbind()

        self.board = PlayerCanvas(board=board, app=self)
        self.levelnum += 1
        sound("res/softstart.wav")

    def new_level(self):
        if self.board is not None:
            self.board.destroy()
            if self.board.rule_bulletin is not None:
                self.board.rule_bulletin.destroy()
            self.board = None

        self.levelscreen = LevelScreen(self, get_level(self.levelnum))


def dist_real_to_coord(coord1, coord2):
    return math.sqrt((coord1[0] - (coord2[0] + 0.5) * CELL) ** 2 +
                     (coord1[1] - (coord2[1] + 0.5) * CELL) ** 2)


def bounds(canvas, item):
    coords = canvas.bbox(item)
    bounds = coords[2] - coords[0], coords[3] - coords[1]
    return bounds


def sound(file):
    Thread(target=lambda: playsound(file)).start()


class State(tk.Canvas):
    def __init__(self, app: GameApp, dim: tuple):
        super().__init__(app.master, width=dim[0], height=dim[1])
        self.master.minsize(*dim)
        self.app = app

    def draw(self):
        pass
