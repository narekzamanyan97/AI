"""
Tic Tac Toe Player
"""
# 
# https://cs50.harvard.edu/ai/2024/projects/0/tictactoe/

import math
# for deep copy
import copy

import random

X = "X"
O = "O"
EMPTY = None

global_counter = 0

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_count = 0
    y_count = 0

    for row in range(0, 3):
        for col in range(0, 3):
            if board[row][col] == X:    
                x_count += 1
            elif board[row][col] == O:
                y_count += 1

    # no need to check for a terminal state
    if x_count == y_count:
        return X
    else:
        return O

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = []

    for row in range(0, 3):
        for col in range(0, 3):
            if board[row][col] == EMPTY:
                action = (row, col)
                actions.append(action)

    return actions

def print_board(board):
    for row in range(0, 3):
        print(' ', end='')
        for col in range(0, 3):
            if board[row][col] != None:
                print(board[row][col], end=' | ')
            else:
                print(' ', end=' | ')
        print()

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # deep copy the given board so that we don't modify it
    board_copy = copy.deepcopy(board)


    # print_board(board_copy)
    # print(action)
    # get the player
    which_player = player(board_copy)

    try:
        # if the state is not terminal
        if terminal(board_copy) == False:
            # make sure the cell specified by the action is empty
            if board_copy[action[0]][action[1]] == EMPTY:
                board_copy[action[0]][action[1]] = which_player
                return board_copy
            else:
                raise ValueError('The given action ' + str(action) + ' cannot be taken because the cell is not empty.')
        else:
            raise ValueError('No action can be taken. The game is over. ')
    except IndexError as e:
        print(e)
    except TypeError as e:
        print_board(board_copy)
        print(e)

# return X if X wins the game, O if O wins the game
# If there is no winner (either because board it's a tie, or in progress)
# NOTE: assuming there is only 1 winner. The board will never have both players with three-in-a-row
def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    utility_value = utility(board)

    if utility_value == 1:
        return X
    elif utility_value == -1:
        return O
    else:
        return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # if the board is full, return true
    if is_board_full(board):
        return True
    # if any player wins horizontally, return true
    if wins_horizontally(board) != 0:
        return True
    if wins_vertically(board) != 0:
        return True
    if wins_diagonally(board) != 0:
        return True

    return False

# helper function for terminal
def is_board_full(board):
    for row in range(0, 3):
        for col in range(0, 3):
            if board[row][col] == EMPTY:
                return False

    return True

# helper function for terminal and utility
# check if x or o wins horizontally (along the rows)
# return 0
def wins_horizontally(board):
    for row in range(0, 3):
        # keep track of the # of x's in a given row
        x_count = 0
        o_count = 0
        for col in range(0, 3):
            if board[row][col] == X:
                x_count += 1
            elif board[row][col] == O:
                o_count += 1

        # 3 x's (or o's) in a row, return true
        if x_count == 3:
            return 1
        elif o_count == 3:
            return -1

    return 0

# helper function for terminal and utility
# check if x or o wins vertically (across the columns)
def wins_vertically(board):
    for col in range(0, 3):
        x_count = 0
        o_count = 0
        for row in range(0, 3):
            if board[row][col] == X:
                x_count += 1
            elif board[row][col] == O:
                o_count += 1

        # 3 x's (or o's) vertically, return true
        if x_count == 3:
            return 1
        elif o_count == 3:
            return -1
    
    return 0


# helper function for terminal and utility
# check if x or o wins along the diagonal
def wins_diagonally(board):
    # check left to right
    if (board[0][0] == board[1][1] and board[1][1] == board[2][2]):
        if board[0][0] == X:
            return 1
        elif board[0][0] == O:
            return -1
        else:
            return 0
    # check right to left
    if (board[0][2] == board[1][1] and board[1][1] == board[2][0]):
        if board[0][2] == X:
           return 1
        elif board[0][2] == O:
            return -1
        else:
            return 0

    return 0

# NOTE: assume utility() is called only on a board when terminal(board) is True
def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    horizontal = wins_horizontally(board)
    vertical = wins_vertically(board)
    diagonal = wins_diagonally(board)

    if terminal(board):
        # if any player wins horizontally, return true
        if horizontal != 0:
            return horizontal
        elif vertical != 0:
            return vertical
        elif diagonal != 0:
            return diagonal
        else:
            # it's a draw
            return 0
    else:
        raise ValueError("The state should be terminal.")

# go through all the allowable actions and return the one that has the highest utility
#       using the min_value and max_value helper funcitons
def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # find out whose turn it is
    which_player = player(board)

    action_dict = {}

    # if X, maximize utility by calling max_value
    for action in actions(board):
        if which_player == X:
            # we are assuming O plays optimally, hence we call the min_value() method
            max_val = min_value(result(board, action))
            
            # add randomness so that the algorithm doesn't always choose the last move.
            # choose which key and action pair to keep
            # if the max_val is already a key in the dict
            if max_val in action_dict:
                # either overwrite the existing key, or leave it as is
                if random.randint(1, 2) == 1:
                    action_dict[max_val] = action
            else:
                action_dict[max_val] = action
        else:
            # we are assuming X plays optimally, hence we call the max_value() method.
            #       Then we will minimize it.
            min_val = max_value(result(board, action))
            # add randomness
            if min_val in action_dict:
                if random.randint(1, 2) == 1:
                    action_dict[min_val] = action
            else:
                action_dict[min_val] = action

    values = list(action_dict.keys())
    
    # for X, sort the dictionary keys (utilities) in descending order
    if which_player == X:
        values.sort(reverse=True)
    # for O, sort the dictionary keys (utilities) in ascending order
    else:
        values.sort()

    # get the optimal value from the sorted list. After sorting, the
    #       first element is the optimal
    optimal_value = values[0]

    # sort the dictionary based on keys (min or max value)
    sorted_dict = {i: action_dict[i] for i in values}

    # return the optimal move
    return sorted_dict[optimal_value]

# recursive algorithm to find the maximum utility of the opponent's (O)
#   possible moves. This keeps calling the min_value to find the
#   opponent's moves, and takes the maximum of those values
"""
    returns the max value that these path (action) will yield,
        assuming both players play optimally
"""
def max_value(board):
    global global_counter
    # to terminate the recursion
    if terminal(board):
        global_counter += 1
        return utility(board)

    # to guarantee at least one value is chosen
    v = -math.inf

    counter = 0
    for action in actions(board):
        # we are maximizing the score given what our (optimal) opponent will do
        v = max(v, min_value(result(board, action)))

    return v

# recursive algorithm to find the minimum utility of the opponent's (X) 
#   possible moves. This keeps calling the max_value to find the
#   opponent's moves, and takes the minimum of those values
"""
    returns the min value that these path (action) will yield,
        assuming both players play optimally
"""
def min_value(board):
    global global_counter
    # to terminate the recursion
    if terminal(board):
        global_counter += 1
        return utility(board)

    v = math.inf

    for action in actions(board):
        # we are minimizing the score given what our (optimal) opponent will do
        v = min(v, max_value(result(board, action)))

    return v