from math import pi, sqrt


def calculate_square_area(x):
    return round(x ** 2, 4)


def calculate_sector_area(r, angle):
    return round(angle / 360 * pi * r ** 2, 4)


def calculate_catheti(hyp):
    return round(hyp / sqrt(2), 4)


def calculate_figure_area(x):
    s1 = calculate_square_area(x)
    r2 = calculate_catheti(x)
    s2 = calculate_sector_area(r2, 90)
    x3 = r2 * 2
    s3 = calculate_square_area(x3)
    s4 = calculate_sector_area(x3, 270)
    return s1 + s2 + s3 + s4


x_inp = float(input("Input x: "))
print("Figure area: ", round(calculate_figure_area(x_inp), 4))
