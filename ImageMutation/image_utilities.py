import numpy as np


def brightness(pixels):
    """ Returns a matrix for which each entry represents the brightness of the same entry in pixels.

    :param pixels:  A row x col x 3 matrix representing an image.
    :return:        A row x col x 1 matrix where each entry is the maximum of the three values for the corresponding
                    pixel.
    """
    """ For each pixel in pixels, returns the brightness (or maximum of its three colors). """
    big_pixels = pixels.astype(int)
    return np.maximum(np.maximum(big_pixels[:, :, 0], big_pixels[:, :, 1]), big_pixels[:, :, 2])


def select_random_rows(rows):
    """ Will randomly select sequential rows. """
    import random
    start = 0
    while start != rows:
        start = random.randint(start, rows - 1) + 1
        yield start - 1
