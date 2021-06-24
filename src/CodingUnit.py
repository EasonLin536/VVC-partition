import numpy as np

MIN_CU_SIZE = 8

class CodingUnit:
    def __init__(self, x, y, width, height):
        # x, y is the coordinates of the CTU
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.children = []
        self.stop_split = False
        self.no_QT = False # MT node can no longer be partitioned by QT
    
    def get_coord(self):
        return self.x, self.y

    def get_size(self):
        return self.width, self.height

    def get_np_block(self, pil_img):
        luma_np = np.array(pil_img)
        block = luma_np[self.y : self.y + self.height, self.x : self.x + self.width]
        return block

    def terminate_split(self):
        self.stop_split = True

    def split_mode(self, index):
        if index == 0:
            self.split_QT()
        elif index == 1:
            self.split_BH()
        elif index == 2:
            self.split_BV()
        elif index == 3:
            self.split_TH()
        else:
            self.split_TV()
        
    def split_QT(self):
        w = self.width // 2
        h = self.height // 2

        if w < 4:
            self.terminate_split()
            return

        if self.no_QT:
            return

        for i in range(2):
            for j in range(2):
                x = self.x + w * i
                y = self.y + h * j
                child = CodingUnit(x, y, w, h)
                self.children.append(child)

        return self.children

    def split_BH(self):
        w = self.width
        h = self.height // 2

        if (h < MIN_CU_SIZE):
            self.terminate_split()
            return

        for i in range(2):
            x = self.x
            y = self.y + h * i
            child = CodingUnit(x, y, w, h)
            self.children.append(child)

        self.no_QT = True
        return self.children

    def split_BV(self):
        w = self.width // 2
        h = self.height

        if (w < MIN_CU_SIZE):
            self.terminate_split()
            return

        for i in range(2):
            x = self.x + w * i
            y = self.y
            child = CodingUnit(x, y, w, h)
            self.children.append(child)

        self.no_QT = True
        return self.children
        
    def split_TH(self):
        w = self.width
        h = self.height // 4

        if (h < MIN_CU_SIZE):
            self.terminate_split()
            return

        for i in range(3):
            x = self.x
            if i == 2:
                y = self.y + h * 3
            else:
                y = self.y + h * i
            if i == 1:
                child = CodingUnit(x, y, w, h * 2)
            else:
                child = CodingUnit(x, y, w, h)
            self.children.append(child)

        self.no_QT = True
        return self.children
        
    def split_TV(self):
        w = self.width // 4
        h = self.height

        if (w < MIN_CU_SIZE):
            self.terminate_split()
            return

        for i in range(3):
            y = self.y
            if i == 2:
                x = self.x + w * 3
            else:
                x = self.x + w * i
            if i == 1:
                child = CodingUnit(x, y, w * 2, h)
            else:
                child = CodingUnit(x, y, w, h)
            self.children.append(child)

        self.no_QT = True
        return self.children
        