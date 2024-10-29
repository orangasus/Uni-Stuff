import turtle as trtl


def draw_spiral(color, num_arcs, st_rad, rad_inc, pen_weight=1):
    trtl.color(color)
    trtl.pensize(pen_weight)
    cur_rad = st_rad
    for i in range(num_arcs):
        trtl.circle(cur_rad, 90)
        cur_rad += rad_inc


def draw_from_file(src="./resources/spiral.txt"):
    with open(src, 'r') as src_file:
        for line in src_file.readlines():
            color, num_arcs, st_rad, rad_inc, pen_weight = line.strip().split(',')
            num_arcs = int(num_arcs)
            st_rad = int(st_rad)
            rad_inc = float(rad_inc)
            pen_weight = int(pen_weight)
            draw_spiral(color, num_arcs, st_rad, rad_inc, pen_weight)
