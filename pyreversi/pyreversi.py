"""
pyreversi use case
"""
from columnar import columnar
from click import style
import os
import re
import random


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


BLACK = "\U000026AB"
WHITE = "\U000026AA"
VIDEE = " "


def play():
    my_plateau = [
        [VIDEE, VIDEE, VIDEE, VIDEE, VIDEE, VIDEE, VIDEE, VIDEE],
        [VIDEE, VIDEE, VIDEE, VIDEE, VIDEE, VIDEE, VIDEE, VIDEE],
        [VIDEE, VIDEE, VIDEE, VIDEE, VIDEE, VIDEE, VIDEE, VIDEE],
        [VIDEE, VIDEE, VIDEE, BLACK, WHITE, VIDEE, VIDEE, VIDEE],
        [VIDEE, VIDEE, VIDEE, WHITE, BLACK, VIDEE, VIDEE, VIDEE],
        [VIDEE, VIDEE, VIDEE, VIDEE, VIDEE, VIDEE, VIDEE, VIDEE],
        [VIDEE, VIDEE, VIDEE, VIDEE, VIDEE, VIDEE, VIDEE, VIDEE],
        [VIDEE, VIDEE, VIDEE, VIDEE, VIDEE, VIDEE, VIDEE, VIDEE],
    ]
    joueur = None
    while True:
        if joueur == None or joueur == BLACK:
            joueur = WHITE
        else:
            joueur = BLACK
        clearConsole()
        display_plateau(my_plateau)
        if not availableMoves(my_plateau, joueur):
            if joueur == WHITE:
                joueur_against = BLACK
            else:
                joueur_against = WHITE
            if not availableMoves(my_plateau, joueur_against):
                print("partie terminee!")
                if score(WHITE,my_plateau)>score(BLACK,my_plateau):
                    print("victoire "+WHITE+"!") 
                elif score(WHITE,my_plateau)<score(BLACK,my_plateau):   
                    print("victoire "+BLACK+"!") 
                else:
                    print("égalité!")         
                os.sys.exit(0)
            input(
                joueur
                + " , pas de mouvement possible, tapez une touche"
            )
            if joueur == None or joueur == BLACK:
                joueur = WHITE
            else:
                joueur = BLACK            
        while True:
            while True:
                if (joueur == WHITE and compute_args().whitebot==-1) or (joueur == BLACK and compute_args().blackbot==-1):
                    answer = input(joueur + " , enter your move : ")
                    if re.match("[A-H][1-8]", answer):
                        break
                    clearConsole()
                    display_plateau(my_plateau)
                    print("no valid place")
                else:
                    if joueur == WHITE:
                        level= compute_args().whitebot
                    else:
                        level= compute_args().blackbot                  
                    answer=calcul_bot(my_plateau, joueur,level)
                    print(joueur + " , plays move : " + answer)
                    input("tapez une touche")
                    break
            column = ord(answer[0].lower()) - 96 - 1
            line = int(answer[1]) - 1
            if is_valid_move(my_plateau, joueur, line, column):
                break
            clearConsole()
            display_plateau(my_plateau)
            print("no valid move")
        calcul_nouveau_plateau(my_plateau, joueur, line, column)

def calcul_bot(my_plateau, joueur, level):
    if level==0:
        return availableMoves(my_plateau,joueur)[0]
    else:
        return random.choice(availableMoves(my_plateau,joueur))

def availableMoves(my_plateau, joueur):
    moves=[]
    for i in range(0, 8):
        for j in range(0, 8):
            if is_valid_move(my_plateau, joueur, i, j):
                moves.append(chr(65+j)+str(i+1))
    if compute_args().verbose:
        print("availableMoves : " + str(moves))            
    return moves


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
    print(
        "score : "
        + WHITE
        + " "
        + str(score(WHITE, plateau))
        + " - "
        + str(score(BLACK, plateau))
        + " "
        + BLACK
    )


def score(joueur, my_plateau):
    return sum([i.count(joueur) for i in my_plateau])
