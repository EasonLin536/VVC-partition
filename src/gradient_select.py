import numpy as np
from scipy.ndimage import filters

TH_2 = 2.7
TH_3 = 50000

def gradient_select(luma_img, CU):

    block = CU.get_np_block(luma_img)

    img_x = filters.sobel(block, 1)
    img_y = filters.sobel(block, 0)
    D_x = np.sum(abs(img_x))
    D_y = np.sum(abs(img_y))

    if D_x > TH_3 and D_y > TH_3:
        if D_x / D_y < TH_2 or D_y / D_x < TH_2:
            return True
    else:
        return False
