from PyQt6.QtWidgets import (
    QLabel,
    QPushButton,
    QApplication,
    QMainWindow,
    QComboBox,
    QMessageBox,
    QTextBrowser,
    QFileDialog,
)
import sys
from Widgets import ImageViewFrame, GroupBoxLayout

Yes = QMessageBox.StandardButton.Yes
No = QMessageBox.StandardButton.No
Ok = QMessageBox.StandardButton.Ok
Cancel = QMessageBox.StandardButton.Cancel


class GameUI(QMainWindow):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.setWindowTitle("战棋平台")

        self.img_frame = ImageViewFrame(self)

        self.cb_board_size = QComboBox()
        self.cb_board_size.addItems([str(i) for i in range(8, 20)])
        self.cb_game_type = QComboBox()
        self.cb_game_type.addItems(["五子棋", "围棋", "黑白棋"])
        self.btn_load_game = QPushButton("载入对局")
        self.btn_gen_chessboard = QPushButton("生成棋盘")
        self.btn_start_game = QPushButton("重新开始")
        self.btn_pass = QPushButton("虚着")
        self.btn_retract = QPushButton("悔棋一步")
        self.btn_admit_defeat = QPushButton("投子认负")
        self.btn_save_game = QPushButton("保存局面")
        self.msgbox = QTextBrowser()
        self.msgbox.setMaximumHeight(200)

        self.msg = []

        self.qgb = GroupBoxLayout(self)
        self.qgb.addRow((QLabel("对局模式"), self.cb_game_type))
        self.qgb.addRow((QLabel("棋盘尺寸"), self.cb_board_size))
        self.qgb.addRow((self.btn_gen_chessboard, ), (2, ))
        self.qgb.addRow((self.btn_start_game, ), (2, ))
        self.qgb.addRow((self.btn_pass, ), (2, ))
        self.qgb.addRow((self.btn_retract, ), (2, ))
        self.qgb.addRow((self.btn_admit_defeat, ), (2, ))
        self.qgb.addRow((self.btn_load_game, ), (2, ))
        self.qgb.addRow((self.btn_save_game, ), (2, ))
        self.qgb.addRow((self.msgbox, ), (2, ))

        self.qgb.apply_layout()

        self.adjust_size()

    def adjust_size(self):
        width, height = 1000, 800
        self.resize(width, height)
        self.img_frame.setGeometry(0, 0, height, height)
        self.qgb.setGeometry(height, 0, width - height, height)

    def show_msg(self):
        self.msgbox.setText("\n".join(self.msg))

    def show_dialog(self, type: str, caption: str, text: str):
        if type == "about":
            QMessageBox.about(self, caption, text)
        elif type == "infomation":
            QMessageBox.information(self, caption, text)
        elif type == "question":
            return QMessageBox.question(self, caption, text, Yes | No, Yes) == Yes
        elif type == "warning":
            return QMessageBox.warning(self, caption, text, Ok | Cancel, Ok)==Ok
        elif type == "critical":
            QMessageBox.critical(self, caption, text, Ok | Cancel, Ok)

    def get_save_path(self, caption="保存为", filter=""):
        fname, _ = QFileDialog.getSaveFileName(self, caption, filter=filter)
        return fname

    def get_open_path(self, caption="保存为", filter=""):
        fname, _ = QFileDialog.getOpenFileName(self, caption, filter=filter)
        return fname

    # def resizeEvent(self, event):
    #     super().resizeEvent(event)
    #     self.adjust_size()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GameUI()
    window.show()
    app.exec()
