"""
pyreversi use case
"""
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


BLACK = "\U000026AB"
WHITE = "\U000026AA"
VIDEE = " "


def play():
    my_plateau = [
        [VIDEE, VIDEE, VIDEE, VIDEE, VIDEE, VIDEE, VIDEE, VIDEE],
        [VIDEE, VIDEE, VIDEE, VIDEE, VIDEE, VIDEE, VIDEE, VIDEE],
        [VIDEE, VIDEE, VIDEE, VIDEE, VIDEE, VIDEE, VIDEE, VIDEE],
        [VIDEE, VIDEE, VIDEE, WHITE, BLACK, VIDEE, VIDEE, VIDEE],
        [VIDEE, VIDEE, VIDEE, BLACK, WHITE, VIDEE, VIDEE, VIDEE],
        [VIDEE, VIDEE, VIDEE, VIDEE, VIDEE, VIDEE, VIDEE, VIDEE],
        [VIDEE, VIDEE, VIDEE, VIDEE, VIDEE, VIDEE, VIDEE, VIDEE],
        [VIDEE, VIDEE, VIDEE, VIDEE, VIDEE, VIDEE, VIDEE, VIDEE],
    ]
    joueur = None
    while True:
        joueur = switch(joueur)
        clearConsole()
        display_plateau(my_plateau)
        if not availableMoves(my_plateau, joueur):
            joueur_against = opposite_joueur(joueur)
            if not availableMoves(my_plateau, joueur_against):
                print("partie terminee!")
                if score(WHITE,my_plateau)>score(BLACK,my_plateau):
                    print("victoire "+WHITE+"!") 
                elif score(WHITE,my_plateau)<score(BLACK,my_plateau):   
                    print("victoire "+BLACK+"!") 
                else:
                    print("égalité!")         
                os.sys.exit(0)
            if not compute_args().auto:
                input(
                    joueur
                    + " , pas de mouvement possible, tapez une touche"
                )
            joueur = switch(joueur)         
        while True:
            while True:
                if (joueur == WHITE and compute_args().whitebot==-1) or (joueur == BLACK and compute_args().blackbot==-1):
                    answer = input(joueur + " , enter your move : ")
                    if re.match("[A-H][1-8]", answer):
                        break
                    clearConsole()
                    display_plateau(my_plateau)
                    print("no valid place - enter [A-H][1-8] format. For example : B3")
                else:
                    level = level_bot(joueur)                  
                    answer=calcul_bot(my_plateau, joueur,level)
                    print(joueur + " , plays move : " + answer)
                    if not compute_args().auto:
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

def level_bot(joueur):
    if joueur == WHITE:
        level= compute_args().whitebot
    else:
        level= compute_args().blackbot
    return level

def opposite_joueur(joueur):
    if joueur == WHITE:
        joueur_against = BLACK
    else:
        joueur_against = WHITE
    return joueur_against

def switch(joueur):
    if joueur == None or joueur == BLACK:
        joueur = WHITE
    else:
        joueur = BLACK
    return joueur

def calcul_bot(my_plateau, joueur, level):
    available_moves = availableMoves(my_plateau,joueur)
    if compute_args().random:
        random.shuffle(available_moves)
    if compute_args().verbose:
        print("availableMoves : " + str(available_moves))  
    if level==0:
        choice = available_moves[0]
        if compute_args().verbose:
            print("choice : " + choice)
        return choice    
    if level==1:
        best_move=""
        best_gain=0
        for move in available_moves:
            sandbox=copy.deepcopy(my_plateau)
            calcul_nouveau_plateau (sandbox,joueur,int(move[1]) - 1,ord(move[0].lower()) - 96 - 1)     
            gain = score(joueur,sandbox)-score(joueur,my_plateau)
            if gain>best_gain:
                if compute_args().verbose:
                    print("better move : " + move + " with " + str(gain) + " pts")
                best_move=move
                best_gain=gain
        if compute_args().verbose:
            print("best move : " + best_move + " with " + str(best_gain) + " pts")                
        return best_move
    if level==2:
        moves=available_moves
        #on vise les coins
        corners = ["A1","A8","H1","H8"]
        if compute_args().random:
            random.shuffle(corners)
        for move in corners:
            if move in moves:
                if compute_args().verbose:
                    print("corner available!")
                return move
        #on evite d'offrir les coins
        close_corners = ["A2","B2","B1","G1","G2","H2","A7","B7","B8","G8","G7","H7"]
        if compute_args().random:
            random.shuffle(close_corners)        
        for move in close_corners:
            if move in moves and len(moves)>1:
                if compute_args().verbose:
                    print(move + " can offer a corner! Remove it")
                moves.remove(move)       
        best_move=""
        best_gain=0
        for move in moves:
            sandbox=copy.deepcopy(my_plateau)
            calcul_nouveau_plateau(sandbox,joueur,int(move[1]) - 1,ord(move[0].lower()) - 96 - 1)     
            gain = score(joueur,sandbox)-score(joueur,my_plateau)
            if gain>best_gain:
                if compute_args().verbose:
                    print("better move : " + move + " with " + str(gain) + " pts")                
                best_move=move
                best_gain=gain
        if compute_args().verbose:
            print("best move : " + best_move + " with " + str(best_gain) + " pts")                   
        return best_move        
    if level==3:
        moves=available_moves
        #on vise les coins
        corners = ["A1","A8","H1","H8"]
        if compute_args().random:
            random.shuffle(corners)
        for move in corners:
            if move in moves:
                if compute_args().verbose:
                    print("corner available!")
                return move
        #on evite d'offrir les coins
        close_corners = ["A2","B2","B1","G1","G2","H2","A7","B7","B8","G8","G7","H7"]
        if compute_args().random:
            random.shuffle(close_corners)        
        for move in close_corners:
            if move in moves and len(moves)>1:
                if compute_args().verbose:
                    print(move + " can offer a corner! Remove it")
                moves.remove(move)       
        best_move=""
        best_gain=-65
        for move in moves:
            sandbox=copy.deepcopy(my_plateau)
            calcul_nouveau_plateau(sandbox,joueur,int(move[1]) - 1,ord(move[0].lower()) - 96 - 1)     
            gain = score(joueur,sandbox)-score(joueur,my_plateau)
            futur_moves=availableMoves(sandbox,switch(joueur))  
            if not futur_moves:
                gain = gain - 0
            best_down_gain=0
            for futur_move in futur_moves:
                futur_sandbox=copy.deepcopy(sandbox)
                calcul_nouveau_plateau(futur_sandbox,switch(joueur),int(futur_move[1]) - 1,ord(futur_move[0].lower()) - 96 - 1)     
                down_gain = score(switch(joueur),futur_sandbox)-score(switch(joueur),sandbox)              
                if down_gain>best_down_gain:             
                    best_down_gain=down_gain
            gain = gain - best_down_gain
            if gain>best_gain:
                if compute_args().verbose:
                    print("better move : " + move + " with " + str(gain) + " pts")                
                best_move=move
                best_gain=gain
        if compute_args().verbose:
            print("best move : " + best_move + " with " + str(best_gain) + " pts")                   
        return best_move 
    

def availableMoves(my_plateau, joueur):
    moves=[]
    for i in range(0, 8):
        for j in range(0, 8):
            if is_valid_move(my_plateau, joueur, i, j):
                moves.append(chr(65+j)+str(i+1))          
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
