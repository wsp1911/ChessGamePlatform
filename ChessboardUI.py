import os
import cv2 as cv
from ChessboardFactory import ChessboardFactory
from Memento import Memento


class ChessboardUI:

    def __init__(self, img_frame) -> None:
        self.img_frame = img_frame
        self.chessboard_factory = ChessboardFactory()
        self.chessboard = None
        self.game_type = 0

        self.pass_cnt = 0
        self.cur_player = -1
        self.winner = 0  # 0是未分胜负，2是平局

        self.path_resources = "./resources"
        self.img_chessboard = None
        self.img = None
        self.img_piece = {}

        self.img_w = self.img_frame.geometry().width() - 2 * self.img_frame.get_border()
        self.img_w1 = 0
        self.img_stone_w = 0
        self.img_stone_offset = 0
        self.img_lu_offset = 0

    def gen_snapshot(self, memento: Memento):
        states = [self.game_type, self.cur_player, self.pass_cnt, self.winner, self.get_size()]
        memento.save_state(type(self), states)
        self.chessboard.gen_snapshot(memento)

    def restore_from_snapshot(self, memento: Memento):
        states = memento.get_state(type(self))
        self.game_type = states[0]
        self.cur_player = states[1]
        self.pass_cnt = states[2]
        self.winner = states[3]
        if self.chessboard is None:
            size = states[-1]
            self.gen_chessboard(self.game_type, size)
        self.chessboard.restore_from_snapshot(memento)
        self.update_img()

    def reset(self):
        self.cur_player = -1
        self.pass_cnt = 0
        self.winner = 0
        self.chessboard.reset()
        self.img = self.img_chessboard.copy()
        self.update_img()

    def get_size(self):
        return self.chessboard.get_size()

    def get_counts(self):
        return self.chessboard.get_counts()

    def get_winner(self):
        return self.winner

    def get_cur_player(self):
        return self.cur_player

    def get_gametype(self):
        return self.game_type

    def exchange_player(self):
        self.cur_player = -self.cur_player

    def load_piece_img(self, s):
        path = os.path.join(self.path_resources, "white.jpg")
        self.img_piece[1] = cv.cvtColor(cv.imread(path), cv.COLOR_BGR2RGB)
        path = os.path.join(self.path_resources, "black.jpg")
        self.img_piece[-1] = cv.cvtColor(cv.imread(path), cv.COLOR_BGR2RGB)
        path = os.path.join(self.path_resources, "mask.jpg")
        self.img_piece["mask"] = cv.imread(path)
        for i in [-1, 1, "mask"]:
            self.img_piece[i] = cv.resize(self.img_piece[i], (s, s))
        self.img_piece["~mask"] = 1 - self.img_piece["mask"]

    def load_chessboard_bg(self, size: int):
        path = os.path.join(self.path_resources, "%d.jpg" % size)
        self.img_chessboard = cv.imread(path)
        self.img_chessboard = cv.cvtColor(self.img_chessboard, cv.COLOR_BGR2RGB)
        self.img_chessboard = cv.resize(self.img_chessboard, (self.img_w, self.img_w))
        self.img = self.img_chessboard.copy()

    def load_chessboard_imgs(self, game_type: int = -1, size: int = -1):
        if game_type == -1:
            game_type = self.game_type
        if size == -1:
            size = self.get_size()
        if game_type != 2:
            self.img_w1 = self.img_w / size
            self.img_stone_w = int(self.img_w1 * 0.9)
            self.img_stone_offset = (self.img_w1 - self.img_stone_w) / 2
            self.img_lu_offset = 0
            self.load_piece_img(self.img_stone_w)
            self.load_chessboard_bg(size)
        else:
            s = size + 1
            self.img_w1 = self.img_w / s
            self.img_stone_w = int(self.img_w1 * 0.9)
            self.img_stone_offset = self.img_w1 - self.img_stone_w / 2
            self.img_lu_offset = self.img_w1 / 2
            self.load_piece_img(self.img_stone_w)
            self.load_chessboard_bg(s)

    def gen_chessboard(self, game_type: int, size: int):
        self.game_type = game_type
        self.load_chessboard_imgs(game_type, size)
        self.chessboard = self.chessboard_factory.create_chessboard(game_type, size)
        self.update_img()
        self.reset()

    def add_stone_img_to(self, r, c, color):
        x = int(r * self.img_w1 + self.img_stone_offset)
        y = int(c * self.img_w1 + self.img_stone_offset)
        copy = self.img[x:x + self.img_stone_w, y:y + self.img_stone_w]
        self.img[x:x + self.img_stone_w, y:y +
                 self.img_stone_w] = self.img_piece["mask"] * self.img_piece[color] + self.img_piece["~mask"] * copy

    def update_img(self):
        self.img = self.img_chessboard.copy()
        s = self.chessboard.get_size()
        for i in range(s):
            for j in range(s):
                c = self.chessboard.get_xy(i, j)
                if c:
                    self.add_stone_img_to(i, j, c)

        self.img_frame.setImage(self.img)

    def make_move(self, x: int, y: int):
        if self.chessboard.make_move(x, y, self.cur_player):
            self.update_img()
            return True
        return False

    def play_stone(self, x, y):
        x -= self.img_lu_offset
        y -= self.img_lu_offset
        cx, cy = x / self.img_w1, y / self.img_w1
        xi, yi = int(cx), int(cy)
        if abs(cx - xi - 0.5) < 0.3 and abs(cy - yi - 0.5) < 0.3:
            if self.make_move(xi, yi):
                self.pass_cnt = 0  # 虚着计数归零
                if self.chessboard.check(xi, yi):
                    self.winner = self.cur_player
                self.exchange_player()
                return True
        return False

    def pass_(self):
        if self.game_type == 0:
            return False

        if self.pass_cnt == 1:
            n1, n2 = self.get_counts()
            if n1 > n2:
                self.winner = 1
            elif n1 < n2:
                self.winner = -1
            else:
                self.winner = 2
            return True

        self.pass_cnt += 1
        self.exchange_player()
        return True
