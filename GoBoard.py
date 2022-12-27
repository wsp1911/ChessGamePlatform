from Chessboard import Chessboard


class GoBoard(Chessboard):

    def __init__(self, size: int):
        super().__init__(size, 1)
        self._forbid_repeat = False
        self._offset = [[0, 1], [1, 0], [0, -1], [-1, 0]]
        self._qi = 0
        self._no_qi = True

    def check(self, x: int, y: int):
        return False

    def remove_from_board(self):
        s = self.get_size()
        visited = self.get_valid_board() == 0
        to_remove = []
        for i in range(s):
            for j in range(s):
                if visited[i, j]:
                    continue
                self._no_qi = True
                nodes = []
                self.bfs(i, j, visited, nodes)
                if self._no_qi:
                    to_remove.extend(nodes)

        for x, y in to_remove:
            self.set_xy(x, y, 0)

    def bfs(self, x, y, visited, nodes):
        c = self.get_xy(x, y)
        if c == 2 or visited[x, y]:
            return
        visited[x, y] = True
        nodes.append((x, y))
        for dx, dy in self._offset:
            xi, yi = x + dx, y + dy
            ci = self.get_xy(xi, yi)
            if ci == 2:
                continue
            if ci == 0:
                self._no_qi = False
                continue
            if ci == c and not visited[xi, yi]:
                self.bfs(xi, yi, visited, nodes)

    def get_qi(self, x, y):
        """查询(x,y)处棋子的气，需保证此处有棋子
        """
        self._qi = 0
        visited = self.get_valid_board() == 0
        self.bfs2(x, y, visited)
        return self._qi

    def bfs2(self, x, y, visited):
        c = self.get_xy(x, y)
        if c == 2 or visited[x, y]:
            return
        visited[x, y] = True
        for dx, dy in self._offset:
            xi, yi = x + dx, y + dy
            ci = self.get_xy(xi, yi)
            if ci == 2:
                continue
            if ci == 0:
                self._qi += 1
                continue
            if ci == c and not visited[xi, yi]:
                self.bfs2(xi, yi, visited)

    def validate(self, x: int, y: int, color: int):
        """0为非法，1为有气合法，2为无气但可以吃子"""
        if self.get_xy(x, y) != 0:
            return 0
        self.set_xy(x, y, color)
        qi = self.get_qi(x, y)
        if qi:
            self.set_xy(x, y, 0)
            return 1

        # 无气时检查是否能吃子
        can_eat = 0
        for dx, dy in self._offset:
            xi, yi = x + dx, y + dy
            if self.get_xy(xi, yi) == 2:  # 边界
                continue
            if self.get_qi(xi, yi) == 0:
                can_eat = 2
                break

        self.set_xy(x, y, 0)
        return can_eat

    def make_move(self, x: int, y: int, color: int):
        valid = self.validate(x, y, color)
        if valid:
            self.set_xy(x, y, color)
            self.remove_from_board()
            if valid == 2:
                self.set_xy(x, y, color)
            return True
        return False

if __name__ == "__main__":
    board = GoBoard(4)
    for i in range(2):
        for j in range(2):
            board.set_xy(i, j, 1)
    for i in range(2):
        board.set_xy(i, 2, -1)
    for i in range(2):
        board.set_xy(2, i, -1)
    print(board._board)
    board.remove_from_board()
    print(board._board)
