def move_box(box_dict):
    print(f"{box_dict['width']}x{box_dict['height']} box is at coordinates ({box_dict['x']}, {box_dict['y']})")
    try:
        x_inc = int(input("Change x by: "))
        y_inc = int(input("Change y by: "))
    except ValueError:
        print("Value can't be accepted")
    else:
        box_dict['x'] += x_inc
        box_dict['y'] += y_inc


def convert_representation(box_dict, area_height):
    x_left_edge = box_dict['x']
    x_right_edge = x_left_edge + box_dict['width']
    y_bottom_edge = area_height - box_dict['y']
    y_top_edge = y_bottom_edge - box_dict['height']
    return (x_left_edge, x_right_edge, y_top_edge, y_bottom_edge)


box_1 = {
    "x": 0,
    "y": 0,
    "width": 50,
    "height": 20,
}
box_2 = {
    "x": 10,
    "y": 20,
    "width": 40,
    "height": 30,
}

y_max = int(input("Input maximum value of y: "))

move_box(box_1)
reversed_coords_1 = convert_representation(box_1, y_max)
print(f"Box edges in reversed coordinates\n{reversed_coords_1}")

move_box(box_2)
reversed_coords_2 = convert_representation(box_2, y_max)
print(f"Box edges in reversed coordinates\n{reversed_coords_2}")
