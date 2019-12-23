from PIL import Image
import numpy as np
from image_utilities import ranges


def parse_args():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--files", "-f", dest="files", default=["../demo/nasa--hI5dX2ObAs-unsplash.jpg"], nargs="+",
                        help="File(s) to sort. Can be any format supported by PIL. ")
    fit_options = parser.add_mutually_exclusive_group(required=True)
    fit_options.add_argument("--reshape", nargs=2, type=int, default=None,
                             help="Output shape. Row col order.")
    fit_options.add_argument("--random_fit", action="store_true",
                             help="Will fit to a random rectangle.")
    fit_options.add_argument("--most_square", action="store_true",
                             help="Will fit to the most square rectangle.")

    return parser.parse_args()


def random_fit(n, loss_tolerance=0.1):
    """ Returns a random pair of values which, when multiplied, is close to n.

    :param n:               The number to produce a random fit for.
    :param loss_tolerance:  The maximum negative difference that is allowed.
    :return:                Two numbers which, when multiplied, are between 100*(1-loss_tolerance)% and 100% of n.
    """

    assert 0 <= loss_tolerance <= 1
    assert n < 65535 ** 2
    # Max dim is 65535
    import random

    side_a = random.randint(0, n)
    side_b = n // side_a
    while side_a > 65535 or side_b > 65535:
        side_a = random.randint(0, n)
        side_b = n // side_a

    while (n - side_a * side_b) / n > loss_tolerance:
        side_a += 1
        side_b = n // side_a

    return side_a, side_b


def factors(n):
    """ Returns the factors of n which are closest to being square.

    :param n:       The number to produce factors for
    :return:        Two
    """
    import math
    guess = math.ceil(math.sqrt(n))
    while n % guess != 0:
        guess -= 1
    return int(n / guess), int(guess)


def main():
    """ Program runner: parses the arguments and produces the appropriate images."""
    import os

    args = parse_args()

    for file_name in args.files:
        img = Image.open(file_name)

        pixel_view = np.asarray(img)
        rows, cols, _ = pixel_view.shape
        true_pixel_count = rows * cols

        if args.reshape:
            reshape_rows, reshape_cols = args.reshape
        elif args.most_square:
            reshape_rows, reshape_cols = factors(true_pixel_count)
        else:
            reshape_rows, reshape_cols = random_fit(true_pixel_count)

        num_pixels = reshape_rows * reshape_cols

        pixels = np.reshape(pixel_view, (rows * cols, 1, 3))

        if true_pixel_count < num_pixels and args.pad:
            extension = np.zeros((num_pixels - true_pixel_count, 3), dtype=np.uint8)
            pixels = np.append(pixels, extension)

        pixels = np.reshape(pixels[:num_pixels], (reshape_rows, reshape_cols, 3))

        im = Image.fromarray(pixels)
        im.save(f"{os.path.splitext(file_name)[0]}_reshaped{os.path.splitext(file_name)[-1]}")


if __name__ == "__main__":
    main()
