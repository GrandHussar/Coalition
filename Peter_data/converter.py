import numpy as np
from PIL import Image

im = np.array(Image.open('sample_photo_2.pgm'))

print(im.shape)