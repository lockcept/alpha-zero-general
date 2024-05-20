import numpy as np

from quoridor.QuoridorGame import QuoridorGame


n = 5  # 보드 크기

g = QuoridorGame(n)
board = np.zeros((n, n, 6))

# 예시 상태 설정
board[0, n // 2, 0] = 1  # 플레이어 1의 위치
board[n - 1, n // 2, 1] = 1  # 플레이어 2의 위치
board[1, 1, 2] = 1  # 수평 벽
board[2, 3, 3] = 1  # 수직 벽
board[:, :, 4] = 10  # 플레이어 1의 벽 개수
board[:, :, 5] = 8  # 플레이어 2의 벽 개수


def printBoard(b):
    print("플레이어 1의 위치:\n", b[:, :, 0])
    print("플레이어 2의 위치:\n", b[:, :, 1])
    print("수평 벽:\n", b[:, :, 2])
    print("수직 벽:\n", b[:, :, 3])
    print("플레이어 1의 벽 개수:\n", b[:, :, 4])
    print("플레이어 2의 벽 개수:\n", b[:, :, 5])


new_board = g.getCanonicalForm(board, -1)

print("원래 보드 상태:")
printBoard(board)
print("새로운 보드 상태:")
printBoard(new_board)
