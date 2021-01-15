from gui.app import *


def main():
    root = tk.Tk()
    root.geometry("1000x800")
    app = GameApp(master=root)
    app.focus_set()
    app.new_level()
    app.mainloop()


if __name__ == "__main__":
    main()
