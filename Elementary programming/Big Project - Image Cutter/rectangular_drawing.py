import sweeperlib as swlib

parameters = {
    "x": 0,
    "y": 0,
    "width": 100,
    "height": 100,
    "color": (10, 10, 255, 255),
}


def draw():
    """
    Draws a rectangle based on the values in the parameters dictionary.
    """
    swlib.clear_window()
    swlib.draw_background()
    swlib.prepare_rectangle(parameters['x'], parameters['y'],
                            parameters['width'], parameters['height'],
                            parameters['color'])
    swlib.draw_sprites()


def main():
    """
    Creates an application window and sets a handler for drawing rectangles.
    Starts the application.
    """
    # changing bg color doesn't work??
    swlib.create_window(1080, 720)
    swlib.set_draw_handler(draw)
    swlib.start()


if __name__ == "__main__":
    main()
