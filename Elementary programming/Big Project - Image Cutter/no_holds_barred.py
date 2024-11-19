import pyglet
from pyglet.window import key

THRESHOLD = 10
state = {
    "counter": 0,
    "holds": {'UP': 0, 'DOWN': 0}
}


def draw():
    window.clear()
    label = pyglet.text.Label(str(state['counter']), font_name='Times New Roman', font_size=32, x=window.width // 2,
                              y=window.height // 2, anchor_x='center', anchor_y='center')
    label.draw()


def update(delta_time):
    # taking into account whether shift is held or not
    modifier = 1
    if keyboard_state[key.LSHIFT] or keyboard_state[key.RSHIFT]:
        modifier = 10

    # checking if both arrows are pressed
    if keyboard_state[key.DOWN] and keyboard_state[key.UP]:
        return

    # if not held down
    if not keyboard_state[key.DOWN]:
        state['holds']['DOWN'] = 0

    if not keyboard_state[key.UP]:
        state['holds']['UP'] = 0

    # when the key is pressed
    if keyboard_state[key.DOWN] and state['holds']['DOWN'] == 0:
        state['counter'] -= 1 * modifier

    if keyboard_state[key.UP] and state['holds']['UP'] == 0:
        state['counter'] += 1 * modifier

    # when we start to hold the key
    if keyboard_state[key.DOWN]:
        state['holds']['DOWN'] += 1
    else:
        state['holds']['DOWN'] = 0

    if keyboard_state[key.UP]:
        state['holds']['UP'] += 1
    else:
        state['holds']['UP'] = 0

    # if we hold the key long enough to change the value
    # why state['holds']['UP'] = 1 and not 0. Well, if we want to avoid introducing new variables (as I understood from the task)
    # we need to skip through the 'single press check' in the beginning of the update function and that's the easiest way
    # + doesn't affect the functionality much
    if state['holds']['UP'] > THRESHOLD:
        state['counter'] += 1 * modifier
        state['holds']['UP'] = 1

    if state['holds']['DOWN'] > THRESHOLD:
        state['counter'] -= 1 * modifier
        state['holds']['DOWN'] = 1


def main():
    # clean this up later
    global window
    # dictionary with state of each key on the keyboard
    global keyboard_state

    keyboard_state = key.KeyStateHandler()
    window = pyglet.window.Window(width=720, height=480)
    # telling pyglet to track keys pressed in this window
    window.push_handlers(keyboard_state)
    # assigning draw function as a drawing handler
    window.push_handlers(on_draw=draw)
    # telling pyglet to run update() every 1/60 of a second
    pyglet.clock.schedule_interval(update, 1 / 60)
    pyglet.app.run()


if __name__ == "__main__":
    main()
