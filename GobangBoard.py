from Chessboard import Chessboard


class GobangBoard(Chessboard):

    def __init__(self, size: int):
        super().__init__(size, 4)
        self._dx = [1, 0, 1, 1]
        self._dy = [0, 1, 1, -1]
    
    def validate(self,x,y,color):
        if self.get_xy(x, y) == 0:
            return 1
        return 0

    def check(self, x: int, y: int):
        center = self.get_xy(x, y)
        for i in range(4):
            cnt1, cnt2 = 0, 0

            for j in range(1, 5):
                if self.get_xy(x + self._dx[i] * j, y + self._dy[i] * j) != center:
                    break
                cnt1 += 1

            for j in range(1, 5):
                if self.get_xy(x - self._dx[i] * j, y - self._dy[i] * j) != center:
                    break
                cnt2 += 1

            if cnt1 + cnt2 >= 4:
                return center
        return 0

    def make_move(self, x: int, y: int, color: int):
        if self.validate(x,y,color):
            self.set_xy(x, y, color)
            return True
        return False
