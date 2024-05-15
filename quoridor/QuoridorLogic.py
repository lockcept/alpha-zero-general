class Board:
    def __init__(self, n):
        self.n = n
        self.board = [[0] * n for _ in range(n)]
        self.p1_pos = (0, n // 2)
        self.p2_pos = (n - 1, n // 2)
        self.p1_walls = 10
        self.p2_walls = 10
        self.h_walls = set()
        self.v_walls = set()

    def clone(self):
        b = Board(self.n)
        b.board = [row[:] for row in self.board]
        b.p1_pos = self.p1_pos
        b.p2_pos = self.p2_pos
        b.p1_walls = self.p1_walls
        b.p2_walls = self.p2_walls
        b.h_walls = self.h_walls.copy()
        b.v_walls = self.v_walls.copy()
        return b

    def execute_move(self, move, player):
        if player == 1:
            self.p1_pos = move
        else:
            self.p2_pos = move

    def place_wall(self, pos, wall_type, player):
        if wall_type == 0:
            self.h_walls.add(pos)
        else:
            self.v_walls.add(pos)
        if player == 1:
            self.p1_walls -= 1
        else:
            self.p2_walls -= 1

    def is_win(self, player):
        if player == 1:
            return self.p1_pos[0] == self.n - 1
        else:
            return self.p2_pos[0]
