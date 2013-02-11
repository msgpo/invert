#!/usr/bin/python

# Copyright (C) 2013 Michael Hansen (mihansen@indiana.edu)

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import numpy as np, argparse
from PIL import Image

def HTMLColorToRGBA(html_color):
    """Converts #RRGGBB[AA] to (R, G, B, A)"""
    if html_color.startswith("#"):
        html_color = html_color[1:]

    alpha = 255 if len(html_color) < 8 else int(html_color[6:8])

    return (int(html_color[0:2], 16),
            int(html_color[2:4], 16),
            int(html_color[4:6], 16),
            alpha)

def invert(p, center, radius):
    """Inverts p in a circle at center with the given radius"""
    dist = (p[0] - center[0])**2 + (p[1] - center[1])**2
    return radius**2 * (p - center) / dist

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description = "Inversion in a circle filter")

    parser.add_argument("input", type=str,
            help = "Path to input image")

    parser.add_argument("-o", "--output", type=str, default="output.png",
            help="Path to output image (default: output.png)")

    parser.add_argument("-r", "--radius", type=float, default=np.NaN,
            help = "Radius of the inversion circle (default: half image width)")

    parser.add_argument("-x", "--centerx", type=float, default=np.NaN,
            help = "X coordinate of inversion circle center (default: half image width)")

    parser.add_argument("-y", "--centery", type=float, default=np.NaN,
            help = "Y coordinate of inversion circle center (default: half image width)")

    parser.add_argument("-s", "--scale", type=float, default=1.0,
            help = "Scalar for inverted image size (default: 1.0)")

    parser.add_argument("-c", "--color", type=str, default="#FFFFFF",
            help = "Color to use for points beyond image bounds in non-tiled case (default: #FFFFFF)")

    parser.add_argument("--tile", action="store_true", help = "Tile source image across the plane")

    args = parser.parse_args()

    in_image = Image.open(args.input).convert("RGBA")
    in_data = in_image.load()
    in_size = np.array(in_image.size)

    out_image = Image.new("RGBA", (in_size * args.scale).astype(int))
    out_data = out_image.load()

    inf_color = HTMLColorToRGBA(args.color)
    half = np.array(out_image.size) / 2.0

    center = np.array([half[0] if np.isnan(args.centerx) else args.centerx,
                       half[1] if np.isnan(args.centery) else args.centery])

    radius = half[0] if np.isnan(args.radius) else args.radius

    # Do filter (painfully slow)
    for x in range(out_image.size[0]):
        for y in range(out_image.size[1]):
            p = invert(np.array([x, y]), center, radius) + half

            if args.tile:
                p = np.abs(p).round() % in_size
            else:
                p = p.round()

            c = inf_color

            # If inside original image bounds, use actual color
            if ((0 <= p[0] < in_size[0]) and
                (0 <= p[1] < in_size[1])):
                c = in_data[int(p[0]), int(p[1])]

            out_data[x, y] = c
      
    out_image.save(args.output)
