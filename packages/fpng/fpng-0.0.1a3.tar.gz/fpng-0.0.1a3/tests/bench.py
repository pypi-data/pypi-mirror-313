import os
import os.path as osp
import timeit

from PIL import Image

import fpng


REPEAT = 10


img = Image.open('fpng/example.png')
img.load()


fp = open(os.devnull, "wb")

t = timeit.timeit(lambda: img.save(fp, format='png'), number=REPEAT)
print(f'on-memory PNG: {t:f} (sec)')

t = timeit.timeit(lambda: img.save(fp, format='fpng'), number=REPEAT)
print(f'on-memory fpng: {t:f} (sec)')


t = timeit.timeit(lambda: img.save('pil_png.png', format='png'), number=REPEAT)
print(f'write PNG: {t:f} (sec)')

t = timeit.timeit(lambda: img.save('pil_fpng.png', format='fpng'), number=REPEAT)
print(f'write fpng: {t:f} (sec)')


print(f'PNG size {osp.getsize("pil_png.png"):,} bytes')
print(f'fpng size {osp.getsize("pil_fpng.png"):,} bytes')
