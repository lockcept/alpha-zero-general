import numpy as np
from .QuoridorLogic import Board
from Game import Game


class QuoridorGame(Game):
    def __init__(self, n):
        self.n = n

    def getInitBoard(self):
        b = Board(self.n)
        return b.to_array()

    def getBoardSize(self):
        return (
            self.n,
            self.n,
            6,
        )  # p1_pos, p2_pos, h_walls, v_walls, p1_walls, p2_walls

    def getActionSize(self):
        return self.n * self.n + (self.n - 1) * (self.n - 1) * 2

    def getNextState(self, board, player: int, action: int):
        # valid action만 들어온다고 가정
        b = Board(self.n)
        b.p1_pos = tuple(np.argwhere(board[:, :, 0] == 1)[0])
        b.p2_pos = tuple(np.argwhere(board[:, :, 1] == 1)[0])
        b.p1_walls = int(board[0, 0, 4])
        b.p2_walls = int(board[0, 0, 5])

        for i in range(self.n):
            for j in range(self.n):
                if board[i, j, 2] == 1:
                    b.h_walls.add((i, j))
                if board[i, j, 3] == 1:
                    b.v_walls.add((i, j))

        if action < self.n * self.n:
            move = (action // self.n, action % self.n)
            b.execute_move(move, player)
        else:
            wall_type = (action - self.n * self.n) // ((self.n - 1) * (self.n - 1))
            wall_pos = (action - self.n * self.n) % ((self.n - 1) * (self.n - 1))
            wall_pos = (wall_pos // (self.n - 1), wall_pos % (self.n - 1))
            b.place_wall(wall_pos, wall_type, player)
        return (b.to_array(), -player)

    def getValidMoves(self, board, player):
        # 주어진 상태에서 가능한 행동 반환
        valids = [0] * self.getActionSize()
        b = Board(self.n)
        b.p1_pos = tuple(np.argwhere(board[:, :, 0] == 1)[0])
        b.p2_pos = tuple(np.argwhere(board[:, :, 1] == 1)[0])
        b.p1_walls = int(board[0, 0, 4])
        b.p2_walls = int(board[0, 0, 5])

        for i in range(self.n):
            for j in range(self.n):
                if board[i, j, 2] == 1:
                    b.h_walls.add((i, j))
                if board[i, j, 3] == 1:
                    b.v_walls.add((i, j))

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
        b = Board(self.n)
        b.p1_pos = tuple(np.argwhere(board[:, :, 0] == 1)[0])
        b.p2_pos = tuple(np.argwhere(board[:, :, 1] == 1)[0])
        b.p1_walls = int(board[0, 0, 4])
        b.p2_walls = int(board[0, 0, 5])

        for i in range(self.n):
            for j in range(self.n):
                if board[i, j, 2] == 1:
                    b.h_walls.add((i, j))
                if board[i, j, 3] == 1:
                    b.v_walls.add((i, j))

        if b.is_win(player):
            return 1
        if b.is_win(-player):
            return -1
        return 0

    def getCanonicalForm(self, board, player):
        # 표준 형태의 보드 반환
        if player == 1:
            return board
        else:
            new_board = np.zeros_like(board)
            new_board[:, :, 0:2] = np.flip(board[:, :, 0:2], axis=[0, 2])
            new_board[:-1, :-1, 2:4] = np.flip(board[:-1, :-1, 2:4], axis=0)
            new_board[:, :, 4:6] = np.flip(board[:, :, 4:6], axis=2)
            return new_board

    def getSymmetries(self, board, pi):
        # 대칭 상태 반환
        assert len(pi) == self.getActionSize()  # 올바른 pi 길이 확인

        pi_board = np.reshape(pi[: self.n * self.n], (self.n, self.n))
        pi_walls = pi[self.n * self.n :]

        l = []

        for i in range(1, 5):
            newB = np.rot90(board, i)
            newPi = np.rot90(pi_board, i)
            newWalls = pi_walls.copy()
            if i % 2 == 1:
                newWalls[: len(newWalls) // 2], newWalls[len(newWalls) // 2 :] = (
                    newWalls[len(newWalls) // 2 :],
                    newWalls[: len(newWalls) // 2],
                )
            newPi = list(newPi.ravel()) + list(newWalls)
            l += [(newB, newPi)]

        return l

    def stringRepresentation(self, board):
        # 보드 상태를 문자열로 반환
        return board.tostring()

    @staticmethod
    def display(board: Board):
        n = board.shape[0]
        print("  ", end="")
        for y in range(n):
            print(y, end=" ")
        print("")

        for x in range(n):
            print(x, end=" ")
            for y in range(n):
                piece = board[x, y, :]
                if piece[0] == 1:
                    print("1", end=" ")
                elif piece[1] == 1:
                    print("2", end=" ")
                elif piece[2] == 1:
                    print("-", end=" ")
                elif piece[3] == 1:
                    print("|", end=" ")
                else:
                    print(".", end=" ")
            print("")
