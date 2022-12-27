from Chessboard import Chessboard


class OthelloBoard(Chessboard):

    def __init__(self, size: int):
        super().__init__(size, 1)
        self._offset = [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [-1, -1], [1, -1], [-1, 1]]
        self.set_xy(3,3,1)
        self.set_xy(4,4,1)
        self.set_xy(3,4,-1)
        self.set_xy(4,3,-1)
        
    def reset(self):
        super().reset()
        self.set_xy(3,3,1)
        self.set_xy(4,4,1)
        self.set_xy(3,4,-1)
        self.set_xy(4,3,-1)

    def check(self, x: int, y: int):
        return False

    def validate(self, x: int, y: int, color: int):
        c2 = -color
        valid = 0
        for dx, dy in self._offset:
            i = 1
            while self.get_xy(x + i * dx, y + i * dy) == c2:
                i += 1
            if self.get_xy(x + i * dx, y + i * dy) != color:  #空格或边界
                continue
            if i==1: # 和同色子相邻
                continue
            valid = 1
            for j in range(1, i):
                self.set_xy(x + j * dx, y + j * dy, color)
        return valid

    def make_move(self, x: int, y: int, color: int):
        if self.validate(x,y,color):
            self.set_xy(x,y,color)
            return True
        return False
