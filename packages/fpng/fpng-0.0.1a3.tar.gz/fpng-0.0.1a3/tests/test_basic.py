import os.path as osp

import fpng

import cv2
import numpy as np
from PIL import Image


EXAMPLE_PNG = osp.join(osp.dirname(__file__), '../fpng/example.png')


def test_ndarray():
    img = Image.open(EXAMPLE_PNG)
    png = fpng.from_ndarray(np.asarray(img))

    with open('np.png', 'wb') as outf:
        outf.write(png)


def test_pil():
    img = Image.open(EXAMPLE_PNG)
    img.save('pil.png', 'FPNG')


def test_tofile():
    img = Image.open(EXAMPLE_PNG)

    if img.mode == "RGB":
        num_chan = 3
    elif img.mode == "RGBA":
        num_chan = 4
    else:
        raise OSError(f"cannot write mode {img.mode} as FPNG")

    # bool fpng_encode_image_to_file(const char* pFilename, const void* pImage, uint32_t w, uint32_t h, uint32_t num_chans, uint32_t flags)
    ret = fpng.fpng_ext.encode_image_to_file('tofile.png', img.tobytes(), img.width, img.height, num_chan, 0)

    assert ret


def test_cv2():
    img = cv2.imread(EXAMPLE_PNG)
    png = fpng.from_cv2(img)

    with open('cv2.png', 'wb') as outf:
        outf.write(png)


if __name__ == "__main__":
    test_ndarray()
    test_pil()
    test_tofile()
