import tkinter as tk

from PIL import ImageTk


class EditorView:
    def __init__(self, parent_widget, img_uploaded):
        self.parent_widget = parent_widget
        self.parent_widget.title('Editor View')
        self.parent_widget.geometry('720x720')

        self.img_to_cut = img_uploaded
        tk_img = ImageTk.PhotoImage(self.img_to_cut)
        self.img_label = tk.Label(self.parent_widget, image=tk_img)
        self.img_label.image = tk_img
        self.img_label.pack()
