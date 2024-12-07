# py-fpng-nb
# https://github.com/dofuuz/py-fpng-nb
#
# SPDX-FileCopyrightText: (c) 2024 KEUM Myungchul
# SPDX-License-Identifier: MIT
#
# Fast PNG writer for Python.
# py-fpng-nb is a Python wrapper of fpng(https://github.com/richgel999/fpng).

# for this file only: 
# Original code from python-fpnge(https://github.com/animetosho/python-fpnge) (Public domain)


from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import IO
    from numpy.typing import NDArray
    from PIL.Image import Image
    from cv2 import Mat

import lazy_loader as lazy

from . import fpng_ext
from ._version import __version__


cv2 = lazy.load('cv2')
fpng_ext.init()


def from_pil(im: 'Image') -> bytes:
    # make sure image data is available
    im.load()

    mode_map = {
      "RGB":  (3, 8),
      "RGBA": (4, 8),
    }
    if im.mode not in mode_map:
        conv_map = {
          "1": "RGB",
          "P": "RGBA",
          "CMYK": "RGB",
          "YCbCr": "RGB",
          "LAB": "RGB",
          "HSV": "RGB",
          "LA": "RGBA",
          "RGBa": "RGBA",
          "La": "RGBA",
        }
        im = im.convert(mode=conv_map[im.mode])

    png = fpng_ext.encode_image_to_memory(im.tobytes(), im.width, im.height, mode_map[im.mode][0])
    return png


def _save_pil(im: 'Image', fp: IO[bytes], filename) -> None:
    png = from_pil(im)
    fp.write(png)

    if hasattr(fp, "flush"):
        fp.flush()


try:
    import PIL.Image

    PIL.Image.register_save("FPNG", _save_pil)
    # Image.register_extension("FPNG", ".png")
    # Image.register_mime("FPNG", "image/png")
except ImportError:
    pass


def from_bytes(dat: bytes, width: int, height: int, channels: int) -> bytes:
    png = fpng_ext.encode_image_to_memory(dat, width, height, channels)
    return png


def from_ndarray(ndarray: 'NDArray') -> bytes:
    if ndarray.ndim != 3:
        raise AttributeError("Must have 3 dimensions (height x width x channels)")

    png = fpng_ext.encode_ndarray(ndarray)
    return png


def from_cv2(mat: 'Mat') -> bytes:
    if mat.ndim != 3:
        raise Exception("Must have 3 dimensions (width x height x channels)")
    # cv2 Mats are BGR, needs to be RGB:
    mat = cv2.cvtColor(mat, cv2.COLOR_BGR2RGB)
    if mat.dtype == 'uint16':
        raise AttributeError("fpng supports 24bpp or 32bpp")

    png = fpng_ext.encode_ndarray(mat)
    return png
