


class Binding:
    def __init__(self, str):
        self.str = str
        self.state = None
        self.bound = None

    def bind(self, func, state):
        self.state = state

    def unbind(self):
        pass


class MouseBinding(Binding):
    def __init__(self, str):
        super().__init__(str)

    def bind(self, func, state):
        self.state = state
        self.bound = self.state.bind(self.str, func, add='+')

    def unbind(self):
        self.state.unbind(self.str, self.bound)


class KeyBinding(Binding):
    def __init__(self, str):
        super().__init__(str)

    def bind(self, func, state):
        self.state = state
        self.bound = self.state.app.master.bind("<Key>", lambda e: func(e) if e.keysym == self.str else None, add='+')

    def unbind(self):
        self.state.app.master.unbind("<Key>", self.bound)


class MasterKeyBinding(Binding):
    def __init__(self, str):
        super().__init__(str)

    def bind(self, func, state):
        self.state = state
        self.bound = self.state.bind("<Key>", lambda e: func(e) if e.keysym == self.str else None, add='+')

    def unbind(self):
        self.state.unbind("<Key>", self.bound)


UP = {KeyBinding("Up"), KeyBinding("w")}
LEFT = {KeyBinding("Left"), KeyBinding("a")}
DOWN = {KeyBinding("Down"), KeyBinding("s")}
RIGHT = {KeyBinding("Right"), KeyBinding("d")}
COMPLETE = {KeyBinding("Return"), MouseBinding('<Double-Button-1>')}
CLEAR = {KeyBinding("space"), KeyBinding("Escape")}
UNDO = {KeyBinding("BackSpace"), MouseBinding('<ButtonRelease-2>')}

FORWARD_VIS = {MouseBinding('<Button-1>'), MouseBinding('<B1-Motion>')}
BACKWARD_VIS = {MouseBinding('<Button-3>'), MouseBinding('<B3-Motion>')}
UPDATE = {MouseBinding('<ButtonRelease-1>'), MouseBinding('<ButtonRelease-3>')}
START = {MouseBinding('<Button-1>')}

SELECT = {MouseBinding('<ButtonRelease-3>'), MasterKeyBinding("Return")}
