from collections import deque
from action import ActionType, QuoridorAction
import numpy as np


class QuoridorBoard:
    def __init__(self, size: int, wall_count: int):
        self.size = size

        player1_position_channel = np.zeros((size, size))
        player2_position_channel = np.zeros((size, size))
        vertical_wall_channel = np.zeros((size, size))
        horizontal_wall_channel = np.zeros((size, size))
        wall_count_channel_player1 = np.full((size, size), wall_count)
        wall_count_channel_player2 = np.full((size, size), wall_count)

        player_positions = {
            1: (self.size // 2, 0),
            2: (self.size // 2, self.size - 1),
        }

        player1_position_channel[player_positions[1]] = 1
        player2_position_channel[player_positions[2]] = 1

        self.pieces = np.stack(
            [
                player1_position_channel,
                player2_position_channel,
                vertical_wall_channel,
                horizontal_wall_channel,
                wall_count_channel_player1,
                wall_count_channel_player2,
            ],
        )

    def bfs_distance_player(self, player):
        player_positions = self.pieces[player - 1]
        player_place = np.argwhere(player_positions == 1)[0]
        vertical_walls = self.pieces[2]
        horizontal_walls = self.pieces[3]
        return self.bfs_distance_with_walls(
            position=tuple(player_place),
            vertical_walls=vertical_walls,
            horizontal_walls=horizontal_walls,
        )

    def bfs_distance_with_walls(self, position, vertical_walls, horizontal_walls):
        distances = np.full((self.size, self.size), -1)
        x, y = position

        queue = deque([(x, y)])
        distances[x][y] = 0

        moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        while queue:
            x, y = queue.popleft()
            distance = distances[x][y]

            for dx, dy in moves:
                new_x, new_y = x + dx, y + dy

                if (
                    0 <= new_x < self.size
                    and 0 <= new_y < self.size
                    and distances[new_x][new_y] == -1
                ):
                    if (
                        dx == 0
                        and horizontal_walls[x][min(y, new_y)] == 0
                        and (x - 1 < 0 or horizontal_walls[x - 1][min(y, new_y)] == 0)
                    ) or (
                        dy == 0
                        and vertical_walls[min(x, new_x)][y] == 0
                        and (y - 1 < 0 or vertical_walls[min(x, new_x)][y - 1] == 0)
                    ):
                        distances[new_x][new_y] = distance + 1
                        queue.append((new_x, new_y))

        return distances

    def is_opened_walls(self, vertical_walls, horizontal_walls, player_positions):
        target_y = {1: self.size - 1, 2: 0}

        for index, (x, y) in enumerate(player_positions):
            player = index + 1
            distances = self.bfs_distance_with_walls(
                position=(x, y),
                vertical_walls=vertical_walls,
                horizontal_walls=horizontal_walls,
            )

            if not np.any(distances[:, target_y[player]] >= 0):
                return False

        return True

    def is_valid_action(self, player, action: QuoridorAction):
        if player not in (1, 2):
            raise ValueError("플레이어 번호는 1 또는 2여야 합니다.")

        player_positions = self.pieces[player - 1]
        enemy_positions = self.pieces[2 - player]

        vertical_walls = self.pieces[2]
        horizontal_walls = self.pieces[3]

        player_place = np.argwhere(player_positions == 1)[0]
        enemy_place = np.argwhere(enemy_positions == 1)[0]

        def is_wall_empty(head, tail):
            (head_x, head_y) = head
            (tail_x, tail_y) = tail
            if abs(head_x - tail_x) + abs(head_y - tail_y) != 1:
                return False
            is_horizontal = abs(head_x - tail_x) == 1

            x = min(head_x, tail_x)
            y = min(head_y, tail_y)

            if is_horizontal:
                if vertical_walls[x][y] == 1:
                    return False
                if y - 1 >= 0 and vertical_walls[x][y - 1] == 1:
                    return False
            else:
                if horizontal_walls[x][y] == 1:
                    return False
                if x - 1 >= 0 and horizontal_walls[x - 1][y] == 1:
                    return False
            return True

        if action.action_type == ActionType.MOVE:
            x, y = action.x, action.y
            if not (0 <= x < self.size) or not (0 <= y < self.size):
                return False

            if player_positions[x][y] == 1:
                return False
            if enemy_positions[x][y] == 1:
                return False

            old_x, old_y = player_place
            enemy_x, enemy_y = enemy_place

            if (abs(old_x - x) + abs(old_y - y)) != 1:
                # 이동 거리가 1이 아닌 경우 뛰어넘기 검사
                if (abs(old_x - x) + abs(old_y - y)) == 2:
                    if abs(old_x - x) == 2 or abs(old_y - y) == 2:
                        center_x = (old_x + x) // 2
                        center_y = (old_y + y) // 2
                        if (
                            (center_x, center_y) == (enemy_x, enemy_y)
                            and is_wall_empty(
                                head=(old_x, old_y), tail=(center_x, center_y)
                            )
                            and is_wall_empty(head=(center_x, center_y), tail=(x, y))
                        ):
                            return True
                    else:
                        if (
                            (old_x, y) == (enemy_x, enemy_y)
                            and is_wall_empty(head=(old_x, old_y), tail=(old_x, y))
                            and is_wall_empty(head=(old_x, y), tail=(x, y))
                            and not is_wall_empty(
                                head=(old_x, y), tail=(old_x, 2 * y - old_y)
                            )
                        ):
                            return True
                        if (
                            (x, old_y) == (enemy_x, enemy_y)
                            and is_wall_empty(head=(old_x, old_y), tail=(x, old_y))
                            and is_wall_empty(head=(x, old_y), tail=(x, y))
                            and not is_wall_empty(
                                head=(x, old_y), tail=(2 * x - old_x, old_y)
                            )
                        ):
                            return True
                        return False

                return False

            # 정상적인 이동 벽 검사
            if not is_wall_empty(head=(old_x, old_y), tail=(x, y)):
                return False

        elif action.action_type == ActionType.WALL_VERTICAL:
            player_wall_counts = self.pieces[3 + player]
            if player_wall_counts[0][0] == 0:
                return False

            x, y = action.x, action.y
            if not (0 <= x < self.size - 1) or not (0 <= y < self.size - 1):
                return False

            if horizontal_walls[x][y] == 1:
                return False
            if (
                (y - 1 >= 0 and vertical_walls[x][y - 1] == 1)
                or vertical_walls[x][y] == 1
                or vertical_walls[x][y + 1] == 1
            ):
                return False

            new_vertical_walls = np.copy(vertical_walls)
            new_vertical_walls[x][y] = 1

            if not self.is_opened_walls(
                player_positions=[tuple(player_place), tuple(enemy_place)],
                vertical_walls=new_vertical_walls,
                horizontal_walls=horizontal_walls,
            ):
                return False

        elif action.action_type == ActionType.WALL_HORIZONTAL:
            player_wall_counts = self.pieces[3 + player]
            if player_wall_counts[0][0] == 0:
                return False

            x, y = action.x, action.y
            if not (0 <= x < self.size - 1) or not (0 <= y < self.size - 1):
                return False

            if vertical_walls[x, y] == 1:
                return False
            if (
                (x - 1 >= 0 and horizontal_walls[x - 1, y] == 1)
                or horizontal_walls[x, y] == 1
                or horizontal_walls[x + 1, y] == 1
            ):
                return False

            new_horizontal_walls = np.copy(horizontal_walls)
            new_horizontal_walls[x][y] = 1

            if not self.is_opened_walls(
                player_positions=[tuple(player_place), tuple(enemy_place)],
                vertical_walls=vertical_walls,
                horizontal_walls=new_horizontal_walls,
            ):
                return False

        return True

    def action_player(self, player: int, action: QuoridorAction):
        if self.is_valid_action(player, action):
            if action.action_type == ActionType.MOVE:
                new_position_channel = np.zeros((self.size, self.size))
                new_position_channel[action.x][action.y] = 1
                self.pieces[player - 1] = new_position_channel
            elif action.action_type == ActionType.WALL_VERTICAL:
                self.pieces[2][action.x][action.y] = 1
                player_wall_count = self.pieces[3 + player][0][0]
                new_wall_count_channel = np.full(
                    (self.size, self.size), player_wall_count - 1
                )
                self.pieces[3 + player] = new_wall_count_channel
            elif action.action_type == ActionType.WALL_HORIZONTAL:
                self.pieces[3][action.x][action.y] = 1
                player_wall_count = self.pieces[3 + player][0][0]
                new_wall_count_channel = np.full(
                    (self.size, self.size), player_wall_count - 1
                )
                self.pieces[3 + player] = new_wall_count_channel

    def is_game_ended(self, player):
        # return 0 if not ended, 1 if player 1 won, -1 if player 1 lost

        end_y = {1: self.size - 1, 2: 0}

        player_positions = self.pieces[player - 1]
        enemy_positions = self.pieces[2 - player]

        player_place = np.argwhere(player_positions == 1)[0]
        enemy_place = np.argwhere(enemy_positions == 1)[0]

        if player_place[1] == end_y[player]:
            return 1
        if enemy_place[1] == end_y[3 - player]:
            return -1
        return 0

    def state(self, player=1):
        enemy_player = 3 - player
        player_positions = self.pieces[player - 1]
        enemy_positions = self.pieces[2 - player]

        vertical_walls = self.pieces[2]
        horizontal_walls = self.pieces[3]

        player_wall_count = self.pieces[3 + player][0][0]
        enemy_wall_count = self.pieces[3 + enemy_player][0][0]

        player_place = np.argwhere(player_positions == 1)[0]
        enemy_place = np.argwhere(enemy_positions == 1)[0]
        state = {
            "my_position": player_place,
            "enemy_position": enemy_place,
            "my_wall_count": player_wall_count,
            "enemy_wall_count": enemy_wall_count,
            "vertical_walls": np.argwhere(vertical_walls == 1),
            "horizontal_walls": np.argwhere(horizontal_walls == 1),
        }
        return state

    def state_str(self, player=1):
        state = self.state(player=player)
        return str(state)
