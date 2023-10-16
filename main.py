import tkinter as tk
from Interface.gui import Application

if __name__ == '__main__':
    root = tk.Tk()
    app = Application(root)
    root.resizable(0, 0)
    root.mainloop()