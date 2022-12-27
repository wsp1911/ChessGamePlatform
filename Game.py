import sys
from GameUI import GameUI, QApplication
from ChessboardUI import ChessboardUI
from Memento import Memento
from collections import deque


class Game(GameUI):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.IN_GAME = False
        self.chessboard = ChessboardUI(self.img_frame)
        self.game_types = ["五子棋", "围棋", "黑白棋"]
        self.players = {1: "白方", -1: "黑方"}
        self.snapshots = deque()
        self.connect()

    def connect(self):
        self.img_frame.connect_mouse_pressed_to(self.on_mouse_pressed)
        self.btn_gen_chessboard.clicked.connect(self.on_btn_gen_chessboard_clicked)
        self.btn_start_game.clicked.connect(self.on_btn_start_game_clicked)
        self.btn_pass.clicked.connect(self.on_btn_pass_clicked)
        self.btn_admit_defeat.clicked.connect(self.on_btn_admit_defeat_clicked)
        self.btn_retract.clicked.connect(self.on_btn_retract_clicked)
        self.btn_save_game.clicked.connect(self.on_btn_save_game_clicked)
        self.btn_load_game.clicked.connect(self.on_btn_load_game_clicked)

    def start_game(self):
        self.IN_GAME = True
        self.gen_snapshot()  # 初始快照
        self.msg = []
        self.msg.append("对局开始")
        self.msg.append("对局类型：" + self.game_types[self.chessboard.get_gametype()])
        self.msg.append("当前落子方：" + self.players[self.chessboard.get_cur_player()])
        self.show_msg()

    def in_game(self):
        return self.IN_GAME

    def stop_game(self):
        self.IN_GAME = False
        self.msgbox.clear()

    def gen_snapshot(self):
        memento = Memento()
        self.chessboard.gen_snapshot(memento)
        self.snapshots.append(memento)

    def post_action(self):
        """落子或虚着后的一系列处理，包括生成快照，判断胜负，更新提示信息"""
        self.gen_snapshot()
        winner = self.chessboard.get_winner()
        if winner:
            game_type = self.chessboard.get_gametype()
            n1, n2 = self.chessboard.get_counts()
            s = ""
            if game_type != 0:
                s += "白子%d，黑子%d；" % (n1, n2)
            if winner == 2:
                s += "平局！"
            else:
                s += "%s获胜！" % self.players[winner]
            self.show_dialog("about", "结果", s)
            self.stop_game()
        else:
            self.msg[-1] = "当前落子方：" + self.players[self.chessboard.get_cur_player()]
            self.show_msg()

    def on_mouse_pressed(self, x, y):
        if not self.in_game():
            self.show_dialog("warning", "警告", "尚未开始游戏，无法落子！")
            return

        self.chessboard.play_stone(x, y)
        self.post_action()

    def on_btn_pass_clicked(self):
        if not self.in_game():
            self.show_dialog("warning", "警告", "尚未开始游戏！")
            return

        success = self.chessboard.pass_()
        if not success:
            self.show_dialog("warning", "警告", "当前模式不能虚着！")
            return

        self.post_action()

    def on_btn_gen_chessboard_clicked(self):
        game_type = self.cb_game_type.currentIndex()
        size = int(self.cb_board_size.currentText())
        self.chessboard.gen_chessboard(game_type, size)
        self.start_game()

    def on_btn_start_game_clicked(self):
        if self.chessboard is None:
            self.show_dialog("warning", "警告", "请先生成棋盘！")
            return
        self.chessboard.reset()
        self.start_game()

    def on_btn_retract_clicked(self):
        if not self.in_game():
            self.show_dialog("warning", "警告", "尚未开始游戏！")
            return

        if len(self.snapshots) <= 1:
            self.show_dialog("warning", "警告", "尚未落子！")
            return

        if self.show_dialog("question", "提示", "确定悔棋吗？"):
            self.snapshots.pop()
            self.chessboard.restore_from_snapshot(self.snapshots[-1])

    def on_btn_admit_defeat_clicked(self):
        if self.in_game():
            i = self.chessboard.get_cur_player()
            self.show_dialog("about", "结果", "{}认负，{}获胜".format(self.players[i], self.players[-i]))
            self.stop_game()
        else:
            self.show_dialog("warning", "警告", "尚未开始游戏！")

    def on_btn_save_game_clicked(self):
        if not self.in_game():
            self.show_dialog("warning", "警告", "尚未开始游戏！")
            return

        fpath = self.get_save_path(filter="BIN(*.bin)")
        if fpath:
            self.snapshots[-1].save_to_disk(fpath)

    def on_btn_load_game_clicked(self):
        if self.in_game() and not self.show_dialog("warning", "警告", "对局进行中，确定载入吗？"):
            return

        fpath = self.get_open_path(filter="BIN(*.bin)")
        if fpath:
            memento = Memento()
            memento.restore_from_disk(fpath)
            self.chessboard.restore_from_snapshot(memento)
            self.chessboard.load_chessboard_imgs()
            self.start_game()
            self.snapshots = [memento]


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Game()
    window.show()
    app.exec()
