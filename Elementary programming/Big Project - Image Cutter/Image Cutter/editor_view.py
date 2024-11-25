import json
import tkinter as tk
from tkinter import filedialog
# so apparently first line imports only main tkinter module, which doesn't include some other features
from tkinter import messagebox
from tkinter import ttk
from PIL import ImageTk, Image
import cutting_module
import styling_module


class EditorView:
    WINDOW_GEOMETRY = '700x700'
    # Probably would be a good idea to resize the image for it to fit,
    # but then I would also need to keep in mind the ratio to draw the grid accordingly
    MAX_IMAGE_RESOLUTION = (700, 700)
    WINDOW_TITLE = 'Editor View'
    PARAMETERS_NAME = ['num_horiz_rect', 'num_vert_rect', 'rect_width', 'rect_height', 'rect_horiz_dist',
                       'rect_vert_dist', 'top_left_rect_x', 'top_left_rect_y']
    FILETYPES = [('All Files', '*.*'),
                 ('JSON', '*.json')]

    def __init__(self, parent_widget, path_to_image):
        self.parent_widget = parent_widget
        self.parent_widget.title(self.WINDOW_TITLE)
        self.parent_widget.geometry(self.WINDOW_GEOMETRY)
        self.parent_widget.resizable(False, False)

        self.parent_widget.config(bg=styling_module.BACKGROUND_DARK_GRAY)

        # creating a dict with pair name of parameter : reference to the entry object
        self.entries_reference_dict = {name: tk.StringVar() for name in self.PARAMETERS_NAME}
        self.entries_widgets = []

        # dict with param_name : integer value for cutting grid params
        self.cutting_grid_params = None

        self.create_grid_for_layout()

        self.img_to_cut = Image.open(path_to_image)
        self.tk_img = ImageTk.PhotoImage(self.img_to_cut)
        self.image_canvas = tk.Canvas(self.parent_widget, bg=styling_module.BACKGROUND_SOFT_BLACK)

        self.cut_button = ttk.Button(self.parent_widget, text='CUT', command=self.cut_btn_clicked)
        self.save_params_button = ttk.Button(self.parent_widget, text='SAVE PARAMS', command=self.save_params_clicked)

        self.create_layout()

        self.parent_widget.after(100, self.center_image_on_canvas)

    def create_layout(self):
        cur_label_row, cur_label_col = 0, 0
        cur_entry_row, cur_entry_col = 1, 0
        for ind, param_name in enumerate(self.PARAMETERS_NAME):
            cur_entry_label = ttk.Label(self.parent_widget, text=param_name.replace('_', ' '))
            cur_entry_label.grid(row=cur_label_row, column=cur_label_col + 1)

            cur_entry = ttk.Entry(self.parent_widget, textvariable=self.entries_reference_dict[param_name])
            cur_entry.bind('<KeyRelease>', self.on_entry_change)
            cur_entry.grid(row=cur_entry_row, column=cur_entry_col + 1)
            self.entries_widgets.append(cur_entry)

            # switch row if last column
            if ind % 2 != 0:
                cur_label_row += 2
                cur_entry_row += 2

            cur_label_col = (cur_label_col + 1) % 2
            cur_entry_col = (cur_entry_col + 1) % 2

        self.cut_button.grid(row=8, column=1, columnspan=2)
        self.save_params_button.grid(row=9, column=1, columnspan=2)
        self.image_canvas.grid(row=0, column=0, rowspan=11, sticky='news')

    def create_grid_for_layout(self):
        self.parent_widget.columnconfigure(1, weight=0)
        self.parent_widget.columnconfigure(2, weight=0)
        self.parent_widget.columnconfigure(0, weight=1)

        for i in range(9):
            self.parent_widget.rowconfigure(i, weight=0)
        self.parent_widget.rowconfigure(10, weight=1)

    def check_that_all_entries_non_empty(self):
        for entry in self.entries_widgets:
            if entry.get() == "":
                return False
        return True

    def on_entry_change(self, event=None):
        if self.check_that_all_entries_non_empty():
            try:
                self.cutting_grid_params = {key: int(val.get()) for key, val in self.entries_reference_dict.items()}
                self.draw_cutting_grid_on_canvas()
            except Exception as e:
                print(f"Couldn't draw the grid:\n{e}")

    def save_params_clicked(self):
        if self.check_if_all_params_int():
            # guess i rly learned sth :)
            json_filename = tk.filedialog.asksaveasfilename(filetypes=self.FILETYPES, defaultextension='.json')
            self.cutting_grid_params = {key: int(val.get()) for key, val in self.entries_reference_dict.items()}
            with open(json_filename, 'w') as params_file:
                params_file.write(json.dumps(self.cutting_grid_params))

    def check_if_all_params_int(self):
        for key, val in self.entries_reference_dict.items():
            if val == '' or not val.get().isnumeric():
                tk.messagebox.showinfo("Invalid Input",
                                       "All entries should be positive numbers and non-empty")
                return False
            return True

    def cut_btn_clicked(self):
        self.cutting_grid_params = {key: int(val.get()) for key, val in self.entries_reference_dict.items()}
        self.draw_cutting_grid_on_canvas()
        saving_dir = filedialog.askdirectory(title='Select folder to save cut images')
        if not saving_dir:
            tk.messagebox.showinfo('Error', 'No folder selected')
        else:
            cutting_module.perform_cuts(self.img_to_cut.width, self.img_to_cut.height,
                                        saving_dir, self.img_to_cut, self.cutting_grid_params,
                                        self.image_canvas.winfo_width(), self.image_canvas.winfo_height())

    def center_image_on_canvas(self):
        canv_width = self.image_canvas.winfo_width()
        canv_height = self.image_canvas.winfo_height()

        x_center = canv_width // 2
        y_center = canv_height // 2

        self.image_canvas.create_image(x_center, y_center,
                                       anchor=tk.CENTER, image=self.tk_img)
        self.image_canvas.image = self.tk_img

    def draw_rectangle_on_canvas(self, x0, y0):
        self.image_canvas.create_rectangle(x0, y0, x0 + self.cutting_grid_params['rect_width'],
                                           y0 + self.cutting_grid_params['rect_height'], tags='rect')

    def draw_cutting_grid_on_canvas(self):
        if cutting_module.check_if_cutting_grid_fits(self.img_to_cut.width, self.img_to_cut.height,
                                                     self.cutting_grid_params):
            self.image_canvas.delete('rect')
            for el in cutting_module.get_coords_of_all_rect(self.img_to_cut.width, self.img_to_cut.height,
                                                            self.image_canvas.winfo_width(), self.image_canvas.winfo_height(),
                                                            self.cutting_grid_params):
                self.draw_rectangle_on_canvas(el[0], el[1])
        else:
            tk.messagebox.showinfo("Invalid Input", 'Cutting Grid doesn\'t fit')