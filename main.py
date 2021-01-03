import tkinter as tk
import math
from random import random
from rules import *
from playsound import playsound
from threading import Thread
from board import Board
from solver import Solution

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

        # TODO this is an awful line of code
        self.board_class = { PLAYING: PlayerBoard, DESIGNING: DesignerBoard }[CURRENT_STATE]

    def new_board(self):
        self.level_text.destroy()
        self.master.unbind('<Return>', self.key[0])
        self.master.unbind('<ButtonRelease-3>', self.key[1])

        domain = random_domain_path(WID, HEI, [])
        print(domain)

        rules = [EdgesGreaterThanRule(12), CellExactlyNVertex((3, 1), 2),
                 EdgeExactlyOneVertex((3, 0), (3, 1)), CellExactlyNEdge((1, 4), 3),
                 IncludeVertex((1, 4)), IncludeEdge((2, 3), (2, 4)),
                 FinishVertex((3, 3)), GroupCell((0, 1), 2), GroupCell((3, 5), 1),
                 ColorCell((1, 5)), ColorCell((3, 0), color="steel blue")]

        rule_texts = {rule: rule.text for rule in rules if isinstance(rule, TextRule)}
        rule_texts.update({type(rule): CLASS_RULES[type(rule)] for rule in rules if not isinstance(rule, TextRule)})

        self.rule_board = RuleBoard(self, rule_texts)

        self.board = self.board_class(board=Board(*domain, rules, [(0, 0), (3, 5)]), app=self, wr=(WID, HEI),
                                 cell_size=CELL)

        self.level += 1

    def new_level(self):
        if self.board is not None:
            self.board.destroy()
        if self.rule_board is not None:
            self.rule_board.destroy()

        self.key = [self.master.bind('<Return>', lambda e: self.new_board()),
                    self.master.bind('<ButtonRelease-3>', lambda e: self.new_board())]
        self.level_text = tk.Canvas(self.master, state=tk.DISABLED, width=400, height=400)
        self.level_text.create_text(200, 200, fill="darkblue", font="Courier 20 bold", text="Level " + str(self.level))

        self.level_text.pack(anchor=tk.CENTER)

    def design(self):
        self.board = DesignerBoard((WID, HEI), self)


class RuleBoard(tk.Canvas):
    def __init__(self, app: GameApp, rules):
        super().__init__(app.master, width=500, height=75 + 40*len(rules))
        if rules is not None:
            self.rule_texts = rules
        else:
            self.rule_texts = dict()
        self.rule_shapes = dict()
        self.draw()
        self.place(relx=0.75, rely=0.5, anchor=tk.CENTER)

    def __set__(self, instance, value):
        self.rule_texts[instance] = value

    def draw(self):
        self.create_rectangle(5, 5, 445, 70 + 40*len(self.rule_texts), fill="gray92", outline="dim gray")
        dep = 30
        for cl in self.rule_texts.keys():
            if isinstance(cl, TextRule):
                self.rule_shapes[cl] = self.create_text(25, dep, text=self.rule_texts[cl],
                                                        width=400, anchor=tk.NW, font="Helvetica 12 bold")
            else:
                self.rule_shapes[cl] = self.create_text(25, dep, text=self.rule_texts[cl],
                                                        width=400, anchor=tk.NW, font="Helvetica 10")
            b = bounds(self, self.rule_shapes[cl])
            dep += b[1] + 15

    def success(self, cl):
        self.itemconfig(self.rule_shapes[cl], fill="green")

    def error(self, cl):
        self.itemconfig(self.rule_shapes[cl], fill="red")

    def normal(self, cl):
        self.itemconfig(self.rule_shapes[cl], fill="black")


class DesignerBoard(tk.Canvas):
    def __init__(self, wr, app: GameApp, cell_size=64):
        super().__init__(app.master, width=wr[0]*cell_size, height=wr[1]*cell_size)
        self.start = (0,0)
        self.rules = []
        self.cell_size = cell_size
        self.app = app
        self.wr = wr
        self.vrule_list = [lambda pos: FinishVertex(pos)]
        self.erule_list = [lambda p, q: EdgeExactlyOneVertex(p, q)]
        self.crule_list = [lambda pos: CellExactlyNEdge(pos, 1)]
        self.master.minsize((wr[0] + 1)*cell_size, (wr[1] + 1)*cell_size)
        self.vtool = 0
        self.etool = 0
        self.crule = 0
        self.dmode = True
        self.draw_dots()
        self.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def draw_dots(self):
        for i in range(self.wr[0]):
            for j in range(self.wr[1]):
                self.create_oval((i + 15/32) * self.cell_size, (j + 15/32) * self.cell_size,
                                 (i + 17/32) * self.cell_size, (j + 17/32) * self.cell_size,
                                 fill="slate gray")

        self.sshape = self.create_oval((self.start[0] + 0.5) * 64 - 5, (self.start[1] + 0.5) * 64 - 5,
                         (self.start[0] + 0.5) * 64 + 5, (self.start[1] + 0.5) * 64 + 5,
                          fill="black", outline="black")

    def add_rule(self, e):
        pass

    def add_domain(self, e):
        pass

    def remove_rule(self, e):
        pass

    def remove_domain(self, e):
        pass


class PlayerBoard(tk.Canvas):
    def __init__(self, board, wr, app: GameApp, cell_size=64):
        super().__init__(app.master, width=wr[0]*cell_size, height=wr[1]*cell_size)
        self.cell_size = cell_size
        self.connections = []
        self.visual_connections = []
        self.connections_stack = [[]]
        self.visited = []
        self.board = board

        self.app = app
        self.wr = wr
        self.lines = []
        self.draw_grid()
        self.draw_objects()
        self.draw()
        self.bindings = {}
        self.appbindings = {}
        if len(self.board.starts) == 1:
            self.start = self.board.starts[0]
            self.cur = self.start
            self.line_draw_bindings()
            self.sshape = self.create_oval((self.start[0] + 0.5)*64 - 5, (self.start[1] + 0.5)*64 - 5,
                                           (self.start[0] + 0.5)*64 + 5, (self.start[1] + 0.5)*64 + 5,
                                           fill="black", outline="black")
        else:
            self.start_bindings()
        self.master.minsize((wr[0] + 1)*cell_size+500, (wr[1] + 1)*cell_size)
        self.place(relx=0.25, rely=0.5, anchor=tk.CENTER)

    def draw_grid(self):
        for cell in self.board.cells:
            self.create_rectangle((cell[0] + 0.5)*self.cell_size, (cell[1] + 0.5)*self.cell_size,
                                  (cell[0] + 1.5)*self.cell_size, (cell[1] + 1.5)*self.cell_size,
                                  fill="gray93", outline="light grey", dash=(4, 4), width=2)
        for segment in self.board.connections:
            self.create_line((segment[0][0] + 0.5) * self.cell_size, (segment[0][1] + 0.5) * self.cell_size,
                             (segment[1][0] + 0.5) * self.cell_size, (segment[1][1] + 0.5) * self.cell_size,
                             fill="gainsboro", width=5)
        for s in self.board.starts:
            self.create_oval((s[0] + 0.5)*64 - 5, (s[1] + 0.5)*64 - 5,
                             (s[0] + 0.5)*64 + 5, (s[1] + 0.5)*64 + 5,
                              fill="white", outline="black")

    def choose_start(self, e):
        for s in self.board.starts:
            if self.dist_real_to_coord((e.x, e.y), s) < self.cell_size/2:
                self.start = s
                self.cur = self.start
                self.unbindAll()
                self.sshape = self.create_oval((self.start[0] + 0.5)*64 - 5, (self.start[1] + 0.5)*64 - 5,
                                               (self.start[0] + 0.5)*64 + 5, (self.start[1] + 0.5)*64 + 5,
                                               fill="black", outline="black")
                self.line_draw_bindings()
                Thread(target=lambda: playsound("start.wav")).start()
                break

    def draw_objects(self):
        for rule in self.board.rules:
            rule.draw(self)

    def unbindAll(self):
        for key in self.bindings.keys():
            self.unbind(key, self.bindings[key])
        for key in self.appbindings:
            self.master.unbind(key, self.appbindings[key])
        self.appbindings = {}
        self.bindings = {}

    def show_succ_err(self):
        errcls = set()
        succls = set()
        for rule in self.board.rules:
            if rule.is_satisfied(Solution(self.visited, self.connections, self.cur, self.start), self.board):
                rule.success(self)
                if isinstance(rule, TextRule) and rule not in errcls:
                    succls.add(rule)
                elif type(rule) not in errcls:
                    succls.add(type(rule))
            else:
                rule.error(self)
                if isinstance(rule, TextRule):
                    errcls.add(rule)
                else:
                    errcls.add(type(rule))
                    if type(rule) in succls:
                        succls.remove(type(rule))

        for cl in errcls:
            self.app.rule_board.error(cl)
        for cl in succls:
            self.app.rule_board.success(cl)

    def unshow_succ_err(self):
        cls = set()
        for rule in self.board.rules:
            rule.normal(self)
            if isinstance(rule, TextRule):
                cls.add(rule)
            else:
                cls.add(type(rule))

        for cl in cls:
            self.app.rule_board.normal(cl)

    def win(self):
        self.unbindAll()

        def complete(e):
            for key in self.appbindings:
                self.master.unbind(key, self.appbindings[key])
            self.app.new_level()

        self.bindings = {'<ButtonRelease-3>': self.bind('<ButtonRelease-3>', complete)}
        self.appbindings = {'<Return>': self.master.bind('<Return>', complete)}

        self.show_succ_err()

        for line in self.lines:
            self.itemconfig(line, fill="green")
        self.itemconfig(self.sshape, fill="green")
        Thread(target=lambda: playsound("success.wav")).start()

    def not_win(self):

        self.show_succ_err()

        self.flash(5)
        self.master.after(1000, self.un_not_win)
        self.unbindAll()
        Thread(target=lambda: playsound("error.wav")).start()

    def flash(self, n):
        if n == 0:
            return

        if n % 2 == 0:
            for line in self.lines:
                self.itemconfig(line, fill="")
            self.itemconfig(self.sshape, fill="white")
        else:
            for line in self.lines:
                self.itemconfig(line, fill="red")
            self.itemconfig(self.sshape, fill="red")

        self.master.after(200, lambda: self.flash(n-1))

    def un_not_win(self):
        self.unshow_succ_err()

        for line in self.lines:
            self.itemconfig(line, fill="black")
        self.itemconfig(self.sshape, fill="black")
        self.line_draw_bindings()

    def start_bindings(self):
        self.bindings['<Button-1>'] = self.bind('<Button-1>', self.choose_start, add='+')

    def line_draw_bindings(self):
        self.bindings['<Button-1>'] = self.bind('<Button-1>', self.show_add_line, add='+')
        self.bindings['<ButtonRelease-1>'] = self.bind('<ButtonRelease-1>', self.update_to_visual, add='+')
        self.bindings['<B1-Motion>'] = self.bind('<B1-Motion>', self.show_add_line, add='+')

        self.bindings['<Button-3>'] = self.bind('<Button-3>', self.show_remove_line, add='+')
        self.bindings['<ButtonRelease-3>'] = self.bind('<ButtonRelease-3>', self.update_to_visual, add='+')
        self.bindings['<B3-Motion>'] = self.bind('<B3-Motion>', self.show_remove_line, add='+')
        self.bindings['<ButtonRelease-2>'] = self.bind('<ButtonRelease-2>', self.undo)
        self.bindings['<Double-Button-1>'] = self.bind('<Double-Button-1>', lambda e: self.win() if self.board.satisfied(self.visited, self.connections, self.cur, self.start) else self.not_win())

        self.appbindings['<Key>'] = self.master.bind('<Key>', self.change, add='+')

    def draw(self):
        self.delete(*self.lines)
        self.lines = []

        for segment in self.visual_connections:
            self.lines.append(self.create_line((segment[0][0] + 0.5) * 64, (segment[0][1] + 0.5) * 64,
                             (segment[1][0] + 0.5) * 64, (segment[1][1] + 0.5) * 64,
                             fill="black", width=3))

    def is_valid(self, *connections):
        for connection in connections:
            if connection not in self.board.connections and (connection[1], connection[0]) not in self.board.connections:
                return False
        return True

    def show_add_line(self, e):
        self.visual_connections = list(self.connections)

        for i in range(self.cur[0]+1, self.wr[0]) if e.x > (self.cur[0] + 0.5) * self.cell_size \
                else range(self.cur[0]-1, -1, -1):

            if (i, self.cur[1]) in self.visited:
                break

            if self.dist_real_to_coord((e.x, e.y), (i, self.cur[1])) < self.cell_size/2:
                new_conns = []
                if i < self.cur[0]:
                    for k in range(self.cur[0]-1, i-1, -1):
                        new_conns.append(((k + 1, self.cur[1]), (k, self.cur[1])))
                elif i > self.cur[0]:
                    for k in range(self.cur[0], i):
                        new_conns.append(((k, self.cur[1]), (k + 1, self.cur[1])))

                if self.is_valid(*new_conns):
                    self.visual_connections.extend(new_conns)
                    self.draw()
                else:
                    self.visual_connections = list(self.connections)
                return

        for j in range(self.cur[1]+1, self.wr[1]) if e.y > (self.cur[1] + 0.5) * self.cell_size \
                else range(self.cur[1]-1, -1, -1):

            if (self.cur[0], j) in self.visited:
                break

            if self.dist_real_to_coord((e.x, e.y), (self.cur[0], j)) < self.cell_size/2:
                new_conns = []
                if j < self.cur[1]:
                    for k in range(self.cur[1]-1, j-1, -1):
                        new_conns.append(((self.cur[0], k+1), (self.cur[0], k)))
                elif j > self.cur[1]:
                    for k in range(self.cur[1], j):
                        new_conns.append(((self.cur[0], k), (self.cur[0], k+1)))
                self.draw()

                if self.is_valid(*new_conns):
                    self.visual_connections.extend(new_conns)
                    self.draw()
                else:
                    self.visual_connections = list(self.connections)
                return

        self.draw()

    def update_to_visual(self, e):
        self.connections = self.visual_connections
        self.update_points()
        if tuple(self.connections) != tuple(self.connections_stack[-1]):
            self.connections_stack.append(tuple(self.connections))

    def update_points(self):
        if len(self.connections) != 0:
            self.visited = [conn[1] for conn in self.connections]
            self.visited.append(self.start)
            self.cur = self.connections[-1][1]
        else:
            self.cur = self.start
            self.visited = []

    def change(self, e):
        if e.keysym == "Up" or e.keysym == "w":
            if (self.cur[0], self.cur[1] - 1) not in self.visited and \
               self.is_valid(((self.cur[0], self.cur[1]), (self.cur[0], self.cur[1] - 1))):
                self.visual_connections.append(((self.cur[0], self.cur[1]), (self.cur[0], self.cur[1] - 1)))
            elif len(self.connections) != 0 and self.connections[-1] == \
                    ((self.cur[0], self.cur[1] - 1), (self.cur[0], self.cur[1])):
                self.visual_connections = self.connections[:-1]
        elif e.keysym == "Down" or e.keysym == "s":
            if (self.cur[0], self.cur[1] + 1) not in self.visited and \
               self.is_valid(((self.cur[0], self.cur[1]), (self.cur[0], self.cur[1] + 1))):
                self.visual_connections.append(((self.cur[0], self.cur[1]), (self.cur[0], self.cur[1] + 1)))
            elif len(self.connections) != 0 and self.connections[-1] == \
                    ((self.cur[0], self.cur[1] + 1), (self.cur[0], self.cur[1])):
                self.visual_connections = self.connections[:-1]
        elif e.keysym == "Left" or e.keysym == "a":
            if (self.cur[0] - 1, self.cur[1]) not in self.visited and self.cur[0] > 0 and \
               self.is_valid(((self.cur[0], self.cur[1]), (self.cur[0] - 1, self.cur[1]))):
                self.visual_connections.append(((self.cur[0], self.cur[1]), (self.cur[0] - 1, self.cur[1])))
            elif len(self.connections) != 0 and self.connections[-1] == \
                    ((self.cur[0] - 1, self.cur[1]), (self.cur[0], self.cur[1])):
                self.visual_connections = self.connections[:-1]
        elif e.keysym == "Right" or e.keysym == "d":
            if (self.cur[0] + 1, self.cur[1]) not in self.visited and self.cur[0] < self.wr[0]-1 and \
               self.is_valid(((self.cur[0], self.cur[1]), (self.cur[0] + 1, self.cur[1]))):
                self.visual_connections.append(((self.cur[0], self.cur[1]), (self.cur[0] + 1, self.cur[1])))
            elif len(self.connections) != 0 and self.connections[-1] == \
                    ((self.cur[0] + 1, self.cur[1]), (self.cur[0], self.cur[1])):
                self.visual_connections = self.connections[:-1]
        elif e.keysym == "space":
            self.visual_connections = []
        elif e.keysym == "BackSpace":
            self.undo(e)
        elif e.keysym == "Return":
            if self.board.satisfied(self.visited, self.connections, self.cur, self.start):
                self.win()
                return
            else:
                self.not_win()
                return
        elif e.keysym == "Escape" and len(self.board.starts) != 1:
            self.visual_connections = []
            self.visited = []
            self.connections = []
            self.connections_stack = [[]]
            self.itemconfigure(self.sshape, fill="")
            self.draw()
            self.unbindAll()
            self.start_bindings()
        else:
            print(e.keysym)

        self.draw()
        self.update_to_visual(None)

    def show_remove_line(self, e):
        self.visual_connections = list(self.connections)
        for i in range(len(self.connections)):
            if self.dist_real_to_coord((e.x, e.y), self.connections[i][0]) < self.cell_size/2:
                self.visual_connections = self.visual_connections[:i]
                break
        self.draw()

    def undo(self, e):
        if len(self.connections_stack) != 1:
            self.connections_stack.pop()
            self.connections = list(self.connections_stack[-1])
            self.visual_connections = self.connections
            self.draw()

        self.update_points()

    def dist_real_to_coord(self, coord1, coord2):
        return math.sqrt((coord1[0] - (coord2[0] + 0.5) * self.cell_size) ** 2 +
                         (coord1[1] - (coord2[1] + 0.5) * self.cell_size) ** 2)


def basic_domain(n, m):
    vertices = []
    edges = []
    cells = []
    for i in range(n):
        for j in range(m):
            vertices.append((i, j))
            if i != n-1:
                edges.append(((i, j), (i+1, j)))
            if j != m-1:
                edges.append(((i, j), (i, j+1)))
            if i != n-1 and j != m-1:
                cells.append((i, j))

    return vertices, edges, cells


def collect_vertices_from_edges(edges):
    vertices = set()
    for edge in edges:
        vertices.add(edge[0])
        vertices.add(edge[1])
    return vertices


def random_domain_path(n, m, path, likelihood=.9):
    edges = [*path]
    cells = []
    for i in range(n):
        for j in range(m):
            if i != n-1 and j != m-1:
                cells.append((i, j))
            if i != n-1:
                if random() <= likelihood and ((i, j), (i+1, j)) not in path:
                    edges.append(((i, j), (i+1, j)))
            if j != m-1:
                if random() <= likelihood and ((i, j), (i, j+1)) not in path:
                    edges.append(((i, j), (i, j+1)))

    return collect_vertices_from_edges(edges), edges, cells


def bounds(canvas, item):
    coords = canvas.bbox(item)
    bounds = coords[2] - coords[0], coords[3] - coords[1]
    return bounds


def play():
    root = tk.Tk()
    root.geometry("1000x800")
    app = GameApp(master=root)
    app.focus_set()
    app.new_level()
    app.mainloop()


def design():
    root = tk.Tk()
    root.geometry("1000x800")
    app = GameApp(master=root)
    app.focus_set()
    app.new_level()
    app.mainloop()


if __name__ == "__main__":
    design()
