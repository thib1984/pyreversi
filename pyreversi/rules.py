
from pyreversi.plateau import BLACK, WHITE, VIDEE
from pyreversi.display import debug

def is_valid_move(board, joueur, position):

    column = ord(position[0].lower()) - 96 - 1
    line = int(position[1]) - 1

    if board[int(line)][int(column)] != VIDEE:
        return False
    if (
        not is_one_in(board, joueur, line, column, 1, 0)
        and not is_one_in(board, joueur, line, column, 1, 1)
        and not is_one_in(board, joueur, line, column, 0, 1)
        and not is_one_in(board, joueur, line, column, -1, 1)
        and not is_one_in(board, joueur, line, column, -1, 0)
        and not is_one_in(board, joueur, line, column, -1, -1)
        and not is_one_in(board, joueur, line, column, 0, -1)
        and not is_one_in(board, joueur, line, column, 1, -1)
    ):
        return False
    return True


def is_one_in(board, joueur, line, column, dirline, dircol):
    check_line = line
    check_column = column
    if joueur == WHITE:
        joueur_against = BLACK
    else:
        joueur_against = WHITE
    check_one = False
    while True:
        check_line = check_line + dirline
        check_column = check_column + dircol

        if (
            check_column > 7
            or check_line > 7
            or check_column < 0
            or check_line < 0
            or board[int(check_line)][int(check_column)] == VIDEE
        ):
            return False
        if board[int(check_line)][int(check_column)] == joueur:
            return check_one
        if (
            board[int(check_line)][int(check_column)]
            == joueur_against
        ):
            check_one = True


def return_in(board, joueur, line, column, dirline, dircol):
    check_line = line
    check_column = column
    if joueur == WHITE:
        joueur_against = BLACK
    else:
        joueur_against = WHITE
    check_one = False
    while True:
        check_line = check_line + dirline
        check_column = check_column + dircol

        if check_column > 7 or check_line > 7:
            return
        if check_column < 0 or check_line < 0:
            return
        if board[int(check_line)][int(check_column)] == VIDEE:
            return
        if (
            check_one
            and board[int(check_line)][int(check_column)]
            == joueur
        ):
            return
        if (
            board[int(check_line)][int(check_column)]
            == joueur_against
        ):
            board[int(check_line)][int(check_column)] = joueur
            check_one = True

    # N
    # E
    # W
    # NE
    # SE
    # SO
    # NO
    #
    #


def score(joueur, board):
    return sum([i.count(joueur) for i in board])


def calcul_nouveau_plateau(board, joueur, position):

    column = ord(position[0].lower()) - 96 - 1
    line = int(position[1]) - 1

    board[int(line)][int(column)] = joueur
    if is_one_in(board, joueur, line, column, 1, 0):
        return_in(board, joueur, line, column, 1, 0)
    if is_one_in(board, joueur, line, column, 1, 1):
        return_in(board, joueur, line, column, 1, 1)
    if is_one_in(board, joueur, line, column, 0, 1):
        return_in(board, joueur, line, column, 0, 1)
    if is_one_in(board, joueur, line, column, -1, 1):
        return_in(board, joueur, line, column, -1, 1)
    if is_one_in(board, joueur, line, column, -1, 0):
        return_in(board, joueur, line, column, -1, 0)
    if is_one_in(board, joueur, line, column, -1, -1):
        return_in(board, joueur, line, column, -1, -1)
    if is_one_in(board, joueur, line, column, 0, -1):
        return_in(board, joueur, line, column, 0, -1)
    if is_one_in(board, joueur, line, column, 1, -1):
        return_in(board, joueur, line, column, 1, -1)


def available_moves(board, joueur):
    moves = []
    for i in range(0, 8):
        for j in range(0, 8):
            move = chr(65 + i) + str(j + 1)
            if is_valid_move(board, joueur, move):
                moves.append(move)
    debug("available_moves for " + joueur +" : " + str(moves))                 
    return moves

def can_play(board,joueur):
    if available_moves(board, joueur) ==[]:
        return False
    return True  

def end_game(board):
    if not can_play(board, WHITE) and not can_play(board, BLACK):
        return True
    return False  


