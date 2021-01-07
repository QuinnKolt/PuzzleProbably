class LevelScreen(tk.Canvas):
    def __init__(self, app, levels):
        super().__init__(app.master, width=800, height=800)
        for binding in controls.SELECT:
            binding.bind(lambda e: app.new_board(level.board), app.master)

        self.levels = levels

        self.create_text(200, 200, fill="darkblue", font="Courier 20 bold", text="Level " + str(self.level.num))
        self.create_text(200, 300, fill="black", font="Helvetica 12", text=self.level.hint)

        self.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.master.minsize(850, 850)
