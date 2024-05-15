import numpy as np
from .QuoridorLogic import Board
from Game import Game


class QuoridorGame(Game):
    def __init__(self, n):
        self.n = n

    def getInitBoard(self):
        # 초기 보드 상태를 반환
        b = Board(self.n)
        return b

    def getBoardSize(self):
        # 보드 크기 반환
        return (self.n, self.n)

    def getActionSize(self):
        # 가능한 행동의 수 반환 (플레이어 이동 + 벽 설치)
        return self.n * self.n + (self.n - 1) * (self.n - 1) * 2

    def getNextState(self, board, player, action):
        # 주어진 행동에 따른 다음 상태 반환
        b = board.clone()
        if action < self.n * self.n:
            move = (action // self.n, action % self.n)
            b.execute_move(move, player)
        else:
            wall_type = (action - self.n * self.n) // ((self.n - 1) * (self.n - 1))
            wall_pos = (action - self.n * self.n) % ((self.n - 1) * (self.n - 1))
            wall_pos = (wall_pos // (self.n - 1), wall_pos % (self.n - 1))
            b.place_wall(wall_pos, wall_type, player)
        return (b, -player)

    def getValidMoves(self, board, player):
        # 주어진 상태에서 가능한 행동 반환
        valids = [0] * self.getActionSize()
        b = board.clone()

        # 이동 가능 체크
        moves = b.get_legal_moves(player)
        for move in moves:
            valids[move[0] * self.n + move[1]] = 1

        # 벽 설치 가능 체크
        walls = b.get_legal_walls(player)
        for wall in walls:
            wall_idx = self.n * self.n + wall[0] * (self.n - 1) + wall[1]
            if wall[2] == "h":
                wall_idx += 0
            else:
                wall_idx += (self.n - 1) * (self.n - 1)
            valids[wall_idx] = 1

        return np.array(valids)

    def getGameEnded(self, board, player):
        # 게임 종료 여부 판단
        if board.is_win(player):
            return 1
        if board.is_win(-player):
            return -1
        return 0

    def getCanonicalForm(self, board, player):
        # 표준 형태의 보드 반환
        return board

    def getSymmetries(self, board, pi):
        # 대칭 상태 반환
        return [(board, pi)]

    def stringRepresentation(self, board):
        # 보드 상태를 문자열로 반환
        return board.to_string()
