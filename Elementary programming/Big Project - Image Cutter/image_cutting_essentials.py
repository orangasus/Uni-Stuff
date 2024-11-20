import os.path

from PIL import Image as Pil_Image


def prompt_input(prompt_str, error_str, min_value=0):
    """
    Prompts an integer from the user using the given prompt string. The integer
    is checked against a minimum value that is taken from an optional argument, and
    defaults to 0. If the user gives an invalid input, the provided error message
    is printed.
    """

    while True:
        try:
            x = int(input(prompt_str))
            if x < min_value:
                raise ValueError
        except ValueError:
            print(error_str)
        else:
            return x


def prompt_path(prompt_str, error_str="", new_file=False):
    """
    Prompts the user to provide a path using the given prompt string. This
    function checks whether the path matches an existing file, unless the last
    optional parameter has a value of True. If checked, and the file does not exist
    the user is given the error message from the second parameter and prompted
    again.
    """
    while True:
        file_path = input(prompt_str)
        if new_file or os.path.exists(file_path):
            return file_path
        print(error_str)


def prompt_values():
    """
    Prompts the user for edge coordinates of a rectangle and returns them as a
    dictionary. Only positive integers are accepted. In addition, the right edge
    of the rectangle must be larger than the left, and similarly the bottom edge
    must be larger than the top edge. The returned dictionary contains these edges
    in the keys "left", "right", "top", "bottom".
    """

    left = prompt_input('Left: ', 'Value error')
    right = prompt_input('Right: ', 'Value error', left)
    top = prompt_input('Top: ', 'Value error')
    bottom = prompt_input('Bottom: ', 'Value error', top)

    return {'left': left, 'right': right, 'top': top, 'bottom': bottom}


def perform_cut(src_image_path, cut_params, res_image_path):
    """
    Cuts a region from the provided image and saves it as a new image in the
    requested location. The region's dimensions are taken from the provided
    dictionary from the keys "left", "right", "top", "bottom". As the origin for
    the image is at the top left corner, the bottom coordinate should be larger
    than the top coordinate. If the region goes outside the source image, the cut
    is not performed.
    """

    try:
        with Pil_Image.open(src_image_path) as img:
            img_width, img_height = img.size
            # checks if the rectangle fits into img dimensions
            if (0 <= cut_params['bottom'] <= img_height) and (0 <= cut_params['top'] <= img_height) and (
                    0 <= cut_params['left'] <= img_width) and (0 <= cut_params['right'] <= img_width):
                res_img = img.crop((cut_params['left'], cut_params['top'], cut_params['right'], cut_params['bottom']))
                # Should the use provide file extension???
                res_img.save(res_image_path)

    except Exception as e:
        print(f"Something went wrong with the image: {e}")


def main():
    file_path = prompt_path("File path: ", "File does not exist.")
    val_dict = prompt_values()
    perform_cut(file_path, val_dict, "./TestImages/res.png")


if __name__ == "__main__":
    main()
