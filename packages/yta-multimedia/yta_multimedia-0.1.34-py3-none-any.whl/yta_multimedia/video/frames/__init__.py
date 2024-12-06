"""
Using the 'get_frame' in moviepy returns a numpy array of 3 or 1 
dimension depending on the type of clip. If the clip is a main 
clip, a 3d array with values between [0, 255] is returned (one
[255, 255, 255] array would be a white pixel). If the clip is a
mask clip, a 1d array with values between [0, 1] is returned (the
1 completely transparent, the 0 is not).

Thats why you need to normalize or denormalize those values to
work with them because they are different and turning frames into
an image would need you to have the same range [0, 1] or [0, 255].

Check the Pillow, ImageIO and other libraries to see what kind of
numpy arrays are needed to write (or read) images.

TODO: This was in the previous 'frames.py' file that was moved to
a whole module in a folder. Do I need this explanation here (?)
"""