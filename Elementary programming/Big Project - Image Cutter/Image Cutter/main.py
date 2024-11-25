import tkinter as tk

from main_menu import MainMenu

# TODO:
#   MBY: dragging grid using mouse
#   MBY: add scaling for bigger images, taking that into account when drawing grid
#   MBY: document the whole thing properly with comments and docstrings


root = tk.Tk()
app = MainMenu(root)
root.mainloop()
