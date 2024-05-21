import numpy as np

from quoridor.QuoridorLogic import Board
from quoridor.QuoridorGame import QuoridorGame


# 테스트
n = 9
board = np.zeros((n, n, 7))
game = QuoridorGame(n)

# 예시 상태 설정
board[0, 4, 0] = 1  # 플레이어 1의 위치
board[1, 4, 1] = 1  # 플레이어 2의 위치
board[0, 0, 2] = 1
board[0, 2, 2] = 1
board[0, 4, 2] = 1
board[1, 4, 2] = 1
board[1, 3, 3] = 1
board[:, :, 4] = 6  # 플레이어 1의 벽 개수
board[:, :, 5] = 10  # 플레이어 2의 벽 개수
board[:, :, 6] = 300


def printMoves(moves):
    print(np.reshape(moves[: n * n], (n, n)))
    print(np.reshape(moves[n * n : n * n + (n - 1) * (n - 1)], (n - 1, n - 1)))
    print(np.reshape(moves[n * n + (n - 1) * (n - 1) :], (n - 1, n - 1)))


game.display(board)
game.display(game.getCanonicalForm(board, -1))
game.display(game.getSymmetries(board, range(1, 81 + 64 + 64 + 1))[1][0])
print(game.getSymmetries(board, range(1, 81 + 64 + 64 + 1))[1][1])
# printMoves(game.getValidMoves(board, 1))
