```python
import ...


def parse_args():
    import argparse
    parser.add_argument("--files", "-f", default=["../demo/source_file.jpg"],
                    nargs="+",
                    help="File(s) to apply a mountain effect to. Can be any format supported by PIL. ")

    # Further arguments specified here.

    # OPTIONAL: Parse the arguments to ensure correctness

    return parser.parse_args()


def apply_effect_name_effect_row(row, compressed_row):
    # Do something with the row. Should be in place

    mod_row = [0] * len(compressed_row)

    ...

    row[:] = mod_row[:]


def apply_effect_name_effect(image, compressed_image, *args, **kwargs):
    """ General details about effect.

    SIDE EFFECTS: Will modify the input image - provide a copy to apply the effect on if this is unwanted.

    :param image:               The image to modify.
    :param compressed_image:    The array with the same number of rows and columns as image, where each element is
                                the weight of the pixel compared to its neighbours.
    :param *args:               Description for each argument.
    :param **kwargs:            Description for each argument.
    :return:                    Nothing. Image is modified in place - user is expected to provide a copy.
    """

    rows, cols, _ = image.shape

    ...


def main():
    """ Program runner: parses the arguments and produces the appropriate images."""
    import os

    args = parse_args()
    for file_name in args.files:
        img = Image.open(file_name)
        pixels = np.copy(np.asarray(img))

        apply_effect_name_effect(pixels, pixels_compressed, *args, **kwargs)

        im = Image.fromarray(pixels)
        im.save(f"{os.path.splitext(file_name)[0]}_effect_name{os.path.splitext(file_name)[-1]}")


if __name__ == "__main__":
    main()
```
