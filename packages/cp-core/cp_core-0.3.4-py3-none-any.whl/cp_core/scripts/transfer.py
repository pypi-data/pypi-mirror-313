import pathlib

import imageio
from gui.config import Media


def transfer_to_gif(filename: pathlib.Path):
    im = imageio.imread(filename)
    print(filename.suffix)
    imageio.imwrite(str(filename)[:-4] + ".gif", im)


def main():
    for path in Media.get_image_list():
        p = pathlib.Path(path)
        if p.suffix != ".gif":
            transfer_to_gif(p)


if __name__ == "__main__":
    main()
