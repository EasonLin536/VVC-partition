from CodingUnit import CodingUnit
import numpy as np

TH_1 = 300

def early_terminate(luma_img, CU):
    
    block = CU.get_np_block(luma_img)
    # print("block [{}:{}, {}:{}] var = {}".format(CU.x, CU.x + CU.width, \
        # CU.y, CU.y + CU.height, block.var()))
    if block.var() < TH_1:
        CU.terminate_split()
        return True 
    else:
        return False
