def convert_representation(box_dict, area_height):
    """Converts rectangle coordinates from (x,y) of top
    left corner to the edges coordinates"""
    x_left_edge = box_dict['x']
    x_right_edge = x_left_edge + box_dict['width']
    y_bottom_edge = area_height - box_dict['y']
    y_top_edge = y_bottom_edge - box_dict['height']
    return (x_left_edge, x_right_edge, y_top_edge, y_bottom_edge)


def prompt_input(promt, error_msg='Please give a positive integer'):
    """
    Prompts the user for an integer using the prompt parameter.
    If an invalid input is given, an error message is shown using
    the error message parameter. A valid input is returned as an
    integer
    """

    while True:
        try:
            x = int(input(promt))
        except:
            print(error_msg)
        else:
            if x > -1:
                return x
            print(error_msg)


def get_coordinates(deploy_dict):
    """
    Calculates coordinates for a set of rectangles based on given parameters.
    Returns a list of coordinates so that the first rectangle is at the given
    initial coordinates, and the following rectangles are spaced the given
    distance away from previous one.
    """

    coords = []
    cur_x, cur_y = deploy_dict['x-initial'], deploy_dict['y-initial']
    for i in range(deploy_dict['rows']):
        for j in range(deploy_dict['columns']):
            coords.append((cur_x, cur_y))
            cur_x += deploy_dict['width'] + deploy_dict['x-spacing']
        cur_x = deploy_dict['x-initial']
        cur_y += deploy_dict['height'] + deploy_dict['y-spacing']
    return coords


def create_rects(deploy_dict):
    """
    Calculates positions for rectangles based on given parameters.
    The parameters in the dictionary are interpreted as being defined
    in a coordinate system where the origin is at the top left corner.
    The function returns the edge coordinates of each rectangle, presented
    in a coordinate system where the origin is at the bottom left corner.
    """
    top_left_corner_coords = get_coordinates(deploy_dict)
    edges_coords = []
    for x, y in top_left_corner_coords:
        edges_coords.append(
            convert_representation({'x': x, 'y': y, 'width': deploy_dict['width'],
                                    'height': deploy_dict['height']},
                                   deploy_dict['image-height']))
    return edges_coords


def print_rectangles_created(coords):
    """Prints edges coordinates on separate
    lines for each rectangle"""
    for rect in coords:
        print(rect)


deployment_dict = {'columns': prompt_input('Number of rectangles (horizontal): '),
                   'rows': prompt_input('Number of rectangles (vertical): '),
                   'width': prompt_input('Rectangle width: '),
                   'height': prompt_input('Rectangle height: '),
                   'x-initial': prompt_input('X coordinate of the first rectangle: '),
                   'y-initial': prompt_input('Y coordinate of the first rectangle: '),
                   'x-spacing': prompt_input('Rectangle spacing (horizontal): '),
                   'y-spacing': prompt_input('Rectangle spacing (vertical): '),
                   'image-height': prompt_input('Image height for coordinate flipping: ')}

print_rectangles_created(create_rects(deployment_dict))
