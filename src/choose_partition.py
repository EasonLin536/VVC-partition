import copy
from math import nan
import numpy as np

def choose_partition(img, CU):

    # Copy the current coding unit for 5 different partitions
    max_var = 0
    max_idx = 0
    if CU.no_QT:
        start = 1
    else:
        start = 0
    for i in range(start, 5):
        CU_copy = copy.deepcopy(CU)
        CU_copy.split_mode(i)
        if CU_copy.children:
            var = []
            for child in CU_copy.children:
                var.append(child.get_np_block(img).var())
            if (np.array(var)).var() > max_var:
                max_var = (np.array(var)).var()
                max_idx = i

    return max_idx