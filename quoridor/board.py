from action import ActionType, QuoridorAction
from config import BOARD_SIZE, WALL_COUNT


class QuoridorBoard:
    def __init__(self):
        self.size = BOARD_SIZE
        self.player_positions = {
            1: (self.size // 2, 0),
            2: (self.size // 2, self.size - 1),
        }
        self.player_wall_counts = {1: WALL_COUNT, 2: WALL_COUNT}
        self.vertical_walls = set()
        self.horizontal_walls = set()

    def is_opened_walls(self, vertical_walls, horizontal_walls, player_positions):
        target_y = {1: self.size - 1, 2: 0}
        visited = set()

        def dfs(player, x, y):
            if y == target_y[player]:
                return True

            visited.add((x, y))

            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                new_x, new_y = x + dx, y + dy
                if (
                    (new_x, new_y) not in visited
                    and 0 <= new_x < self.size
                    and 0 <= new_y < self.size
                ):
                    if (
                        dx == 0
                        and not (x, min(y, new_y)) in horizontal_walls
                        and not (x - 1, min(y, new_y)) in horizontal_walls
                    ) or (
                        dy == 0
                        and not (min(x, new_x), y) in vertical_walls
                        and not (min(x, new_x), y - 1) in vertical_walls
                    ):
                        if dfs(player, new_x, new_y):
                            return True

            return False

        for player, (x, y) in player_positions.items():
            visited.clear()
            if not dfs(player, x, y):
                return False

        return True

    def is_valid_action(self, player, action: QuoridorAction):
        if player not in (1, 2):
            raise ValueError("플레이어 번호는 1 또는 2여야 합니다.")

        def is_wall_empty(head, tail):
            (head_x, head_y) = head
            (tail_x, tail_y) = tail
            if abs(head_x - tail_x) + abs(head_y - tail_y) != 1:
                return False
            is_horizontal = abs(head_x - tail_x) == 1

            x = min(head_x, tail_x)
            y = min(head_y, tail_y)

            if is_horizontal:
                if (x, y) in self.vertical_walls:
                    return False
                if (x, y - 1) in self.vertical_walls:
                    return False
            else:
                if (x, y) in self.horizontal_walls:
                    return False
                if (x - 1, y) in self.horizontal_walls:
                    return False
            return True

        if action.action_type == ActionType.MOVE:
            x, y = action.x, action.y
            if not (0 <= x < self.size) or not (0 <= y < self.size):
                return False

            if (x, y) == self.player_positions[player]:
                return False
            if (x, y) == self.player_positions[3 - player]:
                return False

            old_x, old_y = self.player_positions[player]
            enemy_place = self.player_positions[3 - player]

            if (abs(old_x - x) + abs(old_y - y)) != 1:
                # 이동 거리가 1이 아닌 경우 뛰어넘기 검사
                if (abs(old_x - x) + abs(old_y - y)) == 2:
                    if abs(old_x - x) == 2 or abs(old_y - y) == 2:
                        center_x = (old_x + x) // 2
                        center_y = (old_y + y) // 2
                        if (
                            (center_x, center_y) == enemy_place
                            and is_wall_empty(
                                head=(old_x, old_y), tail=(center_x, center_y)
                            )
                            and is_wall_empty(head=(center_x, center_y), tail=(x, y))
                        ):
                            return True
                    else:
                        if (
                            (old_x, y) == enemy_place
                            and is_wall_empty(head=(old_x, old_y), tail=(old_x, y))
                            and is_wall_empty(head=(old_x, y), tail=(x, y))
                            and not is_wall_empty(
                                head=(old_x, y), tail=(old_x, 2 * y - old_y)
                            )
                        ):
                            return True
                        if (
                            (x, old_y) == enemy_place
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
            if self.player_wall_counts[player] == 0:
                return False
            x, y = action.x, action.y
            if not (0 <= x < self.size - 1) or not (0 <= y < self.size - 1):
                return False

            if (x, y) in self.horizontal_walls:
                return False
            if (
                (x, y - 1) in self.vertical_walls
                or (x, y) in self.vertical_walls
                or (x, y + 1) in self.vertical_walls
            ):
                return False

            new_vertical_walls = set(self.vertical_walls)
            new_vertical_walls.add((x, y))

            if not self.is_opened_walls(
                player_positions=self.player_positions,
                vertical_walls=new_vertical_walls,
                horizontal_walls=self.horizontal_walls,
            ):
                return False

        elif action.action_type == ActionType.WALL_HORIZONTAL:
            if self.player_wall_counts[player] == 0:
                return False
            x, y = action.x, action.y
            if not (0 <= x < self.size - 1) or not (0 <= y < self.size - 1):
                return False

            if (x, y) in self.vertical_walls:
                return False
            if (
                (x - 1, y) in self.horizontal_walls
                or (x, y) in self.horizontal_walls
                or (x + 1, y) in self.horizontal_walls
            ):
                return False

            new_horizontal_walls = set(self.horizontal_walls)
            new_horizontal_walls.add((x, y))

            if not self.is_opened_walls(
                player_positions=self.player_positions,
                vertical_walls=self.vertical_walls,
                horizontal_walls=new_horizontal_walls,
            ):
                return False

        return True

    def action_player(self, player: int, action: QuoridorAction):
        if self.is_valid_action(player, action):
            if action.action_type == ActionType.MOVE:
                self.player_positions[player] = (action.x, action.y)
            elif action.action_type == ActionType.WALL_VERTICAL:
                self.vertical_walls.add((action.x, action.y))
                self.player_wall_counts[player] -= 1
            elif action.action_type == ActionType.WALL_HORIZONTAL:
                self.horizontal_walls.add((action.x, action.y))
                self.player_wall_counts[player] -= 1

    def state(self, player=1):
        enemy_player = 3 - player
        state = {
            "my_position": self.player_positions[player],
            "enemy_position": self.player_positions[enemy_player],
            "my_wall_count": self.player_wall_counts[player],
            "enemy_wall_count": self.player_wall_counts[enemy_player],
            "vertical_walls": list(self.vertical_walls),
            "horizontal_walls": list(self.horizontal_walls),
        }
        return state
