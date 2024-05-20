import numpy as np

from quoridor.QuoridorLogic import Board


# 테스트
n = 9
board = Board(n)

# 벽 설치 시도
print(board.is_legal_wall((3, 3), 0))  # True: 빈 공간에 수평 벽 설치
print(board.is_legal_wall((3, 3), 1))  # True: 빈 공간에 수직 벽 설치

# 벽 추가
board.h_walls.add((3, 3))
print(board.is_legal_wall((3, 3), 0))  # False: 이미 같은 위치에 수평 벽이 있음
print(board.is_legal_wall((3, 2), 0))  # False: 인접 위치에 수평 벽이 있음
print(board.is_legal_wall((3, 4), 0))  # False: 인접 위치에 수평 벽이 있음
print(
    board.is_legal_wall((3, 3), 1)
)  # False: 같은 위치에 수평 벽이 있어서 교차할 수 없음

# 수직 벽 추가
board.v_walls.add((5, 5))
print(board.is_legal_wall((5, 5), 1))  # False: 이미 같은 위치에 수직 벽이 있음
print(board.is_legal_wall((4, 5), 1))  # False: 인접 위치에 수직 벽이 있음
print(board.is_legal_wall((6, 5), 1))  # False: 인접 위치에 수직 벽이 있음
print(
    board.is_legal_wall((5, 5), 0)
)  # False: 같은 위치에 수직 벽이 있어서 교차할 수 없음

board.h_walls.clear()
board.v_walls.clear()

# 경로 차단 테스트
# 플레이어 1의 경로를 막는 벽 설치 시도
board.h_walls.add((4, 0))
board.h_walls.add((4, 2))
board.h_walls.add((4, 4))
board.h_walls.add((4, 6))
print(board.is_legal_wall((5, 7), 0))  # True
board.v_walls.add((4, 7))
print(board.is_legal_wall((5, 7), 0))  # False
