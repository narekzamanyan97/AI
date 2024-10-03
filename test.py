from tictactoe import *

X = 'X'
O = 'O'
EMPTY = None

board = [[EMPTY, EMPTY, EMPTY],
        [EMPTY, O, EMPTY],
        [O, X, X]]

# board = [[EMPTY, EMPTY, EMPTY],
#         [EMPTY, EMPTY, EMPTY],
#         [EMPTY, EMPTY, EMPTY]]

print(minimax(board))
