import tkinter as tk

from main_menu import MainMenu

# TODO:
#   clear canvas before drawing new grid
#   take into account filetype when saving the cut image
#   implement uploading params
#   implement automatic cutting with uploaded params
#   MBY: redrawing grid when params change
#   MBY: dragging grid using mouse
#   MBY: improve ui (yeah, good luck)
#   document the whole thing properly with comments and docstrings


root = tk.Tk()
app = MainMenu(root)
root.mainloop()
