from __future__ import print_function
import sys
from quoridor.action import QuoridorAction

from quoridor.board import QuoridorBoard

sys.path.append("..")
from Game import Game
import numpy as np


class QuoridorGame(Game):
    def __init__(self, n):
        self.n = n
        self.wall_count = 10

    def getInitBoard(self):
        # return initial board (numpy board)
        b = QuoridorBoard(size=self.n, wall_count=self.wall_count)
        return b.pieces

    def getBoardSize(self):
        return (6, self.n, self.n)

    def getActionSize(self):
        return self.n * self.n + 2 * (self.n - 1) * (self.n - 1)

    def getNextState(self, board, player: int, action: int):
        b = QuoridorBoard(size=self.n, wall_count=self.wall_count)
        b.pieces = np.copy(board)
        action = QuoridorAction.all_actions()[action]
        b.action_player(player=player, action=action)
        return (b.pieces, 3 - player)

    def getValidMoves(self, board, player: int):
        # return a fixed size binary vector
        valids = [0] * self.getActionSize()
        allActions = QuoridorAction.all_actions()
        b = QuoridorBoard(size=self.n, wall_count=self.wall_count)
        b.pieces = np.copy(board)
        for index, action in enumerate(allActions):
            if b.is_valid_action(player=player, action=action):
                valids[index] = 1
        return np.array(valids)

    def getGameEnded(self, board, player: int):
        b = QuoridorBoard(self.n, wall_count=self.wall_count)
        b.pieces = np.copy(board)
        return b.is_game_ended(player=player)

    def getCanonicalForm(self, board, player: int):
        if player == 1:
            return np.copy(board)

        size = self.n

        def mirror_y_wall_positions(positions):
            new_positions = np.zeros((size, size))
            for x in range(size - 1):
                for y in range(size - 1):
                    new_positions[x][y] = positions[x][size - 2 - y]
            return new_positions

        new_board = np.copy(board)
        return np.stack(
            [
                new_board[1][:, ::-1],
                new_board[0][:, ::-1],
                mirror_y_wall_positions(positions=new_board[2]),
                mirror_y_wall_positions(positions=new_board[3]),
                new_board[5],
                new_board[4],
            ],
        )

    def getSymmetries(self, board, pi):
        # 좌우 대칭
        assert len(pi) == self.getActionSize()

        size = self.n

        def mirror_x_wall_positions(positions):
            new_positions = np.zeros((size, size))
            for x in range(size - 1):
                for y in range(size - 1):
                    new_positions[x][y] = positions[size - 2 - x][y]
            return new_positions

        new_board = np.stack(
            [
                board[0][::-1, :],
                board[1][::-1, :],
                mirror_x_wall_positions(positions=board[2]),
                mirror_x_wall_positions(positions=board[3]),
                np.copy(board[4]),
                np.copy(board[5]),
            ]
        )

        move_actions_num = size * size
        wall_actions_num = (size - 1) * (size - 1)

        moves = pi[0:move_actions_num]
        vertical_walls = pi[move_actions_num : move_actions_num + wall_actions_num]
        horizontal_walls = pi[
            move_actions_num
            + wall_actions_num : move_actions_num
            + wall_actions_num * 2
        ]

        mirror_moves = np.reshape(moves, (size, size))[::-1, :]
        vertical_moves = np.reshape(vertical_walls, (size - 1, size - 1))[::-1, :]
        horizontal_moves = np.reshape(horizontal_walls, (size - 1, size - 1))[::-1, :]

        return [
            (
                new_board,
                np.concatenate(
                    (mirror_moves, vertical_moves, horizontal_moves), axis=None
                ),
            )
        ]

    def stringRepresentation(self, board):
        b = QuoridorBoard(self.n, wall_count=self.wall_count)
        b.pieces = np.copy(board)
        return b.state_str()

    def getScore(self, board, player):
        b = QuoridorBoard(self.n)
        b.pieces = np.copy(board)
        target_y = {1: self.size - 1, 2: 0}
        distances = b.bfs_distance_player(player=player)
        distances = np.where(distances == -1, np.inf, distances)
        distance = np.min(distances[:, target_y[player]])

        enemy_player = 3 - player
        enemy_distances = b.bfs_distance_player(player=enemy_player)
        enemy_distances = np.where(enemy_distances == -1, np.inf, enemy_distances)
        enemy_distance = np.min(enemy_distances[:, target_y[enemy_player]])

        return enemy_distance - distance * 5

    @staticmethod
    def display(board: QuoridorBoard):
        print(board.state_str())
