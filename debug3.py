import numpy as np

from quoridor.QuoridorLogic import Board
from quoridor.QuoridorGame import QuoridorGame


# 테스트
n = 5
board = np.zeros((n, n, 6))
game = QuoridorGame(n)

# 예시 상태 설정
board[0, n // 2, 0] = 1  # 플레이어 1의 위치
board[1, n // 2, 1] = 1  # 플레이어 2의 위치
board[1, n // 2, 2] = 1
board[:, :, 4] = 10  # 플레이어 1의 벽 개수
board[:, :, 5] = 10  # 플레이어 2의 벽 개수


def print_moves(moves):
    print(np.reshape(moves[: n * n], (n, n)))
    print(np.reshape(moves[n * n : n * n + (n - 1) * (n - 1)], (n - 1, n - 1)))
    print(np.reshape(moves[n * n + (n - 1) * (n - 1) :], (n - 1, n - 1)))


print_moves(game.getValidMoves(board, 1))
