# sweps-utils
Code utilities for SWEPS group

## Image stitching 

Example usage for image stitching:

```python

import numpy as np
import sweps_utils
import glob
from scipy import ndimage
from PIL import Image, ImageFilter
import matplotlib.pyplot as plt

# Directory where the .tif images are stored
imgdir = r'H:\a\1535eV-26'

# nsize: desired number of pixels on each image
# ncols: number of images along columns
# nrows: Number of images along rows
nsize = 128
ncols = 18
nrows = 25

# overlapping pixels along rows/columns
overlapr = 100
overlapc = 100

# selects all .tif files in the folder
files = glob.glob(r'{}\*.tif'.format(imgdir))
images = []
for file in files:
    # converts from uint16 to float
    img = Image.open(file).convert('F')
    
    # this filters by maximum value in a 3px window
    img = img.filter(ImageFilter.MaxFilter(3))
    
    # resize image if wanted to process faster
    if nsize < img.size[0]:
        img = img.resize((nsize, nsize))
        
    # cropping: (left, upper, left+width, upper+height)
    img = img.crop((0, 0, nsize, nsize))

    images.append(img)


stitched_image = sweps_utils.stitch(images, ncols, nrows, overlapr, overlapc)

img_copy = np.array(stitched_image)

# Gaussian blur filter
img_blur = ndimage.gaussian_filter(img_copy, sigma=0)

# Figure
f = plt.figure(figsize=(10, 10))
plt.imshow(img_blur, cmap='gray')
```
