import numpy as np
from itertools import product
from PIL import Image

# Creates a rows x cols matrix filled with val
def rect_img(val, rows, cols):
    return [[val for col in range(cols)] for row in range(rows)]

# Stitches a list of Pillow Images in a ncols x nrows
# grid with overlapping pixels along rows and columns
def stitch(images, ncols, nrows, overlapr, overlapc):
    img_rows = images[0].size[1]
    img_cols = images[0].size[0]
    new_rows = int(img_rows + (nrows - 1)*(img_rows - overlapr))
    new_cols = int(img_cols + (ncols - 1)*(img_cols - overlapc))
    img_list = [list(np.asarray(img)) for img in images]
    
    new_image  = rect_img(0, new_rows, new_cols)
    mask_total = rect_img(0, new_rows, new_cols)
    coordinates = list(product(range(nrows)[::-1], range(ncols)))

    for idx, t in enumerate(coordinates):
        row_paste = t[0]*(img_rows - overlapr)
        col_paste = t[1]*(img_cols - overlapc)
        
        rows_to_paste = range(row_paste, row_paste + img_rows)
        cols_to_paste = range(col_paste, col_paste + img_cols)
        
        for row in rows_to_paste:
            for col in cols_to_paste:
                if mask_total[row][col]:
                    new_image[row][col] = (new_image[row][col] + img_list[idx][row - row_paste][col - col_paste])/2
                else:
                    new_image[row][col] = img_list[idx][row - row_paste][col - col_paste]
                    mask_total[row][col] = 1
                    
    return Image.fromarray(np.asarray(new_image)).convert('F')
