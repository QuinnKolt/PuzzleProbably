from playsound import playsound

from main import *
from bulletin import RuleBulletin

class PlayerCanvas(tk.Canvas):
    def __init__(self, board, wr, app: GameApp):
        super().__init__(app.master, width=wr[0]*app.cell_size, height=wr[1]*app.cell_size)
        self.visual_connections = []
        self.connections_stack = [[]]
        self.board = board

        self.app = app
        self.wr = wr
        self.lines = []
        self.board.draw(self)
        self.draw()
        self.bindings = {}
        self.appbindings = {}
        self.rule_board = RuleBulletin(app, self.board.rules)

        if len(self.board.starts) == 1:
            start = self.board.starts[0]
            self.line_draw_bindings()
            self.sshape = self.create_oval((start[0] + 0.5)*64 - 5, (start[1] + 0.5)*64 - 5,
                                           (start[0] + 0.5)*64 + 5, (start[1] + 0.5)*64 + 5,
                                           fill="black", outline="black")
        else:
            start = None
            self.start_bindings()
        self.path = Path([], [start], start, start)
        self.master.minsize((wr[0] + 1)*app.cell_size+500, (wr[1] + 1)*app.cell_size)
        self.place(relx=0.25, rely=0.5, anchor=tk.CENTER)

    def choose_start(self, e):
        for s in self.board.starts:
            if dist_real_to_coord((e.x, e.y), s) < self.app.cell_size/2:
                self.path.start = s
                self.path.cur = self.path.start
                self.unbindAll()
                self.sshape = self.create_oval((self.path.start[0] + 0.5)*64 - 5, (self.path.start[1] + 0.5)*64 - 5,
                                               (self.path.start[0] + 0.5)*64 + 5, (self.path.start[1] + 0.5)*64 + 5,
                                               fill="black", outline="black")
                self.line_draw_bindings()
                Thread(target=lambda: playsound("res/start.wav")).start()
                break

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
            if rule.is_satisfied(self.board, self.path):
                rule.success(self)
                succls.add(type(rule))
            else:
                rule.error(self)
                errcls.add(type(rule))
                if type(rule) in succls:
                    succls.remove(type(rule))

        for cl in errcls:
            self.rule_board.error(cl)
        for cl in succls:
            self.rule_board.success(cl)

    def unshow_succ_err(self):
        cls = set()
        for rule in self.board.rules:
            rule.normal(self)
            cls.add(type(rule))

        for cl in cls:
            self.rule_board.normal(cl)

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
        Thread(target=lambda: playsound("res/success.wav")).start()

    def not_win(self):

        self.show_succ_err()

        self.flash(5)
        self.master.after(1000, self.un_not_win)
        self.unbindAll()
        Thread(target=lambda: playsound("res/error.wav")).start()

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
        self.bindings['<Double-Button-1>'] = self.bind('<Double-Button-1>', lambda e: self.win()
                                                       if self.board.is_satisfied(self.path) else self.not_win())

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
            if connection not in self.board.edges and (connection[1], connection[0]) not in self.board.edges:
                return False
        return True

    def show_add_line(self, e):
        self.visual_connections = list(self.path.connections)

        for i in range(self.path.cur[0]+1, self.wr[0]) if e.x > (self.path.cur[0] + 0.5) * self.app.cell_size \
                else range(self.path.cur[0]-1, -1, -1):

            if (i, self.path.cur[1]) in self.path.visited:
                break

            if dist_real_to_coord((e.x, e.y), (i, self.path.cur[1])) < self.app.cell_size/2:
                new_conns = []
                if i < self.path.cur[0]:
                    for k in range(self.path.cur[0]-1, i-1, -1):
                        new_conns.append(((k + 1, self.path.cur[1]), (k, self.path.cur[1])))
                elif i > self.path.cur[0]:
                    for k in range(self.path.cur[0], i):
                        new_conns.append(((k, self.path.cur[1]), (k + 1, self.path.cur[1])))

                if self.is_valid(*new_conns):
                    self.visual_connections.extend(new_conns)
                    self.draw()
                else:
                    self.visual_connections = list(self.path.connections)
                return

        for j in range(self.path.cur[1]+1, self.wr[1]) if e.y > (self.path.cur[1] + 0.5) * self.app.cell_size \
                else range(self.path.cur[1]-1, -1, -1):

            if (self.path.cur[0], j) in self.path.visited:
                break

            if dist_real_to_coord((e.x, e.y), (self.path.cur[0], j)) < self.app.cell_size/2:
                new_conns = []
                if j < self.path.cur[1]:
                    for k in range(self.path.cur[1]-1, j-1, -1):
                        new_conns.append(((self.path.cur[0], k+1), (self.path.cur[0], k)))
                elif j > self.path.cur[1]:
                    for k in range(self.path.cur[1], j):
                        new_conns.append(((self.path.cur[0], k), (self.path.cur[0], k+1)))
                self.draw()

                if self.is_valid(*new_conns):
                    self.visual_connections.extend(new_conns)
                    self.draw()
                else:
                    self.visual_connections = list(self.path.connections)
                return

        self.draw()

    def update_to_visual(self, e):
        self.path.connections = self.visual_connections
        self.update_points()
        if tuple(self.path.connections) != tuple(self.connections_stack[-1]):
            self.connections_stack.append(list(self.path.connections))

    def update_points(self):
        if len(self.path.connections) != 0:
            self.path.visited = [conn[1] for conn in self.path.connections]
            self.path.visited.append(self.path.start)
            self.path.cur = self.path.connections[-1][1]
        else:
            self.path.cur = self.path.start
            self.path.visited = []

    def change(self, e):
        if e.keysym == "Up" or e.keysym == "w":
            if (self.path.cur[0], self.path.cur[1] - 1) not in self.path.visited and \
               self.is_valid(((self.path.cur[0], self.path.cur[1]), (self.path.cur[0], self.path.cur[1] - 1))):
                self.visual_connections.append(((self.path.cur[0], self.path.cur[1]), (self.path.cur[0], self.path.cur[1] - 1)))
            elif len(self.path.connections) != 0 and self.path.connections[-1] == \
                    ((self.path.cur[0], self.path.cur[1] - 1), (self.path.cur[0], self.path.cur[1])):
                self.visual_connections = self.path.connections[:-1]
        elif e.keysym == "Down" or e.keysym == "s":
            if (self.path.cur[0], self.path.cur[1] + 1) not in self.path.visited and \
               self.is_valid(((self.path.cur[0], self.path.cur[1]), (self.path.cur[0], self.path.cur[1] + 1))):
                self.visual_connections.append(((self.path.cur[0], self.path.cur[1]), (self.path.cur[0], self.path.cur[1] + 1)))
            elif len(self.path.connections) != 0 and self.path.connections[-1] == \
                    ((self.path.cur[0], self.path.cur[1] + 1), (self.path.cur[0], self.path.cur[1])):
                self.visual_connections = self.path.connections[:-1]
        elif e.keysym == "Left" or e.keysym == "a":
            if (self.path.cur[0] - 1, self.path.cur[1]) not in self.path.visited and self.path.cur[0] > 0 and \
               self.is_valid(((self.path.cur[0], self.path.cur[1]), (self.path.cur[0] - 1, self.path.cur[1]))):
                self.visual_connections.append(((self.path.cur[0], self.path.cur[1]), (self.path.cur[0] - 1, self.path.cur[1])))
            elif len(self.path.connections) != 0 and self.path.connections[-1] == \
                    ((self.path.cur[0] - 1, self.path.cur[1]), (self.path.cur[0], self.path.cur[1])):
                self.visual_connections = self.path.connections[:-1]
        elif e.keysym == "Right" or e.keysym == "d":
            if (self.path.cur[0] + 1, self.path.cur[1]) not in self.path.visited and self.path.cur[0] < self.wr[0]-1 and \
               self.is_valid(((self.path.cur[0], self.path.cur[1]), (self.path.cur[0] + 1, self.path.cur[1]))):
                self.visual_connections.append(((self.path.cur[0], self.path.cur[1]), (self.path.cur[0] + 1, self.path.cur[1])))
            elif len(self.path.connections) != 0 and self.path.connections[-1] == \
                    ((self.path.cur[0] + 1, self.path.cur[1]), (self.path.cur[0], self.path.cur[1])):
                self.visual_connections = self.path.connections[:-1]
        elif e.keysym == "space":
            self.visual_connections = []
        elif e.keysym == "BackSpace":
            self.undo(e)
        elif e.keysym == "Return":
            if self.board.is_satisfied(self.path):
                self.win()
                return
            else:
                self.not_win()
                return
        elif e.keysym == "Escape" and len(self.board.starts) != 1:
            self.visual_connections = []
            self.path.visited = []
            self.path.connections = []
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
        self.visual_connections = list(self.path.connections)
        for i in range(len(self.path.connections)):
            if dist_real_to_coord((e.x, e.y), self.path.connections[i][0]) < CELL/2:
                self.visual_connections = self.visual_connections[:i]
                break
        self.draw()

    def undo(self, e):
        if len(self.connections_stack) != 1:
            self.connections_stack.pop()
            self.path.connections = list(self.connections_stack[-1])
            self.visual_connections = self.path.connections
            self.draw()

        self.update_points()
