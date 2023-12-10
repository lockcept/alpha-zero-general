from enum import Enum

from quoridor.config import BOARD_SIZE


class ActionType(Enum):
    MOVE = "move"
    WALL_VERTICAL = "wall_vertical"
    WALL_HORIZONTAL = "wall_horizontal"


class QuoridorAction:
    def __init__(self, action_type: ActionType, x: int, y: int):
        self.action_type = action_type
        self.x = x
        self.y = y

    def __str__(self):
        return f"{self.action_type}, X: {self.x}, Y: {self.y}"

    _all_actions = None

    @staticmethod
    def all_actions():
        if QuoridorAction._all_actions is None:
            QuoridorAction._all_actions = QuoridorAction._calculate_all_actions()
        return QuoridorAction._all_actions

    @staticmethod
    def _calculate_all_actions():
        all_actions = []
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                move_action = QuoridorAction(x=x, y=y, action_type=ActionType.MOVE)
                all_actions.append(move_action)
        for x in range(BOARD_SIZE - 1):
            for y in range(BOARD_SIZE - 1):
                vertical_wall = QuoridorAction(
                    x=x, y=y, action_type=ActionType.WALL_VERTICAL
                )
                all_actions.append(vertical_wall)
        for x in range(BOARD_SIZE - 1):
            for y in range(BOARD_SIZE - 1):
                horizontal_wall = QuoridorAction(
                    x=x, y=y, action_type=ActionType.WALL_HORIZONTAL
                )
                all_actions.append(horizontal_wall)
        return all_actions
