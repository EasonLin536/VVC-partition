import sys
import math
from PIL import Image, ImageDraw
from CodingUnit import CodingUnit
from early_terminate import *
from gradient_select import *
from choose_partition import *

CTU_SIZE = 128
MAX_DEPTH = 4

# Read image and crop to size
def read_image(img_fname):
    pil_img = Image.open(img_fname)
    width, height = pil_img.size
    excess_width = width - (width // CTU_SIZE) * CTU_SIZE
    excess_height = height - (height // CTU_SIZE) * CTU_SIZE
    x = math.floor(excess_width / 2)
    y = math.floor(excess_height / 2)
    pil_img = pil_img.crop((x, y, x + (width // CTU_SIZE) * CTU_SIZE, y + (height // CTU_SIZE) * CTU_SIZE))

    return pil_img

# Split into CTU_SIZE * CTU_SIZE pixels
def split_CTU(pil_img):
    width, height = pil_img.size
    col = width // CTU_SIZE
    row = height // CTU_SIZE
    CTU_num = col * row

    CTU = []
    cnt = 1
    for i in range(col):
        for j in range(row):
            x = i * CTU_SIZE
            y = j * CTU_SIZE
            CU = CodingUnit(x, y, CTU_SIZE, CTU_SIZE)
            CTU.append(CU)
            print("Splitting into CTUs [{}/{}]".format(cnt, CTU_num), flush=True, end='\r')
            cnt += 1
    print("")
    return CTU

# Draw blocks
def draw_block(pil_img, CU):
    draw = ImageDraw.Draw(pil_img)
    x, y = CU.get_coord()
    w, h = CU.get_size()
    draw.line((x, y, x + w, y), fill=100, width=1)
    draw.line((x, y, x, y + h), fill=100, width=1)
    draw.line((x + w, y, x + w, y + h), fill=100, width=1)
    draw.line((x, y + h, x + w, y + h), fill=100, width=1)
    for child in CU.children:
        pil_img = draw_block(pil_img, child)

    return pil_img

def draw_recursive(pil_img, CU):
    block_img = draw_block(pil_img, CU)
    return block_img

def partition(img, CU, depth):
    if depth > MAX_DEPTH:
        return

    # STEP 1. EARLY TERMINATION BASED ON VARIANCE
    if early_terminate(img, CU):
        return
    # STEP 2. CHOOSING QT BASED ON GRADIENT
    if gradient_select(img, CU) and not CU.no_QT:
        CU.split_QT()
    # STEP 3. CHOOSING ONE PARTITION FROM FIVE CANDIDATES BASED ON VARIANCE OF VARIANCE
    else:
        idx = choose_partition(img, CU)
        CU.split_mode(idx)

    # Recursive
    for C in CU.children:
        partition(img, C, depth+1)

    return

if __name__ == '__main__':
    pil_img = read_image(sys.argv[1])
    luma_img = pil_img.convert('L')
    CTU = split_CTU(luma_img)
    cnt = 1
    for CU in CTU:
        print("Partition of CTUs [{}/{}]".format(cnt, len(CTU)), flush=True, end='\r')
        partition(luma_img, CU, 1)
        cnt += 1
    print("")

    for CU in CTU:
        pil_img = draw_recursive(pil_img, CU)
    pil_img.save(sys.argv[2])
