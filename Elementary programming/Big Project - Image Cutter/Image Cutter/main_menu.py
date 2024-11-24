import tkinter as tk
from tkinter import filedialog as fd
from tkinter import ttk

from PIL import Image, ImageTk
from prompt_toolkit.output.win32 import BACKGROUND_COLOR

from editor_view import EditorView


class MainMenu:
    MAIN_MENU_GEOMETRY = '480x480'
    MAX_IMAGE_RESOLUTION = (100, 100)
    WINDOW_TITLE = 'Image Cutter'
    FILETYPES = (
        ('Image files', '*.png;*.jpg;*.jpeg'),
        ('All files', '*.*')
    )
    BACKGROUND_COLOR = '#2E2E2E'
    styles = {
        "bg": "#2E2E2E",  # Background color
        "fg": "#FFFFFF",  # Foreground color
        "font": ("Helvetica", 12),
    }

    def __init__(self, root):
        self.root = root
        self.root.title(self.WINDOW_TITLE)
        self.root.geometry(self.MAIN_MENU_GEOMETRY)

        # Styling, woo-hoo!
        self.root.config(bg = self.BACKGROUND_COLOR)
        self.load_custom_theme()

        self.uploaded_image = None
        self.path_to_image = None

        # initializing image label
        self.img_label = ttk.Label(self.root, background=self.BACKGROUND_COLOR)
        self.img_label.pack()
        self.img_label.image = None
        # initializing buttons
        self.editor_view_btn = ttk.Button(self.root, text="Editor View", command=self.open_editor_view)
        self.editor_view_btn.pack()
        self.upload_img_btn = ttk.Button(self.root, text="Upload Image", command=self.upload_image)
        self.upload_img_btn.pack()
        self.upload_params_btn = ttk.Button(self.root, text="Upload Params", command=self.upload_params)
        self.upload_params_btn.pack()

    def apply_styles(widget):
        widget.config(bg=styles["bg"], fg=styles["fg"], font=styles["font"])

    def load_custom_theme(self):
        import os
        theme_dir = r'C:\Users\Gleb\Documents\Uni\Uni Programming\Elementary programming\Big Project - Image Cutter\Image Cutter\TTK Themes'
        print(f"Loading custom theme from: {theme_dir}")

        if os.path.exists(theme_dir):
            self.root.tk.call('lappend', 'auto_path', theme_dir)
            try:
                # Adjusted call to ensure theme is loaded correctly
                self.root.tk.call('package', 'require', 'awthemes')  # Loading awthemes which is main
                self.root.tk.call('package', 'require', 'ttk::theme::awdark')  # Then load specific theme
                self.root.tk.call('package', 'require', 'awdark')  # Alternate method

                # Set the theme
                self.style = ttk.Style()
                self.style.theme_use('awdark')

                print("Theme loaded successfully.")
            except tk.TclError as e:
                print(f"Error loading theme: {e}")
        else:
            print(f"Theme directory {theme_dir} does not exist")

    def upload_image(self):
        # askopenfilename() returns path to the selected file - super convi)
        self.path_to_image = fd.askopenfilename(title='Select Image',
                                                initialdir='/',
                                                filetypes=self.FILETYPES)
        self.uploaded_image = Image.open(self.path_to_image)
        # Makes sure that the image occupies no more than X by Y pixels
        self.uploaded_image.thumbnail(self.MAX_IMAGE_RESOLUTION)
        img_tk = ImageTk.PhotoImage(self.uploaded_image)
        self.img_label.config(image=img_tk)
        # telling the garbage collector to back off
        self.img_label.image = img_tk

    def open_editor_view(self):
        if self.uploaded_image is not None:
            EditorView(tk.Toplevel(self.root), self.path_to_image)
        else:
            print("No image :(")

    def upload_params(self):
        print("...")
