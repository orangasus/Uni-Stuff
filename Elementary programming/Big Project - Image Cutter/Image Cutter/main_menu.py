import tkinter as tk
from tkinter import filedialog as fd
from PIL import Image, ImageTk

from editor_view import EditorView


class MainMenu:
    def __init__(self, root):
        self.root = root
        self.root.title('Image Cutter')
        self.root.geometry('480x720')
        self.uploaded_image = None

        # initializing image label
        self.img_label = tk.Label(self.root)
        self.img_label.pack()
        self.img_label.image = None
        # initializing buttons
        self.editor_view_btn = tk.Button(self.root, text="Editor View", command=self.open_editor_view)
        self.editor_view_btn.pack()
        self.upload_img_btn = tk.Button(self.root, text="Upload Image", command=self.upload_image)
        self.upload_img_btn.pack()
        self.upload_params_btn = tk.Button(self.root, text="Upload Params", command=self.upload_params)
        self.upload_params_btn.pack()
        # defining file types that program accepts
        self.filetypes = (
            ('Image files', '*.png;*.jpg;*.jpeg'),
            ('All files', '*.*')
        )

    def upload_image(self):
        # askopenfilename() returns path to the selected file - super convi)
        file_to_open = fd.askopenfilename(title='Select Image',
                                                     initialdir='/',
                                                     filetypes=self.filetypes)
        self.uploaded_image = Image.open(file_to_open)
        img_tk = ImageTk.PhotoImage(self.uploaded_image)
        self.img_label.config(image=img_tk)
        # telling the garbage collector to back off
        self.img_label.image = img_tk

    def open_editor_view(self):
        if self.uploaded_image is not None:
            EditorView(tk.Toplevel(self.root), self.uploaded_image)
        else:
            print("No image :(")

    def upload_params(self):
        print("...")
