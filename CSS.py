# CSS.py - Assortment of functions for generating stylesheets.  
# 
# All methods are based on HSV-to-RGB algorithm from Wikipedia.

import math
import time
import random
import base64
import cStringIO
from PIL import Image


def main ():
	
	# Test essential functions 
	print "Testing CSS functions..."
	print ""

	# Initial hue, saturation and value
	h = random.randint (0, 359)
	s = random.random()
	v = random.random()

	print "Starting HSV: ({0}, {1}, {2})".format (h, s, v)
	print ""

	# Color conversion functions
	RGB = HSV_to_RGB (h, s, v)
	HTML = RGB_to_HTML (RGB)
	
	print "Converted to RGB:", RGB
	print "HTML color code:", HTML
	print ""

	# Generate backgrounds
	print "Generate backgrounds... "
	prefix = "data:image/png;base64,"
	print "Grid data URI:\n", prefix + gen_grid (h, s, v)	
	print "Polka dot data URI:\n", prefix + gen_polka (h, s, v)	
	print ""

	# Show color dictionary
	print "Create color dictionary:"
	colors = color_dict (h, s, v)
	
	for k, v in colors.iteritems():
		print "{0:>12} - {1}".format(k, v)
	


def HSV_to_RGB (hue, saturation, value):
	"""
	Converts HSV coordinates to RGB values.

	Hue is in degrees from 0 to 360. Saturation and value should be bounded
between 0 and 1.0. Function returns list of strings (e.g. ["FF", "FF", "54"]).


	Algorithm is from Wikipedia:
http://en.wikipedia.org/wiki/HSI_color_space#Converting_to_RGB
	"""

	# Set up calculations
	h = (hue % 360) / 60.0
	s = saturation
	v = value
	
	# Find chroma
	c = s * v

	# Make sure values are valid
	if c > 1.0 or c < 0.0:
		return

	# Pick RGB components
	x = c * (1 - abs (h % 2 - 1))
	(r, g, b) = {
		0: (c, x, 0),
		1: (x, c, 0),
		2: (0, c, x),
		3: (0, x, c),
		4: (x, 0, c),
		5: (c, 0, x),
		}[math.floor(h)]

	# Scale results
	m = v - c

	# Put values in hex string 
	RGB = [hex(int(round((x + m) * 255)))[2:].zfill(2) for x in (r, g, b)]

	# Return list (e.g. ["FF", "FF", "54"])
	return RGB


def RGB_to_HTML (RGB):
	"""
	Converts RGB list to HTML-readable code.

	 	e.g. ["FF", "FF", "54"] -> "#FFFF54"
	"""

	return "#{0}".format("".join(RGB))


def HSV_to_HTML (h, s, v):
	"""Returns HTML code of HSV combination."""

	return RGB_to_HTML(HSV_to_RGB(h, s, v))


def get_background (h, s, v):
	"""
	Interfaces between Django view and PNG functions.

	Hue, saturation and value are given as arguments. Data URI is returned for 
CSS background image. 
	"""

	# Switch between grid, polka, etc.
	data = gen_grid (h, s, v)
	# data = gen_polka (h, s, v)

	# Return image in URI
	prefix = """data:image/png;base64,"""
	return "{0}{1}".format(prefix, data)


def array_to_base64 (data):
	"""
	Converts PIL matrix into base64-encoded PNG string.

	Argument is a two-dimensional matrix represented as a list. Function saves PIL
generated image in string to avoid creating a file. 
	"""

	# Get number of rows in matrix
	N = int(math.sqrt(len(data)))

	# Create image
	img = Image.new ("RGB", (N, N))
	img.putdata (data)

	# Save to string instead of file
	output = cStringIO.StringIO()
	img.save (output, format="PNG")

	# Convert string to base64 and return it
	base_64_string = base64.b64encode (output.getvalue())
	return base_64_string


def gen_grid (h, s, v):
	"""
	Generates PNG for aesthetic grid background tiling.

	Hue, saturation and value are given as arguments. These are converted to
RGB for PIL coloring. PIL takes a two-dimensional array, in the form of a list,
and colors a grid of pixels accordingly. This function returns a base64-encoded
string of the generated PNG.

	Example here: alexstachowiak.com/CSS/grid.
	"""

	# Each tile is 10x10 pixels
	width = 10

	# Convert to RGB for coloring
	RGB = HSV_to_RGB (h, s, v)
	RGB = tuple([int (x, 16) for x in RGB])
	blank = (255, 255, 255)

	# Create grid pattern
	#
	# XXXX
	# X...
	# X...
	# X...
	
	data = [RGB for i in range (width)]
	data = data + sum([([RGB] + [blank for i in range (width - 1)]) for x in range (width - 1)], [])

	# Return base64-encoded PNG
	return array_to_base64 (data)


def gen_polka (h, s, v):	
	"""
	Generates PNG for polka-dot background tiling.

	Example here: alexstachowiak.com/CSS/polka.
	"""

	# Each tile is 10x10 pixels
	width = 10

	# Convert arguments to RGB for coloring
	RGB = HSV_to_RGB (h, 0, 0)
	RGB = tuple ([int (x, 16) for x in RGB])
	blank = (255, 255, 255)

	# Create polka dot pattern
	data = list ()
	[[data.append (blank) for i in range(width)] for x in range(width - 2)]
	[data.append(blank) for i in range(width - 2)]
	data.append (RGB)
	data.append (RGB)
	[data.append(blank) for i in range(width - 2)]
	data.append (RGB)
	data.append (RGB)

	# Return base64-encoded PNG
	return array_to_base64 (data)


def color_dict (h, s, v):
	"""
	Calculates harmonious colors for HSV values. 

	Returns dictionary with the following keys:
	  	    'HSV' - original HSV values (e.g. [240, 0.4, 0.78])
	      'color' - color as HTML color code (e.g. "#7777c7") 
	'compl_color' - complementary color as HTML color code ("#7777c7") 
		 'compl1' - compl. color with hue offset by angle
		 'compl2' - ""
		   'acc1' - orig. color with hue offset by angle
		   'acc2' - ""
	
	Dictionary is used in Django view to supply to template. 

	"""

	# Main color
	color =  HSV_to_RGB (h, s, v)
	HSV = [h, s, v]

	# Offset for other colors
	angle = 30

	# Complementary color
	h_comp = (h + 180) % 360
	compl = HSV_to_RGB (h_comp, s, v)

	# Get HTML codes
	color_code = RGB_to_HTML (color)
	compl_code = RGB_to_HTML (compl)

	# Put in dictionary	
	c_dict =  {'color': color_code, 'compl_color': compl_code, 'HSV': HSV}

	# Add harmonious colors
	c_dict["compl1"] = HSV_to_HTML (h_comp + angle, s, v)
	c_dict["compl2"] = HSV_to_HTML (h_comp - angle, s, v)
	c_dict["acc1"]   = HSV_to_HTML (h + angle, s, v)
	c_dict["acc2"]   = HSV_to_HTML (h - angle, s, v)

	# Return dictionary for Django template
	return c_dict


def rand_color ():
	"""Generates a random pastel color dictionary."""
	
	# Pastels have high saturation and value
	h = random.randint(0, 360)
	s = 0.95
	v = 1.0

	# Return as color dictionary
	return color_dict (h, s, v)


def get_harmony_hues (name, h):
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
	} [name]
	
	# Calculate hues and return the list
	hues = list()
	for angle in angles:
		hue = (h + angle) % 360
		hues.append (hue)
	return hues


if __name__ == '__main__':
	main()
