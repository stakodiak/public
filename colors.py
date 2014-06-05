#!/usr/bin/python2.7
"""
Assortment of functions for generating stylesheets. All methods are
based on HSV-to-RGB algorithm from Wikipedia.
"""
import base64
import cStringIO
import math
import random
from PIL import Image


def main():
    """Tests essential functions."""
    print "Testing color functions..."
    print ""

    # Initial hue, saturation and value
    hue = random.randint(0, 359)
    saturation = random.random()
    value = random.random()
    print "Starting HSV: ({0}, {1}, {2})".format(hue, saturation, value)
    print ""

    # Color conversion functions
    rgb = hsv_to_rgb(hue, saturation, value)
    html = rgb_to_html(rgb)
    print "Converted to RGB:", rgb
    print "HTML color code:", html
    print ""

    # Generate backgrounds
    prefix = "data:image/png;base64,"
    print "Generate backgrounds... "
    print "Grid data URI:\n", prefix + gen_grid(hue, saturation, value)
    print "Polka dot data URI:\n", prefix + gen_polka(hue, saturation, value)
    print ""

    # Show color dictionary
    print "Create color dictionary:"
    colors = color_dict(hue, saturation, value)
    for key, val in colors.iteritems():
        print "{0:>12} - {1}".format(key, val)

def hsv_to_rgb(hue, saturation, value):
    """
    Converts HSV coordinates to RGB values.

    Hue is in degrees from 0 to 360. Saturation and value should be
    bounded between 0 and 1.0. Function returns list of strings (e.g.
    ["FF", "FF", "54"]).


    Algorithm is from Wikipedia:
    http://en.wikipedia.org/wiki/HSI_color_space#Converting_to_RGB
    """

    hue = (hue % 360) / 60.0  # make sure hue is in degrees
    chroma = saturation * value

    # Make sure values are valid
    if chroma > 1.0 or chroma < 0.0:
        return

    # Pick RGB components
    section = chroma * (1 - abs(hue % 2 - 1))
    (red, green, blue) = {
        0: (chroma, section, 0),
        1: (section, chroma, 0),
        2: (0, chroma, section),
        3: (0, section, chroma),
        4: (section, 0, chroma),
        5: (chroma, 0, section),
        }[math.floor(hue)]

    # Put values in hex string
    scale = value - chroma
    rgb = [hex(int(round((x + scale) * 255)))[2:].zfill(2)
           for x in (red, green, blue)]

    # Return list(e.g. ["FF", "FF", "54"])
    return rgb


def rgb_to_html(rgb):
    """
    Converts RGB list to HTML-readable code.
        e.g. ["FF", "FF", "54"] -> "#FFFF54"
    """
    return "#{0}".format("".join(rgb))


def hsv_to_html(hue, saturation, value):
    """Returns HTML code of HSV combination."""
    return rgb_to_html(hsv_to_rgb(hue, saturation, value))


def get_background(hue, saturation, value):
    """
    Interfaces between Django view and PNG functions.

    Hue, saturation and value are given as arguments. Data URI is
    returned for CSS background image.
    """
    # Switch between grid, polka, etc.
    data = gen_grid(hue, saturation, value)
    # data = gen_polka(hue, saturation, value)

    # Return image in URI
    prefix = """data:image/png;base64,"""
    return "{0}{1}".format(prefix, data)


def array_to_base64(data):
    """
    Converts PIL matrix into base64-encoded PNG string.

    Argument is a two-dimensional matrix represented as a list.
    Function saves PIL generated image in string to avoid creating a
    file.
    """

    # Get number of rows in matrix
    num = int(math.sqrt(len(data)))

    # Create image
    img = Image.new("RGB", (num, num))
    img.putdata(data)

    # Save to string instead of file
    output = cStringIO.StringIO()
    img.save(output, format="PNG")

    # Convert string to base64 and return it
    base_64_string = base64.b64encode(output.getvalue())
    return base_64_string


def gen_grid(hue, saturation, value):
    """
    Generates PNG for aesthetic grid background tiling.

    Hue, saturation and value are given as arguments. These are
    converted to RGB for PIL coloring. PIL takes a two-dimensional
    array, in the form of a list, and colors a grid of pixels
    accordingly. This function returns a base64-encoded string of the
    generated PNG.

    Example here: alexstachowiak.com/CSS/grid.
    """
    # Each tile is 10x10 pixels
    width = 10

    # Convert to RGB for coloring
    rgb = hsv_to_rgb(hue, saturation, value)
    rgb = tuple([int(x, 16) for x in rgb])
    blank = (255, 255, 255)

    # Create grid pattern
    #
    # xxxx
    # x...
    # x...
    # x...
    grid = [rgb for _ in range(width)]
    grid += sum([([rgb] + [blank for _ in range(width - 1)])
                 for _ in range(width - 1)], [])

    # Return base64-encoded PNG
    return array_to_base64(grid)


def gen_polka(hue, saturation, value):
    """
    Generates PNG for polka-dot background tiling.

    Example here: alexstachowiak.com/CSS/polka.
    """
    # Each tile is 10x10 pixels
    width = 10

    # Convert arguments to RGB for coloring
    rgb = hsv_to_rgb(hue, saturation, value)
    rgb = tuple([int(x, 16) for x in rgb])
    blank = (255, 255, 255)

    # Create polka dot pattern
    data = list()
    for _ in range(width - 2):
        for _ in range(width):
            data.append(blank)
    for _ in range(width - 2):
        data.append(blank)
    data.append(rgb)
    data.append(rgb)
    for _ in range(width - 2):
        data.append(blank)
    data.append(rgb)
    data.append(rgb)

    # Return base64-encoded PNG
    return array_to_base64(data)


def color_dict(hue, saturation, value):
    """
    Calculates harmonious colors for HSV values.

    Returns dictionary with the following keys:
            'HSV' - original HSV values(e.g. [240, 0.4, 0.78])
          'color' - color as HTML color code(e.g. "#7777c7")
    'compl_color' - complementary color as HTML color code("#7777c7")
         'compl1' - compl. color with hue offset by angle
         'compl2' - ""
           'acc1' - orig. color with hue offset by angle
           'acc2' - ""

    Dictionary is used in Django view to supply to template.

    """
    # Main color
    color = hsv_to_rgb(hue, saturation, value)
    hsv = (hue, saturation, value)

    # Offset for other colors
    angle = 30

    # Complementary color
    h_comp = (hue + 180) % 360
    compl = hsv_to_rgb(h_comp, saturation, value)

    # Get HTML codes
    color_code = rgb_to_html(color)
    compl_code = rgb_to_html(compl)

    # Put in dictionary
    c_dict = {'color': color_code, 'compl_color': compl_code, 'HSV': hsv}

    # Add harmonious colors
    c_dict["compl1"] = hsv_to_html(h_comp + angle, saturation, value)
    c_dict["compl2"] = hsv_to_html(h_comp - angle, saturation, value)
    c_dict["acc1"] = hsv_to_html(hue + angle, saturation, value)
    c_dict["acc2"] = hsv_to_html(hue - angle, saturation, value)

    # Return dictionary for Django template
    return c_dict


def rand_color():
    """Generates a random pastel color dictionary."""

    # Pastels have high saturation and value
    hue = random.randint(0, 360)
    saturation = 0.95
    value = 1.0

    # Return as color dictionary
    return color_dict(hue, saturation, value)


def get_harmony_hues(name, hue):
    """Get harmonies of a hue to generate color schemes."""
    # Harmonies to find
    complement = 180
    triad = 30
    tetrad = 60
    analog = 30

    # Pick the harmony
    angles = {
        'complement': (0, complement),
        'triad': (0, complement - triad, complement + triad),
        'tetrad': (0, tetrad, complement, complement + tetrad),
        'analogic': (analog, 0 - analog),
    }[name]

    # Calculate hues and return the list
    hues = list()
    for angle in angles:
        hue = (hue + angle) % 360
        hues.append(hue)
    return hues


if __name__ == '__main__':
    main()
