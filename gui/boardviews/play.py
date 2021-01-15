from gui.app import *
from gui.boardviews.bulletin import RuleBulletin
from gameplay.constraints import *
from gui import controls
from gameplay.solver import Path


class PlayerCanvas(State):
    def __init__(self, board, app: GameApp):
        super().__init__(app.master, dim=(board.wid*app.cell_size, board.hei*app.cell_size))
        self.visual_connections = []
        self.connections_stack = [[]]
        self.board = board

        self.app = app
        self.lines = []
        self.board.draw(self)
        self.draw()
        self.bindings = []

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
        if len(self.board.constraints) > 0:
            self.rule_bulletin = RuleBulletin(app, self.board.constraints, board.hei)
            self.place(relx=0.25, rely=0.5, anchor=tk.CENTER)
            self.master.minsize((board.wid + 1)*app.cell_size + 500, (board.hei + 1)*app.cell_size)
        else:
            self.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
            self.rule_bulletin = None
            self.master.minsize((board.wid + 1)*app.cell_size, (board.hei + 1)*app.cell_size)

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
                sound("res/softdot.wav")
                break

    def unbindAll(self):
        for binding in self.bindings:
            binding.unbind()
        self.bindings = []

    def show_succ_err(self):
        errcls = set()
        succls = set()
        for rule in self.board.constraints:
            if rule.is_satisfied(self.board, self.path):
                rule.success(self)
                if isinstance(rule, TextConstraint) and rule not in errcls:
                    succls.add(rule)
                elif type(rule) not in errcls:
                    succls.add(type(rule))
            else:
                rule.error(self)
                if isinstance(rule, TextConstraint):
                    errcls.add(rule)
                else:
                    errcls.add(type(rule))
                    if type(rule) in succls:
                        succls.remove(type(rule))

        for cl in errcls:
            self.rule_bulletin.error(cl)
        for cl in succls:
            self.rule_bulletin.success(cl)

    def unshow_succ_err(self):
        cls = set()
        for rule in self.board.constraints:
            rule.normal(self)
            if isinstance(rule, TextConstraint):
                cls.add(rule)
            else:
                cls.add(type(rule))

        for cl in cls:
            self.rule_bulletin.normal(cl)

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
        sound("res/softsuccess.wav")

    def not_win(self):
        self.show_succ_err()

        self.flash(5)
        self.master.after(1000, self.un_not_win)
        self.unbindAll()
        sound("res/softerror.wav")

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
        for binding in controls.START:
            binding.bind(self.choose_start, self)
            self.bindings.append(binding)

    def line_draw_bindings(self):
        for binding in controls.FORWARD_VIS:
            binding.bind(self.show_add_line, self)
            self.bindings.append(binding)
        for binding in controls.UPDATE:
            binding.bind(self.update_to_visual, self)
            self.bindings.append(binding)
        for binding in controls.BACKWARD_VIS:
            binding.bind(self.show_remove_line, self)
            self.bindings.append(binding)
        for binding in controls.UNDO:
            binding.bind(self.undo, self)
            self.bindings.append(binding)
        for binding in controls.UP:
            binding.bind(self.up, self)
            self.bindings.append(binding)
        for binding in controls.DOWN:
            binding.bind(self.down, self)
            self.bindings.append(binding)
        for binding in controls.LEFT:
            binding.bind(self.left, self)
            self.bindings.append(binding)
        for binding in controls.RIGHT:
            binding.bind(self.right, self)
            self.bindings.append(binding)
        for binding in controls.COMPLETE:
            binding.bind(self.complete, self)
            self.bindings.append(binding)
        for binding in controls.CLEAR:
            binding.bind(self.clear, self)
            self.bindings.append(binding)

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

        for i in range(self.path.cur[0]+1, self.board.wid) if e.x > (self.path.cur[0] + 0.5) * self.app.cell_size \
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

        for j in range(self.path.cur[1]+1, self.board.hei) if e.y > (self.path.cur[1] + 0.5) * self.app.cell_size \
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
            self.connections_stack.append(tuple(self.path.connections))

    def update_points(self):
        if len(self.path.connections) != 0:
            self.path.visited = [conn[1] for conn in self.path.connections]
            self.path.visited.append(self.path.start)
            self.path.cur = self.path.connections[-1][1]
        else:
            self.path.cur = self.path.start
            self.path.visited = []

    def up(self, e):
        if (self.path.cur[0], self.path.cur[1] - 1) not in self.path.visited and \
                self.is_valid(((self.path.cur[0], self.path.cur[1]), (self.path.cur[0], self.path.cur[1] - 1))):
            self.visual_connections.append(
                ((self.path.cur[0], self.path.cur[1]), (self.path.cur[0], self.path.cur[1] - 1)))
        elif len(self.path.connections) != 0 and same_edge(self.path.connections[-1],
                ((self.path.cur[0], self.path.cur[1] - 1), (self.path.cur[0], self.path.cur[1]))):
            self.visual_connections = self.path.connections[:-1]
        self.draw()
        self.update_to_visual(None)

    def down(self, e):
        if (self.path.cur[0], self.path.cur[1] + 1) not in self.path.visited and \
                self.is_valid(((self.path.cur[0], self.path.cur[1]), (self.path.cur[0], self.path.cur[1] + 1))):
            self.visual_connections.append(
                ((self.path.cur[0], self.path.cur[1]), (self.path.cur[0], self.path.cur[1] + 1)))
        elif len(self.path.connections) != 0 and same_edge(self.path.connections[-1],
                ((self.path.cur[0], self.path.cur[1] + 1), (self.path.cur[0], self.path.cur[1]))):
            self.visual_connections = self.path.connections[:-1]
        self.draw()
        self.update_to_visual(None)

    def left(self, e):
        if (self.path.cur[0] - 1, self.path.cur[1]) not in self.path.visited and self.path.cur[0] > 0 and \
                self.is_valid(((self.path.cur[0], self.path.cur[1]), (self.path.cur[0] - 1, self.path.cur[1]))):
            self.visual_connections.append(
                ((self.path.cur[0], self.path.cur[1]), (self.path.cur[0] - 1, self.path.cur[1])))
        elif len(self.path.connections) != 0 and same_edge(self.path.connections[-1],
                ((self.path.cur[0] - 1, self.path.cur[1]), (self.path.cur[0], self.path.cur[1]))):
            self.visual_connections = self.path.connections[:-1]
        self.draw()
        self.update_to_visual(None)

    def right(self, e):
        if (self.path.cur[0] + 1, self.path.cur[1]) not in self.path.visited and self.path.cur[0] < self.board.wid - 1 and \
                self.is_valid(((self.path.cur[0], self.path.cur[1]), (self.path.cur[0] + 1, self.path.cur[1]))):
            self.visual_connections.append(
                ((self.path.cur[0], self.path.cur[1]), (self.path.cur[0] + 1, self.path.cur[1])))
        elif len(self.path.connections) != 0 and same_edge(self.path.connections[-1],
                ((self.path.cur[0] + 1, self.path.cur[1]), (self.path.cur[0], self.path.cur[1]))):
            self.visual_connections = self.path.connections[:-1]
        self.draw()
        self.update_to_visual(None)

    def clear(self, e):
        if len(self.board.starts) != 1:
            self.path.visited = []
            self.path.connections = []
            self.connections_stack = [[]]
            self.itemconfigure(self.sshape, fill="")
            self.draw()
            self.unbindAll()
            self.start_bindings()
            sound("res/softundot.wav")
        self.visual_connections = []
        self.draw()
        self.update_to_visual(None)

    def complete(self, e):
        if self.board.is_satisfied(self.path):
            self.win()
            return
        else:
            self.not_win()
            return

    def show_remove_line(self, e):
        self.visual_connections = list(self.path.connections)
        for i in range(len(self.path.connections)):
            if dist_real_to_coord((e.x, e.y), self.path.connections[i][0]) < self.app.cell_size/2:
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
