import numpy as np
from itertools import product
from PIL import Image

# Creates a rows x cols matrix filled with val
def rect_img(val, rows, cols):
    return [[val for col in range(cols)] for row in range(rows)]

# Stitches a list of Pillow Images in a ncols x nrows
# grid with overlapping pixels along rows and columns
def stitch(images, ncols, nrows, overlapr, overlapc):

    # Image sizes
    img_rows = images[0].size[1]
    img_cols = images[0].size[0]
    
    # New total image size taking overlapping into account
    new_rows  = int(img_rows + (nrows - 1)*(img_rows - overlapr))
    new_cols  = int(img_cols + (ncols - 1)*(img_cols - overlapc))
    new_image = rect_img(0, new_rows, new_cols)
    
    # Converts Pillow image to an numpy array then to a python list
    img_list = [list(np.asarray(img)) for img in images]

    # Mask is an array with the same shape as the output image,
    # but filled with 0/1, which controls if the specific pixels
    # have been already used or not in the final image.
    mask_total = rect_img(0, new_rows, new_cols)
    
    # List of (row,col) coordinates of where to paste each image.
    # Runs backwards along the rows since the scanning is done
    # bottom-to-top and left-to-right.
    coordinates = list(product(range(nrows)[::-1], range(ncols)))
    
    # Loops over the coordinates
    for img_index, img_coords in enumerate(coordinates):
        # Top-left corner coordinate of where to paste
        row_paste = img_coords[0]*(img_rows - overlapr)
        col_paste = img_coords[1]*(img_cols - overlapc)
        
        # List of pixels that should be pasted
        rows_to_paste = range(row_paste, row_paste + img_rows)
        cols_to_paste = range(col_paste, col_paste + img_cols)
        
        # Loop over all pixels that should be pasted onto the final
        # image. If the pixel in the final image has already been
        # used (mask = 1), its value is set to the (current+new)/2.
        # Otherwise, it is set to the new pixel value and marks the mask.
        for row in rows_to_paste:
            for col in cols_to_paste:
                new_image[row][col] += img_list[img_index][row - row_paste][col - col_paste]
                mask_total[row][col] += 1
    
    return Image.fromarray(np.array(new_image)/np.array(mask_total)).convert('F')
