import tkinter as tk

from main_menu import MainMenu

# TODO:
#   MBY: Move rect by arrows + shift thing --> actually in the assignment!!!
#   MBY: Choose grid color
#   MBY: Upload params for editor view button
#   MBY: add scaling for bigger images, taking that into account when drawing grid
#   MBY: document the whole thing properly with comments and docstrings

root = tk.Tk()
app = MainMenu(root)
root.mainloop()
