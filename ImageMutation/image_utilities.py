import numpy as np


def brightness(pixels):
    """ Returns a matrix for which each entry represents the brightness of the same entry in pixels.

    :param pixels:  A row x col x 3 matrix representing an image.
    :return:        A row x col x 1 matrix where each entry is the maximum of the three values for the corresponding
                    pixel.
    """
    return np.maximum(np.maximum(pixels[:, :, 0], pixels[:, :, 1]), pixels[:, :, 2])


def select_random_rows(rows):
    """ Will randomly select sequential rows. """
    import random
    start = 0
    while start != rows:
        start = random.randint(start, rows - 1) + 1
        yield start - 1


def ranges(size, max_val, start=0):
    """ Produces a series of intervals of length size, skipping size elements, which end at max_val.

    :param size:        Size of each range (or interval)
    :param start:       The starting interval.
    :param max_val:     The maximum value the intervals will go to.
    :return:            Each value in the covered intervals.
    """

    not_done = True
    while not_done:
        upper_index = min(max_val, start + size)
        for i in range(start, upper_index):
            yield i
        start += 2 * size
        if start >= max_val:
            not_done = False