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

    def is_legal_move(self, pos, player):
        if pos[0] < 0 or pos[0] >= self.n or pos[1] < 0 or pos[1] >= self.n:
            return False
        if player == 1:
            current_pos = self.p1_pos
        else:
            current_pos = self.p2_pos

        if pos == (current_pos[0] - 1, current_pos[1]) and (
            (pos[0], pos[1]) in self.h_walls or (pos[0], pos[1] - 1) in self.h_walls
        ):
            return False
        if pos == (current_pos[0] + 1, current_pos[1]) and (
            (current_pos[0], current_pos[1]) in self.h_walls
            or (current_pos[0], current_pos[1] - 1) in self.h_walls
        ):
            return False
        if pos == (current_pos[0], current_pos[1] - 1) and (
            (pos[0], pos[1]) in self.v_walls or (pos[0] - 1, pos[1]) in self.v_walls
        ):
            return False
        if pos == (current_pos[0], current_pos[1] + 1) and (
            (current_pos[0], current_pos[1]) in self.v_walls
            or (current_pos[0] - 1, current_pos[1]) in self.v_walls
        ):
            return False

        return True

    def get_legal_moves(self, player):
        if player == 1:
            pos = self.p1_pos
        else:
            pos = self.p2_pos

        possible_moves = [
            (pos[0] - 1, pos[1]),
            (pos[0] + 1, pos[1]),
            (pos[0], pos[1] - 1),
            (pos[0], pos[1] + 1),
        ]
        legal_moves = [
            move for move in possible_moves if self.is_legal_move(move, player)
        ]
        return legal_moves

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
                            and (x, y - 1) not in v_walls
                            and (x + 1, y - 1) not in v_walls
                        )
                    ):
                        queue.append((nx, ny))
                        visited.add((nx, ny))

        return False

    def get_legal_walls(self, player):
        legal_walls = []
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
