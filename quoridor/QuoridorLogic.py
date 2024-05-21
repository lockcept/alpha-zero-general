from collections import deque
import numpy as np


class Board:
    def __init__(self, n):
        self.n = n
        self.p1_pos = (0, n // 2)
        self.p2_pos = (n - 1, n // 2)
        self.p1_walls = 10
        self.p2_walls = 10
        self.h_walls = set()
        self.v_walls = set()

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
            return self.p2_pos[0] == 0

    def is_wall_between(self, pos1, pos2):
        # 인접한 두 포지션이라고 가정
        x1, y1 = pos1
        x2, y2 = pos2

        if x1 == x2:
            y = min(y1, y2)
            if (x1 - 1, y) in self.v_walls or (x1, y) in self.v_walls:
                return True
        elif y1 == y2:
            x = min(x1, x2)
            if (x, y1 - 1) in self.h_walls or (x, y1) in self.h_walls:
                return True
        return False

    def get_legal_moves(self, player):
        if player == 1:
            pos = self.p1_pos
            opponent_pos = self.p2_pos
        else:
            pos = self.p2_pos
            opponent_pos = self.p1_pos

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        legal_moves = []

        for move in directions:
            new_pos = (pos[0] + move[0], pos[1] + move[1])
            if not self.is_wall_between(pos, new_pos):
                # 도착 위치에 적이 있는 경우
                if new_pos == opponent_pos:
                    jump_pos = (new_pos[0] + move[0], new_pos[1] + move[1])
                    if not self.is_wall_between(new_pos, jump_pos):
                        legal_moves.append(jump_pos)
                    else:
                        # 수직 방향 이동 검사
                        vertical_moves = []
                        if move[0] == 0:
                            vertical_moves = [(-1, 0), (1, 0)]
                        else:
                            vertical_moves = [(0, -1), (0, 1)]

                        for v_move in vertical_moves:
                            new_v_pos = (new_pos[0] + v_move[0], new_pos[1] + v_move[1])
                            if not self.is_wall_between(new_pos, new_v_pos):
                                legal_moves.append(new_v_pos)
                else:
                    legal_moves.append((pos[0] + move[0], pos[1] + move[1]))

        return [
            (x, y)
            for x, y in legal_moves
            if x >= 0 and x < self.n and y >= 0 and y < self.n
        ]

    def is_legal_wall(self, pos, wall_type):
        if pos[0] < 0 or pos[0] >= self.n - 1 or pos[1] < 0 or pos[1] >= self.n - 1:
            return False

        if wall_type == 0:  # 수평 벽
            if (
                pos in self.h_walls
                or (pos[0], pos[1] - 1) in self.h_walls
                or (pos[0], pos[1] + 1) in self.h_walls
                or (pos in self.v_walls)
            ):
                return False
        elif wall_type == 1:  # 수직 벽
            if (
                pos in self.v_walls
                or (pos[0] - 1, pos[1]) in self.v_walls
                or (pos[0] + 1, pos[1]) in self.v_walls
                or (pos in self.h_walls)
            ):
                return False

        temp_h_walls = self.h_walls.copy()
        temp_v_walls = self.v_walls.copy()
        if wall_type == 0:
            temp_h_walls.add(pos)
        else:
            temp_v_walls.add(pos)

        if not (
            self.can_reach_goal(self.p1_pos, 1, temp_h_walls, temp_v_walls)
            and self.can_reach_goal(self.p2_pos, 2, temp_h_walls, temp_v_walls)
        ):
            return False

        return True

    def can_reach_goal(self, start, player, h_walls, v_walls):
        goal_row = self.n - 1 if player == 1 else 0
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        queue = deque([start])
        visited = set()
        visited.add(start)

        while queue:
            x, y = queue.popleft()
            if x == goal_row:
                return True

            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.n and 0 <= ny < self.n and (nx, ny) not in visited:
                    if (
                        (
                            dx == -1
                            and (x - 1, y - 1) not in h_walls
                            and (x - 1, y) not in h_walls
                        )
                        or (
                            dx == 1
                            and (x, y - 1) not in h_walls
                            and (x, y) not in h_walls
                        )
                        or (
                            dy == -1
                            and (x - 1, y - 1) not in v_walls
                            and (x, y - 1) not in v_walls
                        )
                        or (
                            dy == 1
                            and (x - 1, y) not in v_walls
                            and (x, y) not in v_walls
                        )
                    ):
                        queue.append((nx, ny))
                        visited.add((nx, ny))

        return False

    def get_legal_walls(self, player):
        legal_walls = []
        if player == 1 and self.p1_walls <= 0:
            return legal_walls
        if player == 2 and self.p2_walls <= 0:
            return legal_walls
        for i in range(self.n - 1):
            for j in range(self.n - 1):
                if self.is_legal_wall((i, j), 0):
                    legal_walls.append((i, j, "h"))
                if self.is_legal_wall((i, j), 1):
                    legal_walls.append((i, j, "v"))
        return legal_walls

    def to_array(self):
        board_array = np.zeros((self.n, self.n, 6))
        board_array[self.p1_pos][0] = 1
        board_array[self.p2_pos][1] = 1
        for wall in self.h_walls:
            board_array[wall][2] = 1
        for wall in self.v_walls:
            board_array[wall][3] = 1
        board_array[:, :, 4] = self.p1_walls
        board_array[:, :, 5] = self.p2_walls
        return board_array
