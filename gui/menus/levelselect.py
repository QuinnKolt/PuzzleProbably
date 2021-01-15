import tkinter as tk
import gui.controls
from gui.app import State

LEVEL_SIZE = 100


class LevelSelectScreen(State):
    def __init__(self, app, levels):
        super().__init__(app, (LEVEL_SIZE*7, LEVEL_SIZE*8))

        self.levels = levels

        self.create_text(30, 400, fill="darkblue", font="Courier 20 bold", text="Level Select")

        self.levelselectors = []
        k = 0
        for i in range(5):
            for j in range(6):
                if len(levels) > k:
                    self.preview(levels[k], (i, j))
                    k += 1
                else:
                    break
            if len(levels) <= k:
                break

        self.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.master.minsize(850, 850)

    def preview(self, level, pos):
        pass

    def choose(self):
        pass
