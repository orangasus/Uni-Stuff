import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk

from PIL import ImageTk, Image, ImageDraw

import json

# My modules
import cutting_module
import styling_module


class EditorView:
    WINDOW_GEOMETRY = '700x700'
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
        self.upload_params_button = ttk.Button(self.parent_widget, text='UPLOAD PARAMS',
                                               command=self.upload_params_clicked)

        self.create_layout()

        self.parent_widget.after(100, self.center_image_on_canvas)

        self.cur_mouse_x = parent_widget.winfo_pointerx()
        self.cur_mouse_y = parent_widget.winfo_pointery()

        self.window_state = {'rect_is_dragged': False, 'up_key_pressed': False,
                             'down_key_pressed': False, 'shift_key_pressed': False}

    # Functions responsible for creating layout
    def create_layout(self):
        cur_label_row, cur_label_col = 0, 0
        cur_entry_row, cur_entry_col = 1, 0
        for ind, param_name in enumerate(self.PARAMETERS_NAME):
            cur_entry_label = ttk.Label(self.parent_widget, text=param_name.replace('_', ' '))
            cur_entry_label.grid(row=cur_label_row, column=cur_label_col + 1)

            cur_entry = ttk.Entry(self.parent_widget, textvariable=self.entries_reference_dict[param_name])
            cur_entry.bind('<KeyRelease>', self.on_entry_change)
            cur_entry.bind('<Up>', self.up_key_pressed)
            cur_entry.bind('<KeyRelease-Up>', self.up_key_released)
            cur_entry.bind('<Down>', self.down_key_pressed)
            cur_entry.bind('<KeyRelease-Down>', self.down_key_released)
            cur_entry.grid(row=cur_entry_row, column=cur_entry_col + 1)
            self.entries_widgets.append(cur_entry)

            # switch row if last column
            if ind % 2 != 0:
                cur_label_row += 2
                cur_entry_row += 2

            cur_label_col = (cur_label_col + 1) % 2
            cur_entry_col = (cur_entry_col + 1) % 2

        self.parent_widget.bind('<Shift_L>', self.shift_key_pressed)
        self.parent_widget.bind('<KeyRelease-Shift_L>', self.shift_key_released)
        self.parent_widget.bind('<Shift_R>', self.shift_key_pressed)
        self.parent_widget.bind('<KeyRelease-Shift_R>', self.shift_key_released)

        self.cut_button.grid(row=8, column=1, columnspan=2)
        self.save_params_button.grid(row=9, column=1, columnspan=2)
        self.upload_params_button.grid(row=10, column=1, columnspan=2)
        self.image_canvas.grid(row=0, column=0, rowspan=12, sticky='news')

        self.image_canvas.tag_bind('rect', '<ButtonPress-1>', self.on_rectangle_mouse_click)
        self.image_canvas.tag_bind('rect', '<B1-Motion>', self.on_rectangle_mouse_held)

    def create_grid_for_layout(self):
        self.parent_widget.columnconfigure(1, weight=0)
        self.parent_widget.columnconfigure(2, weight=0)
        self.parent_widget.columnconfigure(0, weight=1)

        for i in range(10):
            self.parent_widget.rowconfigure(i, weight=0)
        self.parent_widget.rowconfigure(11, weight=1)

    def center_image_on_canvas(self):
        canv_width = self.image_canvas.winfo_width()
        canv_height = self.image_canvas.winfo_height()

        x_center = canv_width // 2
        y_center = canv_height // 2

        self.image_canvas.create_image(x_center, y_center,
                                       anchor=tk.CENTER, image=self.tk_img)
        self.image_canvas.image = self.tk_img

    # Functions responsible for updating parameters on change
    def on_params_change(self, event=None):
        for ind, k in enumerate(self.cutting_grid_params.keys()):
            self.set_text_entry_widget(self.entries_widgets[ind], str(self.cutting_grid_params[k]))

    def on_entry_change(self, event=None):
        print('--> On entry change')
        if self.check_that_all_entries_non_empty():
            try:
                self.cutting_grid_params = {key: int(val.get()) for key, val in self.entries_reference_dict.items()}
                self.draw_cutting_grid_on_canvas()
            except Exception as e:
                print(f"Couldn't draw the grid:\n{e}")

    # Button handler function
    def save_params_clicked(self):
        if self.check_if_all_params_int():
            # guess i rly learned sth :)
            json_filename = tk.filedialog.asksaveasfilename(filetypes=self.FILETYPES, defaultextension='.json')
            self.cutting_grid_params = {key: int(val.get()) for key, val in self.entries_reference_dict.items()}
            with open(json_filename, 'w') as params_file:
                params_file.write(json.dumps(self.cutting_grid_params))

    def cut_btn_clicked(self):
        self.cutting_grid_params = {key: int(val.get()) for key, val in self.entries_reference_dict.items()}
        if cutting_module.check_if_cutting_grid_fits(self.img_to_cut.width, self.img_to_cut.height,
                                                     self.cutting_grid_params):
            self.draw_cutting_grid_on_canvas()
            saving_dir = filedialog.askdirectory(title='Select folder to save cut images')
            if not saving_dir:
                tk.messagebox.showinfo('Error', 'No folder selected')
            else:
                cutting_module.perform_cuts(self.img_to_cut.width, self.img_to_cut.height,
                                            saving_dir, self.img_to_cut, self.cutting_grid_params,
                                            self.image_canvas.winfo_width(), self.image_canvas.winfo_height())
        else:
            tk.messagebox.showinfo('Error', 'Grid outside the image')

    def upload_params_clicked(self):
        params_file_path = tk.filedialog.askopenfilename(filetypes=[('JSON', '*.json')])
        with open(params_file_path) as params_file:
            data = json.load(params_file)
            for key, val in data.items():
                self.entries_reference_dict[key].set(str(val))
        self.on_entry_change()

    # Functions responsible for performing parameters check
    def check_if_all_params_int(self):
        for key, val in self.entries_reference_dict.items():
            if val == '' or not val.get().isnumeric():
                tk.messagebox.showinfo("Invalid Input",
                                       "All entries should be positive numbers and non-empty")
                return False
            return True

    def check_that_all_entries_non_empty(self):
        for entry in self.entries_widgets:
            if entry.get() == "":
                return False
        return True

    # Functions responsible for drawing cutting grid
    def draw_rectangle_on_canvas(self, x0, y0, rect_width, rect_height):
        # Create a new image with transparent background
        rect_image = Image.new('RGBA', (rect_width, rect_height), (255, 255, 255, 0))
        draw = ImageDraw.Draw(rect_image)

        # Draw a semi-transparent rectangle
        draw.rectangle(((0, 0), (rect_width, rect_height)), fill=(0, 0, 0, 127))  # Red with 50% transparency

        # Convert to ImageTk format
        tk_rect_image = ImageTk.PhotoImage(rect_image)

        # Add the image to the canvas
        self.image_canvas.create_image(x0, y0, anchor=tk.NW, image=tk_rect_image, tags='rect')

        # Keep a reference to avoid garbage collection
        if not hasattr(self, 'image_references'):
            self.image_references = []
        self.image_references.append(tk_rect_image)

    def draw_cutting_grid_on_canvas(self):
        self.image_canvas.delete('rect')
        for el in cutting_module.get_coords_of_all_rect(self.img_to_cut.width, self.img_to_cut.height,
                                                        self.image_canvas.winfo_width(),
                                                        self.image_canvas.winfo_height(),
                                                        self.cutting_grid_params):
            self.draw_rectangle_on_canvas(el[0], el[1], self.cutting_grid_params['rect_width'],
                                          self.cutting_grid_params['rect_height'])

    # Functions responsible for using mouse to drag cutting grid
    def on_rectangle_mouse_held(self, event):
        delta_mouse_x = event.x - self.cur_mouse_x
        delta_mouse_y = event.y - self.cur_mouse_y
        print(f"Delta X: {delta_mouse_x}, Delta Y: {delta_mouse_y}")

        self.cur_mouse_x = event.x
        self.cur_mouse_y = event.y
        print(f"Updated Mouse Position: ({self.cur_mouse_x}, {self.cur_mouse_y})")

        # Update the positions of all rectangles
        self.cutting_grid_params['top_left_rect_x'] += delta_mouse_x
        self.cutting_grid_params['top_left_rect_y'] += delta_mouse_y
        print(
            f"Updated Cutting Grid Params: {self.cutting_grid_params['top_left_rect_x']}, {self.cutting_grid_params['top_left_rect_y']}")

        self.image_canvas.move('rect', delta_mouse_x, delta_mouse_y)
        self.update_entries_from_params()

    def on_rectangle_mouse_click(self, event):
        self.cur_mouse_x = event.x
        self.cur_mouse_y = event.y
        print(f"Mouse click at: ({event.x}, {event.y})")

    def update_entries_from_params(self):
        for ind, k in enumerate(self.cutting_grid_params.keys()):
            self.set_text_entry_widget(self.entries_widgets[ind], self.cutting_grid_params[k])

    # Functions responsible for handling arrow keys and changing the entries values accordingly
    def set_text_entry_widget(self, entry_widget, text):
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, text)

    def up_key_pressed(self, event=None):
        self.window_state['up_key_pressed'] = True
        self.start_incrementing()

    def up_key_released(self, event=None):
        self.window_state['up_key_pressed'] = False

    def down_key_pressed(self, event=None):
        self.window_state['down_key_pressed'] = True
        self.start_incrementing()

    def down_key_released(self, event=None):
        self.window_state['down_key_pressed'] = False

    def shift_key_pressed(self, event=None):
        self.window_state['shift_key_pressed'] = True

    def shift_key_released(self, event=None):
        self.window_state['shift_key_pressed'] = False

    def start_incrementing(self):
        try:
            ind = self.entries_widgets.index(self.parent_widget.focus_get())
        except ValueError:
            return
        else:
            num = 10 if self.window_state['shift_key_pressed'] else 1
            if self.window_state['down_key_pressed']:
                num *= -1
            if self.entries_widgets[ind].get() == '':
                self.set_text_entry_widget(self.entries_widgets[ind], '0')
            else:
                new_val = int(self.entries_widgets[ind].get()) + num
                if new_val >= 0:
                    self.set_text_entry_widget(self.entries_widgets[ind], str(new_val))
                    self.on_entry_change()
