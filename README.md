invert.py
=========
Inverts an image in a circle

Description
-----------
A "Photoshop filter" effect that does the inversion of each point in the image with respect to a circle ([link](http://en.wikipedia.org/wiki/Inversive_geometry#Circle_inversion)).

By default, the circle is centered on the image with a radius equal to one half the image's width. You can specify the location/size of the circle and the scale the output image. The color of points inverted to infinity can provided, as well as a flag to tile the output image across the plane.

Examples
--------
    # Use default settings
    $ python invert.py monkey.png -o monkey-inverted.png

    # Use a radius of 250 pixels, a scale of 2, black infinity color, and tile the image
    $ python invert.py monkey.png -o monkey-inverted.png -r 250 --tile -s 2 -c "#000000"
 
![monkey.png](https://raw.github.com/synesthesiam/invert/master/monkey.png)
![monkey-inverted.png](https://raw.github.com/synesthesiam/magicpy/invert/monkey-inverted.png)
