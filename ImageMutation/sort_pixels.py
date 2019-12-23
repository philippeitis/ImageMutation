from PIL import Image
import numpy as np
from image_utilities import brightness, select_random_rows

"""
Note that rows in the context of this code will refer to either a row or column if it is in the function name:
 eg. select_random_rows will randomly select a row or column depending on whether you provide it rows or columns.
 If it is not inside the function name, and is not specified in the arguments, rows refers to the rows in the image.
"""

BLACK_VAL = 60
WHITE_VAL = 150


def parse_args():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--files", "-f", dest="files", default=["../demo/nasa--hI5dX2ObAs-unsplash.jpg"], nargs="+",
                        help="File(s) to sort. Can be any format supported by PIL. ")
    parser.add_argument("--mode", "-m", dest="mode", default=1, type=int, choices=[0, 1, 2, 3],
                        help="0: Sorts on black levels\n"
                             "1: Sorts on brightness values\n"
                             "2: Sorts on white levels\n"
                             "3: Sorts on both both black and white levels.")
    # TODO: implement this.
    # parser.add_argument("--maintain_channel", type=str, nargs="?", choices=["r", "g", "b"],
    #                     help="Will not sort on the given channel.")
    parser.add_argument("--random_rows", action="store_true",
                        help="If selected, rows and columns will be randomly selected to be sorted.")
    parser.add_argument("--custom_interval", type=int, nargs="*", default=None,
                        help="Will start sorting on a number less than or equal to the first number supplied, and a"
                             "number higher than the second number supplied.")

    row_or_col = parser.add_mutually_exclusive_group()
    row_or_col.add_argument("--row_only", action="store_true",
                            help="Will only sort rows.")
    row_or_col.add_argument("--col_only", action="store_true",
                            help="Will only sort columns")

    args = parser.parse_args()
    if args.custom_interval:
        args.mode = -1
        if len(args.custom_interval) > 2:
            raise argparse.ArgumentParser("argument custom_interval requires between 1 and 2 arguments.")
        else:
            for light_level in args.custom_interval:
                if light_level < 0 or light_level > 255:
                    raise argparse.ArgumentParser("argument custom_interval requires numbers to be between 0 and 255.")

    return args


def get_non_black_index(x_start, row: np.ndarray):
    point = np.argmax(row[x_start:] > BLACK_VAL)
    if point == 0:
        return -1
    return point + x_start


def get_black_index(x_start, row: np.ndarray):
    point = np.argmax(row[x_start:] <= BLACK_VAL)
    if point == 0:
        return -1
    return point + x_start


def get_non_white_index(x_start, row: np.ndarray):
    """ Get first index that is not "white" past x_start. Returns -1 if no such index exists. """
    point = np.argmax(row[x_start:] < WHITE_VAL)
    if point == 0:
        return -1
    return point + x_start


def get_white_index(x_start, row: np.ndarray):
    """ Get first index that is "white" past x_start. Returns -1 if no such index exists. """
    point = np.argmax(row[x_start:] >= WHITE_VAL)
    if point == 0:
        return -1
    return point + x_start


def sort_pixel_list(row, compressed_row, sort_compressed=True):
    """ Sorts both row and compressed_row (if sort_compressed is True) based on compressed_row. """
    sorted_indices = np.argsort(compressed_row)
    row[:, 0] = row[:, 0][sorted_indices]
    row[:, 1] = row[:, 1][sorted_indices]
    row[:, 2] = row[:, 2][sorted_indices]

    # This produces interesting effects when disabled.
    if sort_compressed:
        compressed_row[:] = compressed_row[sorted_indices]


def sort_row(row, compressed_row, start_point_fn, end_point_fn):
    """ Sorts the row based on compressed_row, using start_point_fn and end_point_fn to determine where to start, and
    stop sorting a given region. """
    len_row = len(row)
    x_start = start_point_fn(0, compressed_row)
    while x_start != len_row and x_start != -1:
        x_end = end_point_fn(x_start, compressed_row)
        if x_end == -1:
            x_end = len_row
        sort_pixel_list(row[x_start:x_end], compressed_row[x_start:x_end])
        if x_end == len_row:
            break
        x_start = start_point_fn(x_end, compressed_row)


def sort_intervals(image, compressed_image, start_point_fn, end_point_fn,
                   iterator=range, sort_cols=True, sort_rows=True):
    """ Sorts the row on each interval starting with start_point_fn's output, and ending on end_point_fn's output.
    Expects end_point_fn to produce values that occur after start_point_fn. If sort_cols or sort_rows specified, will
    sort the columns and rows in the image. Compressed image should be a row x col array, where each element contains a
    given pixels weight, to be used for sorting.

    SIDE EFFECTS: Will modify the input image - provide a copy to sort on if this is unwanted.

    :param iterator:            An iterable which yields a number from 0 to rows - 1, and yields each number at most
                                once.
    :param image:               The image to modify.
    :param compressed_image:    The array with the same number of rows and columns as image, where each element is
                                the weight of the pixel compared to its neighbours (higher pixels will be sorted to the
                                end).
    :param start_point_fn:      A function which produces some start point given a point and a complete row.
    :param end_point_fn:        A function which produces an end point occurring after the start point, given the start
                                point and complete row.
    :param sort_cols:           Will sort cols if set to True.
    :param sort_rows:           Will sort rows if set to True.
    :return:                    Nothing. Image is modified in place - user is expected to provide a copy.
    """

    rows, cols, _ = image.shape

    if sort_cols:
        for col in iterator(cols):
            sort_row(image[:, col], compressed_image[:, col], start_point_fn, end_point_fn)
    if sort_rows:
        for row in iterator(rows):
            sort_row(image[row, :], compressed_image[row, :], start_point_fn, end_point_fn)


def main():
    """ Program runner: parses the arguments and produces the appropriate images."""
    import os

    args = parse_args()
    iterator = select_random_rows if args.random_rows else range

    if args.custom_interval:
        def interval_start_fn(x_start, row: np.ndarray):
            point = np.argmax(row[x_start:] >= args.custom_interval[0])
            if point == 0:
                return -1
            return point + x_start

        if len(args.custom_interval) == 2:
            def interval_end_fn(x_start, row: np.ndarray):
                point = np.argmax(row[x_start:] < args.custom_interval[1])
                if point == 0:
                    return -1
                return point + x_start
        else:
            def interval_end_fn(x_start, row: np.ndarray):
                point = np.argmax(row[x_start:] < args.custom_interval[0])
                if point == 0:
                    return -1
                return point + x_start

    for file_name in args.files:
        img = Image.open(file_name)
        pixels = np.copy(np.asarray(img))
        pixels_compressed = brightness(pixels)

        if args.custom_interval:
            sort_intervals(pixels, pixels_compressed, interval_start_fn, interval_end_fn, iterator,
                           not args.row_only, not args.col_only)
        else:
            if args.mode == 0 or args.mode == 3:
                print("sorting on black")
                sort_intervals(pixels, pixels_compressed, get_black_index, get_non_black_index, iterator,
                               not args.row_only, not args.col_only)
            if args.mode == 2 or args.mode == 3:
                print("sorting on white")
                sort_intervals(pixels, pixels_compressed, get_white_index, get_non_white_index, iterator,
                               not args.row_only, not args.col_only)
            if args.mode == 1:
                # start_fn: returns 0 on entering loop
                # end_fn: returns the length - sorts the entire list
                # start_fn: x is returned, and x is end.
                sort_intervals(pixels, pixels_compressed, lambda x, y: x, lambda x, y: len(y), iterator,
                               not args.row_only, not args.col_only)

        im = Image.fromarray(pixels)
        im.save(f"{os.path.splitext(file_name)[0]}_sorted{os.path.splitext(file_name)[-1]}")


if __name__ == "__main__":
    main()
