import tkinter as tk

from main_menu import MainMenu

# TODO:
#   ---
#   MBY: Choose grid color
#   MBY: add scaling for bigger images, taking that into account when drawing grid
#   MBY: document the whole thing properly with comments and docstrings

root = tk.Tk()
app = MainMenu(root)
root.mainloop()
