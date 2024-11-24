import json
import tkinter as tk
from tkinter import filedialog
# so apparently first line imports only main tkinter module, which doesn't include some other features
from tkinter import messagebox
from tkinter import ttk
from PIL import ImageTk, Image


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

        # creating a dict with pair name of parameter : reference to the entry object
        self.entries_reference_dict = {name: tk.StringVar() for name in self.PARAMETERS_NAME}

        # dict with param_name : integer value for cutting grid params
        self.cutting_grid_params = None

        self.create_grid_for_layout()

        self.img_to_cut = Image.open(path_to_image)
        self.tk_img = ImageTk.PhotoImage(self.img_to_cut)
        self.image_canvas = tk.Canvas(self.parent_widget, bg='lightgrey')

        self.cut_button = ttk.Button(self.parent_widget, text='CUT', command=self.cut_btn_clicked)
        self.save_params_button = ttk.Button(self.parent_widget, text='SAVE PARAMS', command=self.save_params_clicked)

        self.create_layout()

        self.parent_widget.after(100, self.center_image_on_canvas)

    def create_layout(self):
        cur_label_row, cur_label_col = 0, 0
        cur_entry_row, cur_entry_col = 1, 0
        for ind, param_name in enumerate(self.PARAMETERS_NAME):
            cur_entry_label = tk.Label(self.parent_widget, text=param_name.replace('_', ' '))
            cur_entry_label.grid(row=cur_label_row, column=cur_label_col + 1)

            cur_entry = ttk.Entry(self.parent_widget, textvariable=self.entries_reference_dict[param_name])
            cur_entry.grid(row=cur_entry_row, column=cur_entry_col + 1)

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
            self.perform_cuts(saving_dir)

    def get_coords_of_all_rect(self):
        coords = []
        img_width, img_height = self.img_to_cut.size
        canv_width = self.image_canvas.winfo_width()
        canv_height = self.image_canvas.winfo_height()

        # Adjusting origin point to be in the top left corner of the image, not canvas
        origin_x = (canv_width - img_width) // 2
        origin_y = (canv_height - img_height) // 2
        cur_x = self.cutting_grid_params['top_left_rect_x'] + origin_x
        cur_y = self.cutting_grid_params['top_left_rect_y'] + origin_y

        for i in range(self.cutting_grid_params['num_vert_rect']):
            for j in range(self.cutting_grid_params['num_horiz_rect']):
                print(f"Rectangle {i * self.cutting_grid_params['num_horiz_rect'] + j + 1}: (x={cur_x}, y={cur_y})")
                coords.append((cur_x, cur_y))
                cur_x += self.cutting_grid_params['rect_width'] + self.cutting_grid_params['rect_horiz_dist']
            cur_x = self.cutting_grid_params['top_left_rect_x'] + origin_x
            cur_y += self.cutting_grid_params['rect_height'] + self.cutting_grid_params['rect_vert_dist']

        return coords

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
                                           y0 + self.cutting_grid_params['rect_height'])

    def draw_cutting_grid_on_canvas(self):
        if self.check_if_cutting_grid_fits():
            for el in self.get_coords_of_all_rect():
                self.draw_rectangle_on_canvas(el[0], el[1])
        else:
            tk.messagebox.showinfo("Invalid Input", 'Cutting Grid doesn\'t fit')

    def check_if_cutting_grid_fits(self):
        x0, y0 = self.cutting_grid_params['top_left_rect_x'], self.cutting_grid_params['top_left_rect_y']
        xn = (x0 + (self.cutting_grid_params['num_vert_rect'] - 1) * self.cutting_grid_params['rect_vert_dist']
              + self.cutting_grid_params['num_vert_rect'] * self.cutting_grid_params['rect_height'])
        yn = (y0 + (self.cutting_grid_params['num_horiz_rect'] - 1) * self.cutting_grid_params['rect_horiz_dist']
              + self.cutting_grid_params['num_horiz_rect'] * self.cutting_grid_params['rect_width'])
        img_width, img_height = self.img_to_cut.size
        return (x0 <= xn <= img_width) and (y0 <= yn <= img_height)

    def convert_representation(self, x0, y0):
        x_left_edge = x0
        x_right_edge = x0 + self.cutting_grid_params['rect_width']
        y_bottom_edge = y0
        y_top_edge = y_bottom_edge + self.cutting_grid_params['rect_height']
        return x_left_edge, y_bottom_edge, x_right_edge, y_top_edge

    def perform_cuts(self, saving_dir):
        img_width, img_height = self.img_to_cut.size
        canv_width = self.image_canvas.winfo_width()
        canv_height = self.image_canvas.winfo_height()
        origin_x = (canv_width - img_width) // 2
        origin_y = (canv_height - img_height) // 2

        for ind, el in enumerate(self.get_coords_of_all_rect()):
            cur_x0, cur_y0 = el[0] - origin_x, el[1] - origin_y
            cut_box = self.convert_representation(cur_x0, cur_y0)
            cropped_img = self.img_to_cut.crop(cut_box)
            cropped_img.save(f'{saving_dir}/img{ind}.png')
