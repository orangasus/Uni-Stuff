def get_coords_of_all_rect(img_width, img_height, canv_width, canv_height, cutting_grid_params):
    coords = []

    # Adjusting origin point to be in the top left corner of the image, not canvas
    origin_x = (canv_width - img_width) // 2
    origin_y = (canv_height - img_height) // 2
    cur_x = cutting_grid_params['top_left_rect_x'] + origin_x
    cur_y = cutting_grid_params['top_left_rect_y'] + origin_y

    for i in range(cutting_grid_params['num_vert_rect']):
        for j in range(cutting_grid_params['num_horiz_rect']):
            print(f"Rectangle {i * cutting_grid_params['num_horiz_rect'] + j + 1}: (x={cur_x}, y={cur_y})")
            coords.append((cur_x, cur_y))
            cur_x += cutting_grid_params['rect_width'] + cutting_grid_params['rect_horiz_dist']
        cur_x = cutting_grid_params['top_left_rect_x'] + origin_x
        cur_y += cutting_grid_params['rect_height'] + cutting_grid_params['rect_vert_dist']

    return coords


def check_if_cutting_grid_fits(img_width, img_height, cutting_grid_params):
    x0, y0 = cutting_grid_params['top_left_rect_x'], cutting_grid_params['top_left_rect_y']
    xn = x0 + (cutting_grid_params['num_horiz_rect'] * cutting_grid_params['rect_width'] +
               (cutting_grid_params['num_horiz_rect'] - 1) * cutting_grid_params['rect_horiz_dist'])
    yn = y0 + (cutting_grid_params['num_vert_rect'] * cutting_grid_params['rect_height'] +
               (cutting_grid_params['num_vert_rect'] - 1) * cutting_grid_params['rect_vert_dist'])

    return (0 <= x0 <= xn <= img_width) and (0 <= y0 <= yn <= img_height)


def convert_representation(x0, y0, cutting_grid_params):
    x_left_edge = x0
    x_right_edge = x0 + cutting_grid_params['rect_width']
    y_bottom_edge = y0
    y_top_edge = y_bottom_edge + cutting_grid_params['rect_height']
    return x_left_edge, y_bottom_edge, x_right_edge, y_top_edge


def perform_cuts(img_width, img_height, saving_folder, img_to_cut, cutting_grid_params, canv_width = None, canv_height=None):
    if canv_width is None:
        canv_width = img_width
    if canv_height is None:
        canv_height = img_height

    origin_x = (canv_width - img_width) // 2
    origin_y = (canv_height - img_height) // 2


    for ind, el in enumerate(get_coords_of_all_rect(img_width, img_height, canv_width, canv_height, cutting_grid_params)):
        cur_x0, cur_y0 = el[0] - origin_x, el[1] - origin_y
        print(cur_x0, cur_y0)
        cut_box = convert_representation(cur_x0, cur_y0, cutting_grid_params)
        cropped_img = img_to_cut.crop(cut_box)
        cropped_img.save(f'{saving_folder}/img{ind}.png')
