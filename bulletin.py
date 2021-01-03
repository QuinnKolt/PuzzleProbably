from main import *


class RuleBulletin(tk.Canvas):
    def __init__(self, app: GameApp, rules):
        super().__init__(app.master, width=500, height=75 + 40*len(rules))

        if rules is not None:
            self.rule_texts = {rule: rule.text for rule in rules if isinstance(rule, TextRule)}
            self.rule_texts.update(
                {type(rule): CLASS_RULES[type(rule)] for rule in rules if not isinstance(rule, TextRule)})
        else:
            self.rule_texts = dict()
        self.rule_shapes = dict()
        self.draw()
        self.place(relx=0.75, rely=0.5, anchor=tk.CENTER)

    def __set__(self, instance, value):
        self.rule_texts[instance] = value

    def draw(self):
        self.delete("all")

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
