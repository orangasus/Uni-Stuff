def prompt_input(promt, error_msg):
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


def get_coordinates(num_tiles_hor, num_tiles_vert, x_first_tile,
                    y_first_tile, tile_inter_hor, tile_inter_vert):
    """
    Calculates coordinates for a grid figure where the size of each tile is 1.
    Returns a list of coordinates so that the first tile is in the given initial
    coordinates, and the other ones are always a certain distance away from the
    previous one.
    """

    coords = []
    cur_x, cur_y = x_first_tile, y_first_tile
    for i in range(num_tiles_vert):
        for j in range(num_tiles_hor):
            coords.append((cur_x, cur_y))
            cur_x += tile_inter_hor + 1
        cur_x = x_first_tile
        cur_y += tile_inter_vert + 1

    return coords


def find_characters(grid, coords):
    """
    Retrieves characters that fall under the list of given coordinates from the
    given grid. Coordinates are read from top to bottom and left to right.
    Retrieved characters are returned as a list.
    If at least one coordinate pair falls outside the grid, returns an empty list
    instead.
    """
    x_max = len(grid[0]) - 1
    y_max = len(grid) - 1

    # checking if all the received coordinates are within the grid
    for x, y in coords:
        if (x > x_max or x < 0) or (y > y_max or y < 0):
            print("The coordinates go outside the grid")
            return []

    coords.sort()

    # retrieving chars from the grid
    chars = []
    for x, y in coords:
        chars.append(grid[y][x])
    return chars


grid = [
    "lHuVZmmIXaQJwMJkSLlw",
    "KvCrlshqWoMasMvczAhh",
    "knPAJtJpQpkBtABbkOhr",
    "dJGOlebscgWIzmvDbjcU",
    "zrMWdUaVOUeULVOMiZIo",
    "AIhmcMTqtMVIHugFPvfi",
    "hmGLoLYLppyluJlHnSZi",
    "KNaSVIaJzGByYVpdgQFT",
    "DBrjnrRSknsEHimOgAnF",
    "WnFTXGFmoAFfJqlFPBap",
    "ocUHkmAlMawYkmywsFPK",
    "ekaRsoQPqHwkFkaktfWJ",
    "nBzkcfwRSfKuJQyYKwfl",
    "HkRceMHYJDbvnhWRnPCn",
    "EgrQbIvdEIaqNmcgzPNb",
    "lddDLPiAsKrYAPNNewyT",
    "lUsZyjUMywwcygDjujiD",
    "OrfnDAoDDHUjKeDHRuYM",
    "THxlxWcATqBmBzurjVFi",
    "HshFgacciAXNWKXTrBMn",
]
print("Code grid: ")
for row in grid:
    print(" ".join(row))
t_h = prompt_input("Number of tiles horizontally: ", "Please give a positive integer")
t_v = prompt_input("Number of tiles vertically: ", "Please give a positive integer")
x_f = prompt_input("X coordinate of the first tile: ", "Please give a positive integer")
y_f = prompt_input("Y coordinate of the first tile: ", "Please give a positive integer")
s_h = prompt_input("Space between tiles (horizontally): ", "Please give a positive integer")
s_v = prompt_input("Space between tiles (vertically): ", "Please give a positive integer")

secret = find_characters(grid, get_coordinates(t_h, t_v, x_f, y_f, s_h, s_v))
if len(secret) != 0:
    print('The secret code is:')
    print(''.join(secret))
