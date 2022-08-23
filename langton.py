#!/usr/bin/env python3

import sys
import time

# the black cells
black = {}
min_x_black, max_x_black, min_y_black, max_y_black = (0, 22 + 5, 0, 29 + 5)

# starting position
position = (0, 0)
direction = "E"


def turn_right(direction):
    if direction == "E":
        return "S"
    elif direction == "S":
        return "W"
    elif direction == "W":
        return "N"
    elif direction == "N":
        return "E"


def turn_left(direction):
    if direction == "E":
        return "N"
    elif direction == "S":
        return "E"
    elif direction == "W":
        return "S"
    elif direction == "N":
        return "W"


def move(position, direction):
    if direction == "E":
        return (position[0] + 1, position[1])
    elif direction == "S":
        return (position[0], position[1] - 1)
    elif direction == "W":
        return (position[0] - 1, position[1])
    elif direction == "N":
        return (position[0], position[1] + 1)


def turn(position, direction):
    global min_x_black, max_x_black, min_y_black, max_y_black

    if position in black:
        direction = turn_right(direction)
        black.pop(position)
    else:
        direction = turn_left(direction)
        black[position] = True

        x, y = position
        min_x_black = min(min_x_black, x)
        max_x_black = max(max_x_black, x)
        min_y_black = min(min_y_black, y)
        max_y_black = max(max_y_black, y)

    return direction


def make_boxes():
    boxes = [" "] * 16

    pixel_none = 0
    pixel_lower_left = 1 << 3
    pixel_lower_right = 1 << 2
    pixel_upper_left = 1 << 1
    pixel_upper_right = 1 << 0

    # https://en.wikipedia.org/wiki/Box-drawing_character#Block_Elements

    boxes[pixel_none] = " "
    boxes[pixel_upper_left] = "▘"
    boxes[pixel_upper_left + pixel_upper_right] = "▀"
    boxes[pixel_upper_right] = "▝"

    boxes[pixel_lower_left] = "▖"
    boxes[pixel_lower_left + pixel_upper_left] = "▌"
    boxes[pixel_lower_left + pixel_upper_left + pixel_upper_right] = "▛"
    boxes[pixel_lower_left + pixel_upper_right] = "▞"

    boxes[pixel_lower_right] = "▗"
    boxes[pixel_upper_left + pixel_lower_right] = "▚"
    boxes[pixel_upper_left + pixel_upper_right + pixel_lower_right] = "▜"
    boxes[pixel_upper_right + pixel_lower_right] = "▐"

    boxes[pixel_lower_left + pixel_lower_right] = "▄"
    boxes[pixel_upper_left + pixel_lower_left + pixel_lower_right] = "▙"
    boxes[pixel_upper_left + pixel_upper_right + pixel_lower_left + pixel_lower_right] = "█"
    boxes[pixel_upper_right + pixel_lower_left + pixel_lower_right] = "▟"

    return boxes


boxes = make_boxes()


def show():
    print("\033[H\033[2J")  # tput clear
    for y in range(max_y_black, min_y_black - 1, -2):
        line = []
        for x in range(max_x_black, min_x_black + 1, -2):

            box = (
                (((x, y) in black) << 3)  # lower left pixel
                + (((x + 1, y) in black) << 2)  # lower right pixel
                + (((x, y + 1) in black) << 1)  #  upper left pixel
                + (((x + 1, y + 1) in black) << 0)  # upper right pixel
            )

            line.append(boxes[box])
        print("".join(line))


def show_ascii():
    print("\033[H\033[2J")
    for y in range(min_y_black, max_y_black + 1):
        for x in range(min_x_black, max_x_black + 1):
            if (x, y) in black:
                print("#", end="")
            else:
                print(".", end="")
        print()


if __name__ == "__main__":
    steps = 10000
    redraw = 50

    if len(sys.argv) > 1:
        steps = int(sys.argv[1])
    if len(sys.argv) > 2:
        redraw = int(sys.argv[2])

    for iteration in range(steps):

        direction = turn(position, direction)
        position = move(position, direction)

        if iteration % redraw == 0:
            show()
            time.sleep(min(0.5, redraw / 1000))

    show()
