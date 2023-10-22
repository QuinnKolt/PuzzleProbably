from main import *


class RuleBulletin(tk.Canvas):
    def __init__(self, app: GameApp, rules):
        super().__init__(app.master, width=500, height=75 + 40*len(rules))

        if rules is not None:
            self.rule_texts = {}
            for rule in rules:
                self.rule_texts[type(rule)] = rule.bulletin()
        else:
            self.rule_texts = dict()
        self.rule_shapes = dict()
        self.first = True
        self.draw()
        self.place(relx=0.75, rely=0.5, anchor=tk.CENTER)

    def __set__(self, instance, value):
        self.rule_texts[instance] = value

    def draw(self):
        self.delete("all")

        dep = 30
        keys = self.rule_texts.keys()
        # list texts first
        texts = list(cl for cl in keys if issubclass(cl, TextRule))
        nontexts = list(cl for cl in keys if not issubclass(cl, TextRule))
        keys = (*texts, *nontexts)

        for cl in keys:
            if issubclass(cl, TextRule):
                self.rule_shapes[cl] = self.create_text(25, dep, text=self.rule_texts[cl],
                                                        width=400, anchor=tk.NW, font="Helvetica 12 bold")
            else:
                self.rule_shapes[cl] = self.create_text(25, dep, text=self.rule_texts[cl],
                                                        width=400, anchor=tk.NW, font="Helvetica 10")
            b = bounds(self, self.rule_shapes[cl])
            dep += b[1] + 15

        if self.first:
            self.lower(self.create_rectangle(5, 5, 445, dep+15, fill="gray92", outline="dim gray"))
            self.config(height=dep+15)
            self.first = False

    def success(self, cl):
        self.itemconfig(self.rule_shapes[cl], fill="green")

    def error(self, cl):
        self.itemconfig(self.rule_shapes[cl], fill="red")

    def normal(self, cl):
        self.itemconfig(self.rule_shapes[cl], fill="black")
