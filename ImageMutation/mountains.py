from PIL import Image
import numpy as np
from image_utilities import brightness


def parse_args():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--files", "-f", default=["../demo/alexander-andrews--Bq3TeSBRdE-unsplash.jpg"],
                        nargs="+",
                        help="File(s) to apply a mountain effect to. Can be any format supported by PIL. ")
    parser.add_argument("--direction", "-d", dest="direction", type=str, default="up",
                        choices=["down", "up", "left", "right"],
                        help="Direction that mountains will go.")
    parser.add_argument("--darkness", "--dark", dest="darkness", action="store_true",
                        help="Instead of using brightness (eg. height of maximum rgb value), will use darkness to "
                             "determine height.")
    # TODO: implement valleys.
    # parser.add_argument("--valleys", "-v", dest="valleys", action="store_true",
    #                     help="Instead of mountains, produces valleys.")

    return parser.parse_args()


def apply_mountain_effect_row(row, compressed_row):
    copy_row = np.copy(row)
    row_len = len(row)
    max_height = row_len
    # max_height is a bit of a misnomer: max_height is actually supposed to decrease, but it's the maximum height as you
    # view the image: for instance, if max_height = 0, then you're looking at the top pixel.

    for pix, height, i in zip(row[::-1], compressed_row[::-1], range(row_len - 1, -1, -1)):
        top_pixel = max(0, i - height)
        copy_row[top_pixel:max_height, 0] = pix[0]
        copy_row[top_pixel:max_height, 1] = pix[1]
        copy_row[top_pixel:max_height, 2] = pix[2]
        max_height = min(max_height, top_pixel)

    row[:] = copy_row[:]


def apply_mountain_effect(image, compressed_image, direction="down"):
    """

    SIDE EFFECTS: Will modify the input image - provide a copy to apply the effect on if this is unwanted.

    :param direction:           Direction in which the height map is applied.
    :param image:               The image to modify.
    :param compressed_image:    The array with the same number of rows and columns as image, where each element is
                                the weight of the pixel compared to its neighbours (higher pixels will be sorted to the
                                end).
    :return:                    Nothing. Image is modified in place - user is expected to provide a copy.
    """

    rows, cols, _ = image.shape

    if direction == "up":
        for col in range(cols):
            apply_mountain_effect_row(image[:, col], compressed_image[:, col])
    elif direction == "down":
        for col in range(cols):
            apply_mountain_effect_row(image[:, col][::-1], compressed_image[:, col][::-1])
    elif direction == "left":
        for row in range(rows):
            apply_mountain_effect_row(image[row, :], compressed_image[row, :])
    elif direction == "right":
        for row in range(rows):
            apply_mountain_effect_row(image[row, :][::-1], compressed_image[row, :][::-1])


def main():
    """ Program runner: parses the arguments and produces the appropriate images."""
    import os

    args = parse_args()
    for file_name in args.files:
        img = Image.open(file_name)
        pixels = np.copy(np.asarray(img))
        if args.darkness:
            pixels_compressed = 255 - brightness(pixels)
        else:
            pixels_compressed = brightness(pixels)

        apply_mountain_effect(pixels, pixels_compressed, args.direction)

        im = Image.fromarray(pixels)
        im.save(f"{os.path.splitext(file_name)[0]}_mountains{os.path.splitext(file_name)[-1]}")


if __name__ == "__main__":
    main()
