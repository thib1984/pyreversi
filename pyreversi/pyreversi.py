"""
pyreversi use case
"""
from typing import Collection
from columnar import columnar
from click import style
import os
import re
import random
import copy


from pyreversi.args import compute_args


def clearConsole():
    if not compute_args().verbose:
        command = "clear"
        if os.name in (
            "nt",
            "dos",
        ):  # If Machine is running on Windows, use cls
            command = "cls"
        os.system(command)

CLOSE_CORNERS = [
    "A2",
    "B2",
    "B1",
    "G1",
    "G2",
    "H2",
    "A7",
    "B7",
    "B8",
    "G8",
    "G7",
    "H7",
]
CORNERS = ["A1", "A8", "H1", "H8"]
BLACK = "\U000026AB"
WHITE = "\U000026AA"
VIDEE = " "
INIT_PLATEAU = [
    [VIDEE, VIDEE, VIDEE, VIDEE, VIDEE, VIDEE, VIDEE, VIDEE],
    [VIDEE, VIDEE, VIDEE, VIDEE, VIDEE, VIDEE, VIDEE, VIDEE],
    [VIDEE, VIDEE, VIDEE, VIDEE, VIDEE, VIDEE, VIDEE, VIDEE],
    [VIDEE, VIDEE, VIDEE, WHITE, BLACK, VIDEE, VIDEE, VIDEE],
    [VIDEE, VIDEE, VIDEE, BLACK, WHITE, VIDEE, VIDEE, VIDEE],
    [VIDEE, VIDEE, VIDEE, VIDEE, VIDEE, VIDEE, VIDEE, VIDEE],
    [VIDEE, VIDEE, VIDEE, VIDEE, VIDEE, VIDEE, VIDEE, VIDEE],
    [VIDEE, VIDEE, VIDEE, VIDEE, VIDEE, VIDEE, VIDEE, VIDEE],
]


def play():

    my_plateau = INIT_PLATEAU
    joueur = None
    
    while True:
        joueur = opposite_joueur(joueur)
        clearConsole()
        display_plateau(my_plateau)
        if not availableMoves(my_plateau, joueur):
            joueur_against = opposite_joueur(joueur)
            if not availableMoves(my_plateau, joueur_against):
                print("game over!")
                if score(WHITE, my_plateau) > score(
                    BLACK, my_plateau
                ):
                    print(WHITE + " wins !")
                elif score(WHITE, my_plateau) < score(
                    BLACK, my_plateau
                ):
                    print(BLACK + " wins !")
                else:
                    print("draw match !")
                os.sys.exit(0)
            if not compute_args().auto:
                input(
                    joueur
                    + " , no move available, press any key"
                )
            joueur = opposite_joueur(joueur)
        while True:
            while True:
                if (
                    joueur == WHITE and compute_args().whitebot == -1
                ) or (
                    joueur == BLACK and compute_args().blackbot == -1
                ):
                    answer = input(joueur + " , enter your move : ")
                    if re.match("[A-H][1-8]", answer):
                        break
                    clearConsole()
                    display_plateau(my_plateau)
                    print(
                        "no valid place - enter [A-H][1-8] format. For example : B3"
                    )
                else:
                    level = level_bot(joueur)
                    answer = calcul_bot(my_plateau, joueur, level)
                    print(joueur + " , plays move : " + answer)
                    if not compute_args().auto:
                        input("press any key")
                    break
            column = ord(answer[0].lower()) - 96 - 1
            line = int(answer[1]) - 1
            if is_valid_move(my_plateau, joueur, line, column):
                break
            clearConsole()
            display_plateau(my_plateau)
            print("no valid move")
        calcul_nouveau_plateau(my_plateau, joueur, line, column)


def level_bot(joueur):
    if joueur == WHITE:
        level = compute_args().whitebot
    else:
        level = compute_args().blackbot
    return level


def opposite_joueur(joueur):
    if joueur == BLACK:
        joueur_against = WHITE
    else:
        joueur_against = BLACK
    return joueur_against


def calcul_bot(my_plateau, joueur, level):
    available_moves = availableMoves(my_plateau, joueur)
    if not compute_args().fix:
        random.shuffle(available_moves)
    if compute_args().verbose:
        print("availableMoves : " + str(available_moves))
        liste_safe_moves(my_plateau, joueur, available_moves)
    if level == 0:
        choice = available_moves[0]
        return choice
    if level == 1:
        best_move = ""
        best_gain = 0
        for move in available_moves:
            sandbox = copy.deepcopy(my_plateau)
            calcul_nouveau_plateau(
                sandbox,
                joueur,
                int(move[1]) - 1,
                ord(move[0].lower()) - 96 - 1,
            )
            gain = score(joueur, sandbox) - score(joueur, my_plateau)
            if gain > best_gain:
                if compute_args().verbose:
                    print(
                        "better move : "
                        + move
                        + " with "
                        + str(gain)
                        + " pts"
                    )
                best_move = move
                best_gain = gain
        if compute_args().verbose:
            print(
                "best move : "
                + best_move
                + " with "
                + str(best_gain)
                + " pts"
            )
        return best_move
    if level == 2:
        moves = available_moves
        # on vise les coins
        corners = copy.deepcopy(CORNERS)
        if not compute_args().fix:
            random.shuffle(corners)
        for move in corners:
            if move in moves:
                if compute_args().verbose:
                    print("corner available!")
                return move
        # on evite d'offrir les coins


        close_corners = copy.deepcopy(CLOSE_CORNERS)
        if not compute_args().fix:
            random.shuffle(close_corners)
        for move in close_corners:
            if move in moves and len(moves) > 1:
                if compute_args().verbose:
                    print(move + " can offer a corner! Remove it")
                moves.remove(move)
        best_move = ""
        best_gain = 0
        for move in moves:
            sandbox = copy.deepcopy(my_plateau)
            calcul_nouveau_plateau(
                sandbox,
                joueur,
                int(move[1]) - 1,
                ord(move[0].lower()) - 96 - 1,
            )
            gain = score(joueur, sandbox) - score(joueur, my_plateau)
            if gain > best_gain:
                if compute_args().verbose:
                    print(
                        "better move : "
                        + move
                        + " with "
                        + str(gain)
                        + " pts"
                    )
                best_move = move
                best_gain = gain
        if compute_args().verbose:
            print(
                "best move : "
                + best_move
                + " with "
                + str(best_gain)
                + " pts"
            )
        return best_move
    if level == 3:
        moves = available_moves
        # on vise les coins
        corners = copy.deepcopy(CORNERS)
        if not compute_args().fix:
            random.shuffle(corners)
        for move in corners:
            if move in moves:
                if compute_args().verbose:
                    print("corner available!")
                return move
        # on evite d'offrir les coins
        close_corners = copy.deepcopy(CLOSE_CORNERS)
        if not compute_args().fix:
            random.shuffle(close_corners)
        for move in close_corners:
            if move in moves and len(moves) > 1:
                if compute_args().verbose:
                    print(move + " can offer a corner! Remove it")
                moves.remove(move)
        best_move = ""
        best_gain = -65
        for move in moves:
            sandbox = copy.deepcopy(my_plateau)
            calcul_nouveau_plateau(
                sandbox,
                joueur,
                int(move[1]) - 1,
                ord(move[0].lower()) - 96 - 1,
            )
            gain = score(joueur, sandbox) - score(joueur, my_plateau)
            futur_moves = availableMoves(sandbox, opposite_joueur(joueur))
            if not futur_moves:
                gain = gain - 0
            best_down_gain = 0
            for futur_move in futur_moves:
                futur_sandbox = copy.deepcopy(sandbox)
                calcul_nouveau_plateau(
                    futur_sandbox,
                    opposite_joueur(joueur),
                    int(futur_move[1]) - 1,
                    ord(futur_move[0].lower()) - 96 - 1,
                )
                down_gain = score(
                    opposite_joueur(joueur), futur_sandbox
                ) - score(opposite_joueur(joueur), sandbox)
                if down_gain > best_down_gain:
                    best_down_gain = down_gain
            gain = gain - best_down_gain
            if gain > best_gain:
                if compute_args().verbose:
                    print(
                        "better move : "
                        + move
                        + " with "
                        + str(gain)
                        + " pts"
                    )
                best_move = move
                best_gain = gain
        if compute_args().verbose:
            print(
                "best move : "
                + best_move
                + " with "
                + str(best_gain)
                + " pts"
            )
        return best_move


    if level == 4:
        moves = available_moves
        # on vise les coins
        corners = copy.deepcopy(CORNERS)
        if not compute_args().fix:
            random.shuffle(corners)
        for move in corners:
            if move in moves:
                if compute_args().verbose:
                    print("corner available!")
                return move
        # on evite d'offrir les coins
        close_corners = copy.deepcopy(CLOSE_CORNERS)
        delete_safe_close_corners(my_plateau, joueur, close_corners)
        if not compute_args().fix:
            random.shuffle(close_corners)
        for move in close_corners:
            if move in moves:
                if compute_args().verbose:
                    print(move + " can perhaps offer a corner! Remove it")
                moves.remove(move)
        if moves == []:
            if compute_args().verbose:
                print("we should verify the best of bad choices")            
            for move in close_corners:
                if is_valid_move(
                    my_plateau,
                    joueur,
                    int(move[1]) - 1,
                    ord(move[0].lower()) - 96 - 1,
                ):
                    sandbox = copy.deepcopy(my_plateau)
                    calcul_nouveau_plateau(
                        sandbox,
                        joueur,
                        int(move[1]) - 1,
                        ord(move[0].lower()) - 96 - 1,
                    )
                    if move=="A2" or move=="B1" or move=="B2":
                        if not is_valid_move(
                            sandbox,
                            opposite_joueur(joueur),
                            0,
                            0,
                        ):
                            moves.append(move)                          
                    if move=="G1" or move=="G2" or move=="H2":
                        if not is_valid_move(
                            sandbox,
                            opposite_joueur(joueur),
                            0,
                            7,
                        ):
                            moves.append(move) 
                    if move=="A7" or move=="B7" or move=="B8":
                        if not is_valid_move(
                            sandbox,
                            opposite_joueur(joueur),
                            7,
                            0,
                        ):
                            moves.append(move)
                    if move=="H7" or move=="G7" or move=="G8":
                        if not is_valid_move(
                            sandbox,
                            opposite_joueur(joueur),
                            7,
                            7,
                        ):
                            moves.append(move)  
        if moves==[]:
            moves = availableMoves(my_plateau, joueur)
            if not compute_args().fix:
                random.shuffle(available_moves)                                               
        best_move = ""
        best_gain = -65
        for move in moves:
            sandbox = copy.deepcopy(my_plateau)
            calcul_nouveau_plateau(
                sandbox,
                joueur,
                int(move[1]) - 1,
                ord(move[0].lower()) - 96 - 1,
            )
            gain = score_with_protected(
                joueur, sandbox
            ) - score_with_protected(joueur, my_plateau)
            futur_moves = availableMoves(sandbox, opposite_joueur(joueur))
            if not futur_moves:
                gain = gain - 0
            best_down_gain = 0
            for futur_move in futur_moves:
                futur_sandbox = copy.deepcopy(sandbox)
                calcul_nouveau_plateau(
                    futur_sandbox,
                    opposite_joueur(joueur),
                    int(futur_move[1]) - 1,
                    ord(futur_move[0].lower()) - 96 - 1,
                )
                down_gain = score_with_protected(
                    opposite_joueur(joueur), futur_sandbox
                ) - score_with_protected(opposite_joueur(joueur), sandbox)
                if down_gain > best_down_gain:
                    best_down_gain = down_gain
            gain = gain - best_down_gain
            if gain > best_gain:
                if compute_args().verbose:
                    print(
                        "better move : "
                        + move
                        + " with "
                        + str(gain)
                        + " pts"
                    )
                best_move = move
                best_gain = gain
        if compute_args().verbose:
            print(
                "best move : "
                + best_move
                + " with "
                + str(best_gain)
                + " pts"
            )
        return best_move

def delete_safe_close_corners(my_plateau, joueur, close_corners):
    if my_plateau[0][0] == joueur:
        close_corners.remove("A2")
        close_corners.remove("B2")
        close_corners.remove("B1")
    if my_plateau[0][7] == joueur:
        close_corners.remove("G1")
        close_corners.remove("G2")
        close_corners.remove("H2")
    if my_plateau[7][0] == joueur:
        close_corners.remove("A7")
        close_corners.remove("B7")
        close_corners.remove("B8")
    if my_plateau[7][7] == joueur:
        close_corners.remove("G7")
        close_corners.remove("H7")
        close_corners.remove("G8")

def liste_safe_moves(my_plateau, joueur, available_moves):
    for move in available_moves:
        sandbox = copy.deepcopy(my_plateau)
        calcul_nouveau_plateau(
                sandbox,
                joueur,
                int(move[1]) - 1,
                ord(move[0].lower()) - 96 - 1,
            )
        if is_safe_place(
                sandbox,
                joueur,
                int(move[1]) - 1,
                ord(move[0].lower()) - 96 - 1,
            ):
            if compute_args().verbose:
                print(move + " is a safe move")


def availableMoves(my_plateau, joueur):
    moves = []
    for i in range(0, 8):
        for j in range(0, 8):
            if is_valid_move(my_plateau, joueur, i, j):
                moves.append(chr(65 + j) + str(i + 1))
    return moves


def is_safe_place(my_plateau, joueur, line, column):

    safe = True
    for l in range(line, 8):
        for c in range(min(column + (l - line), 7), -1, -1):
            if my_plateau[l][c] != joueur:
                safe = False
    if safe:
        return True

    safe = True
    for l in range(line, 8):
        for c in range(max(column - (l - line), 0), 8):
            if my_plateau[l][c] != joueur:
                safe = False
    if safe:
        return True

    safe = True
    for l in range(line, -1, -1):
        for c in range(min(column + (line - l), 7), -1, -1):
            if my_plateau[l][c] != joueur:
                safe = False
    if safe:
        return True

    safe = True
    for l in range(line, -1, -1):
        for c in range(max(column - (line - l), 0), 8):
            if my_plateau[l][c] != joueur:
                safe = False
    if safe:
        return True

    safe = True
    for c in range(column, 8):
        for l in range(min(line + (c - column), 7), -1, -1):
            if my_plateau[l][c] != joueur:
                safe = False
    if safe:
        return True

    safe = True
    for c in range(column, 8):
        for l in range(max(line - (c - column), 0), 8):
            if my_plateau[l][c] != joueur:
                safe = False
    if safe:
        return True

    safe = True
    for c in range(column, -1, -1):
        for l in range(min(line + (column - c), 7), -1, -1):
            if my_plateau[l][c] != joueur:
                safe = False
    if safe:
        return True

    safe = True
    for c in range(column, -1, -1):
        for l in range(max(line - (column - c), 0), 8):
            if my_plateau[l][c] != joueur:
                safe = False
    if safe:
        return True

    return False


def is_valid_move(my_plateau, joueur, line, column):
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


def calcul_nouveau_plateau(my_plateau, joueur, line, column):
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


def display_plateau(plateau):
    data = []
    headers = ["", "A", "B", "C", "D", "E", "F", "G", "H"]
    for i in range(1, 9):
        ligne = []
        ligne.append(i)
        for j in range(0, 8):
            ligne.append(plateau[i - 1][j])
        data.append(ligne)
    patterns = [
        (WHITE, lambda text: style(text, bg="green")),
        (BLACK, lambda text: style(text, bg="green")),
        (VIDEE, lambda text: style(text, bg="green")),
    ]

    table = columnar(
        data,
        headers,
        no_borders=False,
        wrap_max=0,
        patterns=patterns,
        justify="c",
        max_column_width=2,
    )
    print(table)
    if compute_args().whitebot != -1:
        pw = WHITE + " (IA lvl " + str(compute_args().whitebot)+")"
    else:
        pw = WHITE
    if compute_args().blackbot != -1:
        pb = BLACK + " (IA lvl " + str(compute_args().blackbot)+")"
    else:
        pb = BLACK               
    print(
        "score : "
        + pb
        + " "
        + str(score(BLACK, plateau))
        + " - "
        + str(score(WHITE, plateau))
        + " "
        + pw
    )


def score(joueur, my_plateau):
    return sum([i.count(joueur) for i in my_plateau])


def score_with_protected(joueur, my_plateau):
    score = 0
    for line in range(0, 8):
        for column in range(0, 8):
            if my_plateau[line][column] == joueur:
                if is_safe_place(my_plateau, joueur, line, column):
                    score = score + 3
                else:
                    score = score + 1
    return score
