"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None


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
    # Count number of X's and O's on the board
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)
    
    # Determine the next player based on counts
    if x_count <= o_count:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                possible_actions.add((i, j))
    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    action_i, action_j = action
    if board[action_i][action_j] is not EMPTY:
        raise ValueError("Invalid action: Cell is already occupied.")
    
    new_board = [row[:] for row in board]  # Create a deep copy of the board
    new_board[action_i][action_j] = player(board)  # Place the current player's mark
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    
    if board[0][0] == board[0][1] == board[0][2] != EMPTY:
        return board[0][0]
    elif board[1][0] == board[1][1] == board[1][2] != EMPTY:
        return board[1][0]
    elif board[2][0] == board[2][1] == board[2][2] != EMPTY:
        return board[2][0]
    elif board[0][0] == board[1][0] == board[2][0] != EMPTY:
        return board[0][0]
    elif board[0][1] == board[1][1] == board[2][1] != EMPTY:
        return board[0][1]
    elif board[0][2] == board[1][2] == board[2][2] != EMPTY:
        return board[0][2]
    elif board[0][0] == board[1][1] == board[2][2] != EMPTY:
        return board[0][0]
    elif board[0][2] == board[1][1] == board[2][0] != EMPTY:
        return board[0][2]
    
    else:
        return None



def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    if winner(board) is not None:
        return True
    


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0

def max_value(board):
    if terminal(board):
        return utility(board)
    
    v = -math.inf
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    return v

def min_value(board):
    if terminal(board):
        return utility(board)
    
    v = math.inf
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    return v

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    current_player = player(board)
    
    if current_player == X:
        best_value = -math.inf
        best_action = None
        
        for action in actions(board):
            value = min_value(result(board, action))
            if value > best_value:
                best_value = value
                best_action = action
                
        return best_action
    
    else:  # current_player == O
        best_value = math.inf
        best_action = None
        
        for action in actions(board):
            value = max_value(result(board, action))
            if value < best_value:
                best_value = value
                best_action = action
                
        return best_action
    