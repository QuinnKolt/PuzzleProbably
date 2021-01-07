import math
from playsound import playsound
from threading import Thread
from gameplay.levels import *
from gui.menus.levelscreen import *

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
        self.levelnum = 1
        self.board = None
        self.levelscreen = None
        self.buttons = []
        self.cell_size = CELL
        from gui.boardviews.play import PlayerCanvas
        from gui.boardviews.design import DesignerCanvas

        # TODO this is an awful line of code
        self.board_class = {PLAYING: PlayerCanvas, DESIGNING: DesignerCanvas}[CURRENT_STATE]

    def new_board(self, board):
        if self.levelscreen is not None:
            self.levelscreen.destroy()
            self.levelscreen = None
        for binding in controls.SELECT:
            binding.unbind()

        self.board = self.board_class(board=board, app=self)
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


def main():
    root = tk.Tk()
    root.geometry("1000x800")
    app = GameApp(master=root)
    app.focus_set()
    app.new_level()
    app.mainloop()


if __name__ == "__main__":
    main()
