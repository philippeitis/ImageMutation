from PIL import Image
import numpy as np


def ranges(size, max_val, start=0):
    """

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


def parse_args():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--files", "-f", dest="files", default=["../demo/nasa--hI5dX2ObAs-unsplash.jpg"], nargs="+",
                        help="File(s) to sort. Can be any format supported by PIL. ")
    parser.add_argument("--checkerboard", nargs=1, default=200,
                        help="Size of checkerboard pattern.")
    parser.add_argument("--crop_to_fit", action="store_true",
                        help="Crops the image to fit the checkerboard pattern.")
    return parser.parse_args()


def shift_row_wrapped(row: np.ndarray, shift_by: int):
    """ Shift pixels in row to the right. Pixels shifted off the end of the row become the first elements of the row.
     In place.

    :param row:             The list to modify - pixels will be circularly shifted in place.
    :param shift_by:        The amount to shift the elements by to the right (-ve if to the left).
    :return:                Nothing: operations are done in place.
    """

    row_len = row.shape[0]
    shift_by %= row_len
    shift_by = row_len - shift_by

    if shift_by == 0:
        return

    holding = np.copy(row)

    right_part = holding[shift_by:]
    left_part = holding[:shift_by]
    row[:row_len - shift_by] = right_part
    row[row_len - shift_by:] = left_part


def shift_rows_and_cols(image, rows_to_shift, cols_to_shift, shift_rows_by, shift_columns_by):
    """ Shifts all specified rows and columns (in rows_to_shift and cols_to_shift) by the specified amount. This wraps.

    SIDE EFFECTS: Will modify the input image - provide a copy to sort on if this is unwanted.

    :param shift_columns_by:    How many pixels to shift the specified columns by.
    :param shift_rows_by:       How many pixels to shift the specified rows by.
    :param cols_to_shift:       The specific columns in the image which should be shifted.
    :param rows_to_shift:       The specific rows in the image which should be shifted.
    :param image:               The image to modify.
    :return:                    Nothing. Image is modified in place - user is expected to provide a copy.
    """

    for row in rows_to_shift:
        shift_row_wrapped(image[row, :], shift_rows_by)

    for col in cols_to_shift:
        shift_row_wrapped(image[:, col], shift_columns_by)


def main():
    """ Program runner: parses the arguments and produces the appropriate images."""
    import os

    args = parse_args()

    for file_name in args.files:
        img = Image.open(file_name)
        pixels = np.copy(np.asarray(img))
        rows, cols, _ = pixels.shape

        if args.crop_to_fit:
            rows -= rows % args.checkerboard
            cols -= cols % args.checkerboard
            pixels = pixels[0:rows, 0:cols]

        shift_rows_and_cols(pixels, ranges(args.checkerboard, rows), ranges(args.checkerboard, cols),
                            2*args.checkerboard, args.checkerboard)

        im = Image.fromarray(pixels)
        im.save(f"{os.path.splitext(file_name)[0]}_shifted{os.path.splitext(file_name)[-1]}")


if __name__ == "__main__":
    main()
