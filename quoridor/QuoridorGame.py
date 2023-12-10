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

    def getInitBoard(self):
        # return initial board (numpy board)
        b = QuoridorBoard(size=self.n)
        return b.pieces

    def getBoardSize(self):
        return (self.n, self.n, 6)

    def getActionSize(self):
        return self.n * self.n + 2 * (self.n - 1) * (self.n - 1)

    def getNextState(self, board, player: int, action: int):
        b = QuoridorBoard(size=self.n)
        b.pieces = np.copy(board)
        action = QuoridorAction.all_actions[action]
        b.action_player(action, player)
        return (b.pieces, 3 - player)

    def getValidMoves(self, board, player: int):
        # return a fixed size binary vector
        valids = [0] * self.getActionSize()
        allActions = QuoridorAction.all_actions
        b = QuoridorBoard(size=self.n)
        b.pieces = np.copy(board)
        validActions = b.get_legal_moves(player)
        if len(validActions) == 0:
            valids[-1] = 1
            return np.array(valids)
        for action, index in allActions:
            if b.is_valid_action(player=player, action=action):
                valids[index] = 1
        return np.array(valids)

    def getGameEnded(self, board, player: int):
        # return 0 if not ended, 1 if player 1 won, -1 if player 1 lost
        # player = 1
        b = QuoridorBoard(self.n)
        b.pieces = np.copy(board)
        return b.is_game_ended(player=player)

    def getCanonicalForm(self, board, player: int):
        b = QuoridorBoard(self.n)
        b.pieces = np.copy(board)
        return player * board

    def getSymmetries(self, board, pi):
        # mirror, rotational
        assert len(pi) == self.n**2 + 1  # 1 for pass
        pi_board = np.reshape(pi[:-1], (self.n, self.n))
        l = []

        for i in range(1, 5):
            for j in [True, False]:
                newB = np.rot90(board, i)
                newPi = np.rot90(pi_board, i)
                if j:
                    newB = np.fliplr(newB)
                    newPi = np.fliplr(newPi)
                l += [(newB, list(newPi.ravel()) + [pi[-1]])]
        return l

    def stringRepresentation(self, board: QuoridorBoard):
        return board.state_str()

    def getScore(self, board, player):
        b = QuoridorBoard(self.n)
        b.pieces = np.copy(board)
        return b.countDiff(player)

    @staticmethod
    def display(board: QuoridorBoard):
        print(board.state_str())
