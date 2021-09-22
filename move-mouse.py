from os import system
import subprocess;
import re;
import sys;
import argparse

#parse arguments
ap = argparse.ArgumentParser()
dir_group = ap.add_mutually_exclusive_group(required=True)
dir_group.add_argument("-l", "--left", action="store_true", help="Moves mouse to the left of the current monitor")
dir_group.add_argument("-r", "--right", action="store_true",help="Moves mouse to the right the current monitor")
dir_group.add_argument("-b", "--bottom", action="store_true", help="Moves mouse below the current monitor")
dir_group.add_argument("-t", "--top", action="store_true", help="Moves mouse above the current monitor")

ap.set_defaults(top=False, left=False,  bottom=False, right=False)

args = vars(ap.parse_args())
left = args["left"]
top = args["top"]
right = args["right"]
bottom = args["bottom"]

print(f"Bottom {bottom}")

#get screens
xrandr_proc = subprocess.Popen(("xrandr"), stdout=subprocess.PIPE)
MONITOR_REGEX="^(.*) connected(.*) ([0-9]+)x([0-9]+)\+([0-9]+)\+([0-9]+) (.*)$"
output = subprocess.check_output(["sed", "-rn", f"s/{MONITOR_REGEX}/\\3 \\4 \\5 \\6/p"], stdin=xrandr_proc.stdout)
xrandr_proc.wait()


screens = []
for dim in output.splitlines():
    res = dim.split()
    mapped = map(int, res)
    screens.append(tuple(mapped))

#takes an array of screens and some coordinates and returns the
#screen which contains these coordinates
def get_screen(screens, x, y):
    for screen in screens:
        (width, height, x_offset, y_offset) = screen
        if(
            x_offset <= x < x_offset + width and
            y_offset <= y < y_offset + height
        ):
            return screen

def get_left_screen(screens, screen):
    (width, height, x_offset, y_offset) = screen
    if(width < 0 or height < 0 or x_offset < 0 or y_offset < 0):
        return (-1, -1, -1, -1)
    for scr in screens:
        (w, h, x, y) = scr
        if(x + w == x_offset and y == y_offset):
            return scr
    return (-1,-1,-1,-1)

def get_right_screen(screens, screen):
    (width, height, x_offset, y_offset) = screen
    if(width < 0 or height < 0 or x_offset < 0 or y_offset < 0):
        return (-1, -1, -1, -1)
    for scr in screens:
        (w, h, x, y) = scr
        print(f"We are checking screen ({w},{h},{x},{y})")
        if(x_offset + width == x and y == y_offset):
            print("We found the right screen")
            return scr
        print("No screen found")
        
    return (-1,-1,-1,-1)

def get_top_screen(screens, screen):
    (width, height, x_offset, y_offset) = screen
    if(width < 0 or height < 0 or x_offset < 0 or y_offset < 0):
        return (-1, -1, -1, -1)
    for scr in screens:
        (w, h, x, y) = scr
        if(y + h == y_offset and x == x_offset):
            return scr
    return (-1,-1,-1,-1)

def get_bottom_screen(screens, screen):
    (width, height, x_offset, y_offset) = screen
    if(width < 0 or height < 0 or x_offset < 0 or y_offset < 0):
        return (-1, -1, -1, -1)
    for scr in screens:
        (w, h, x, y) = scr
        if(y_offset + height == y and x == x_offset):
            return scr
    return (-1,-1,-1,-1)

def center(screen):
    (w, h, x, y) = screen
    if(w < 0 or h < 0 or x < 0 or y < 0):
        return (-1, -1)
    return (int((x + (w / 2))), int((y+ (h / 2) )))


MOUSE_REGEX="^x:([0-9]+) y:([0-9]+) screen:([0-9]+) window:([0-9]+)$"
def get_mouse_location():
    xtool_proc = subprocess.Popen(("xdotool", "getmouselocation"), stdout=subprocess.PIPE)
    mouse_output = subprocess.check_output(["sed", "-r", "s/^x:([0-9]+) y:([0-9]+) screen:([0-9]+) window:([0-9]+)$/\\1 \\2/"], stdin=xtool_proc.stdout)
    coords = mouse_output.split()
    mapped_coords = map(int, coords)
    return tuple(mapped_coords)


def move_mouse_to_screen(screen):
    (scr_c_x, scr_c_y) = center(screen)
    if(scr_c_x > 0 and scr_c_y > 0):
        system(f"xdotool mousemove {scr_c_x} {scr_c_y}")


if(left):
    (mouse_x, mouse_y) = get_mouse_location()
    move_mouse_to_screen(get_left_screen(screens, get_screen(screens, mouse_x, mouse_y)))

if(right):
    (mouse_x, mouse_y) = get_mouse_location()
    move_mouse_to_screen(get_right_screen(screens, get_screen(screens, mouse_x, mouse_y)))

if(top):
    (mouse_x, mouse_y) = get_mouse_location()
    move_mouse_to_screen(get_top_screen(screens, get_screen(screens, mouse_x, mouse_y)))

if(bottom):
    (mouse_x, mouse_y) = get_mouse_location()
    move_mouse_to_screen(get_bottom_screen(screens, get_screen(screens, mouse_x, mouse_y)))

for (width, height, x_offset, y_offset) in screens:
    print(width, height, x_offset, y_offset)

""" if(left):
    ()
    (x, y) = center(get_left_screen(screens,))
    system(f"xdotool mousemove") """



#Now the screens array will contain the information for all our screens