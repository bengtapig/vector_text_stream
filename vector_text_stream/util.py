#!/usr/bin/env python

# Copyright (c) 2020 Ryo Sakagami
#
# This software is released under the MIT License.
# http://opensource.org/licenses/mit-license.php

"""
Utility functions for showing long sentence(s) on Vector's screen.
"""

import anki_vector
import os
import sys
import time

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    sys.exit("Cannot import from PIL. Do `pip3 install --user Pillow` to install")

# Information of Vector
SCREEN_WIDTH = 184
SCREEN_HEIGHT = 96

# Font
DIRNAME = os.path.dirname(__file__)
FONT_PATH = os.path.abspath(os.path.join(DIRNAME, 'fonts/JF-Dot-jiskan24.ttf'))


def make_entire_text_image(text, color=(233, 139, 51, 255), font_size=50, position='center'):
    """Function to make an entire text image from string.

    Arguments:
        text {string} -- Text to render in image.

    Keyword Arguments:
        color {tuple} -- Color of the text (default: {(233, 139, 51, 255)}).
        font_size {int} -- Size of the font (default: {50}).
        position {str} -- Vertical position of text in the image.
                          Valid options are 'top', 'center', or 'bottom' (default: {'center'}).

    Raises:
        RuntimeError: Raised when a value except 'top', 'center', or 'bottom' is passed to argument position.

    Returns:
        image {PIL.Image} -- Image with the text rendered on it.
    """
    print("Read font file from {}".format(FONT_PATH))
    font = ImageFont.truetype(FONT_PATH, font_size)
    text_size = font.getsize(text)
    try:
        assert text_size[1] < SCREEN_HEIGHT
    except AssertionError:
        print("Y dimension of text_size exceeds Vector's screen height. Reduce font size.")

    # X dimension of image_size is incremented by 2 * SCREEN_WIDTH for animation
    image_size = (text_size[0] + SCREEN_WIDTH * 2, SCREEN_HEIGHT)
    image = Image.new('RGBA', image_size, (0, 0, 0, 255))
    draw = ImageDraw.Draw(image)

    if position == 'top':
        v_pos = 0
    elif position == 'center':
        v_pos = int(SCREEN_HEIGHT / 4)
    elif position == 'bottom':
        v_pos = int(SCREEN_HEIGHT / 2)
    else:
        print("Position " + str(position) + " is not implemented.")
        raise RuntimeError

    draw.text((SCREEN_WIDTH, v_pos), text, fill=color, font=font)
    return image

def prepare_screen_data_list(text, color=(233, 139, 51, 255), font_size=50, position='center', pixel_per_sec=400, render_hz=10):
    entire_text_image = make_entire_text_image(
        text, color=color, font_size=font_size, position='center')
    render_hz = 20
    entire_duration_s = entire_text_image.size[0] / pixel_per_sec
    render_number = int(render_hz * entire_duration_s)

    print("Rendering Hz: {}".format(render_hz))
    print("Entire duration: {} seconds".format(entire_duration_s))
    print("Total rendering times: {}".format(render_number))

    """
    screen_data_list = []
    for i in range(render_number):
        # Calculate start px
        px = int(pixel_per_sec / render_hz) * i
        # Crop image from the entire text image
        text_image = entire_text_image.crop(
            (px, 0, px + SCREEN_WIDTH, SCREEN_HEIGHT))
        # Convert to the format for Vector
        screen_data = anki_vector.screen.convert_image_to_screen_data(
            text_image)
        screen_data_list.append(screen_data)
    """
    # NOTE: Use the following one-liner expression to improve performance!
    #       The process is equivalent to the above the block comment.
    screen_data_list = [anki_vector.screen.convert_image_to_screen_data(entire_text_image.crop(
            (int(pixel_per_sec / render_hz) * i, 0, int(pixel_per_sec / render_hz) * i + SCREEN_WIDTH, SCREEN_HEIGHT))) for i in range(render_number)]
    return screen_data_list


def render_screen_data_list(robot, screen_data_list, render_hz=10):
    for screen_data in screen_data_list:
        # Show image
        robot.screen.set_screen_with_image_data(screen_data, 1 / render_hz)
        time.sleep(1 / render_hz)


def show_text(robot, text, color=(233, 139, 51, 255), font_size=50, position='center', pixel_per_sec=400, render_hz=10):
    """Function to show text with sliding animation on Vector's screen.

    Arguments:
        robot {anki_vector.Robot} -- Instance of Vector robot.
        text {string} -- Text to show on Vector's screen.

    Keyword Arguments:
        color {tuple} -- Color of the text (default: {(233, 139, 51, 255)}).
        font_size {int} -- Size of the font (default: {50}).
        position {str} -- Vertical position of text in the image.
                          Valid options are 'top', 'center', or 'bottom' (default: {'center'}).
        pixel_per_sec {int} -- Moving speed of the text. Unit is pixel per second. (default: {400})
    """
    screen_data_list = prepare_screen_data_list(text, color, font_size, position, pixel_per_sec, render_hz)
    render_screen_data_list(robot, screen_data_list, render_hz)
