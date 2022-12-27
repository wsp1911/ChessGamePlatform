import numpy as np
from abc import ABC, abstractmethod
from Memento import Memento


class Chessboard(ABC):

    def __init__(self, size: int, border: int):
        self._size = size
        self._border = border
        s = size + 2 * border
        self._board = 2 * np.ones((s, s), dtype=int)
        self._board[border:-border, border:-border] = np.zeros((size, size), dtype=int)

    def reset(self):
        w = self._border
        s = self._size
        self._board[w:-w, w:-w] = np.zeros((s, s), dtype=int)

    def gen_snapshot(self, memento: Memento):
        states = [self._size, self._border]
        whites, blacks = [], []
        for i in range(self._size):
            for j in range(self._size):
                c = self.get_xy(i, j)
                if c == 1:
                    whites.append((i, j))
                elif c == -1:
                    blacks.append((i, j))
        states.append(whites)
        states.append(blacks)
        memento.save_state(type(self), states)

    def restore_from_snapshot(self, memento: Memento):
        states = memento.get_state(type(self))
        self._size = states[0]
        self._border = states[1]
        s = self._size + 2 * self._border
        self.reset()
        for i, j in states[2]:
            self.set_xy(i, j, 1)
        for i, j in states[3]:
            self.set_xy(i, j, -1)

    def get_xy(self, x: int, y: int):
        return self._board[x + self._border, y + self._border]

    def get_size(self):
        return self._size

    def get_valid_board(self):
        return self._board[self._border:-self._border, self._border:-self._border].copy()

    def set_xy(self, x: int, y: int, color: int):
        self._board[x + self._border, y + self._border] = color

    def get_counts(self):
        copy = self.get_valid_board()
        n1 = (copy == 1).sum()
        n2 = (copy == -1).sum()
        return n1, n2

    @abstractmethod
    def check(self, x: int, y: int):
        pass

    @abstractmethod
    def validate(self, x: int, y: int, color: int) -> int:
        """检查(x,y)是否可以落子，0表示非法，大于1为合法
        """
        pass

    @abstractmethod
    def make_move(self, x: int, y: int, color: int):
        pass