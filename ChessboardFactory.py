from Chessboard import Chessboard
from GobangBoard import GobangBoard
from GoBoard import GoBoard
from OthelloBoard import OthelloBoard


class ChessboardFactory:

    def create_chessboard(self, type: int, size: int) -> Chessboard:
        if type == 0:
            return GobangBoard(size)
        if type == 1:
            return GoBoard(size)
        if type==2:
            return OthelloBoard(8)