from pyreversi.plateau import BLACK, WHITE, VIDEE, opposite_joueur


def is_valid_move(my_plateau, joueur, position):

    column = ord(position[0].lower()) - 96 - 1
    line = int(position[1]) - 1

    if my_plateau[int(line)][int(column)] != VIDEE:
        return False
    if (
        not is_one_in(my_plateau, joueur, line, column, 1, 0)
        and not is_one_in(my_plateau, joueur, line, column, 1, 1)
        and not is_one_in(my_plateau, joueur, line, column, 0, 1)
        and not is_one_in(my_plateau, joueur, line, column, -1, 1)
        and not is_one_in(my_plateau, joueur, line, column, -1, 0)
        and not is_one_in(my_plateau, joueur, line, column, -1, -1)
        and not is_one_in(my_plateau, joueur, line, column, 0, -1)
        and not is_one_in(my_plateau, joueur, line, column, 1, -1)
    ):
        return False
    return True


def is_one_in(my_plateau, joueur, line, column, dirline, dircol):
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
            or my_plateau[int(check_line)][int(check_column)] == VIDEE
        ):
            return False
        if my_plateau[int(check_line)][int(check_column)] == joueur:
            if not check_one:
                return False
            else:
                return True
        if (
            my_plateau[int(check_line)][int(check_column)]
            == joueur_against
        ):
            check_one = True


def return_in(my_plateau, joueur, line, column, dirline, dircol):
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
        if my_plateau[int(check_line)][int(check_column)] == VIDEE:
            return
        if (
            check_one
            and my_plateau[int(check_line)][int(check_column)]
            == joueur
        ):
            return
        if (
            my_plateau[int(check_line)][int(check_column)]
            == joueur_against
        ):
            my_plateau[int(check_line)][int(check_column)] = joueur
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


def score(joueur, my_plateau):
    return sum([i.count(joueur) for i in my_plateau])


def calcul_nouveau_plateau(my_plateau, joueur, position):

    column = ord(position[0].lower()) - 96 - 1
    line = int(position[1]) - 1

    my_plateau[int(line)][int(column)] = joueur
    if is_one_in(my_plateau, joueur, line, column, 1, 0):
        return_in(my_plateau, joueur, line, column, 1, 0)
    if is_one_in(my_plateau, joueur, line, column, 1, 1):
        return_in(my_plateau, joueur, line, column, 1, 1)
    if is_one_in(my_plateau, joueur, line, column, 0, 1):
        return_in(my_plateau, joueur, line, column, 0, 1)
    if is_one_in(my_plateau, joueur, line, column, -1, 1):
        return_in(my_plateau, joueur, line, column, -1, 1)
    if is_one_in(my_plateau, joueur, line, column, -1, 0):
        return_in(my_plateau, joueur, line, column, -1, 0)
    if is_one_in(my_plateau, joueur, line, column, -1, -1):
        return_in(my_plateau, joueur, line, column, -1, -1)
    if is_one_in(my_plateau, joueur, line, column, 0, -1):
        return_in(my_plateau, joueur, line, column, 0, -1)
    if is_one_in(my_plateau, joueur, line, column, 1, -1):
        return_in(my_plateau, joueur, line, column, 1, -1)


def availableMoves(my_plateau, joueur):
    moves = []
    for i in range(0, 8):
        for j in range(0, 8):
            move = chr(65 + i) + str(j + 1)
            if is_valid_move(my_plateau, joueur, move):
                moves.append(move)
    return moves

def can_play(my_plateau,joueur):
    if availableMoves(my_plateau, joueur) ==[]:
        return False
    return True  

def end_game(my_plateau):
    if not can_play(my_plateau, WHITE) and not can_play(my_plateau, BLACK):
        return True
    return False  


