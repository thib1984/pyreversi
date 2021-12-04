"""
pyreversi use case
"""
from pyreversi.plateau import (
    CORNERS,
    CLOSE_CORNERS,
    WHITE,
    BLACK,
    opposite_joueur,
)
from pyreversi.rules import (
    is_valid_move,
    score,
    calcul_nouveau_plateau,
    availableMoves,
)
import random
import copy


from pyreversi.args import compute_args


def level_bot(joueur):
    if joueur == WHITE:
        level = compute_args().whitebot
    else:
        level = compute_args().blackbot
    return level


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
                move,
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
                move,
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
                move,
            )
            gain = score(joueur, sandbox) - score(joueur, my_plateau)
            futur_moves = availableMoves(
                sandbox, opposite_joueur(joueur)
            )
            if not futur_moves:
                gain = gain - 0
            best_down_gain = 0
            for futur_move in futur_moves:
                futur_sandbox = copy.deepcopy(sandbox)
                calcul_nouveau_plateau(
                    futur_sandbox,
                    opposite_joueur(joueur),
                    move,
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
                    print(
                        move
                        + " can perhaps offer a corner! Remove it"
                    )
                moves.remove(move)
        if moves == []:
            if compute_args().verbose:
                print("we should verify the best of bad choices")
            for move in close_corners:
                if is_valid_move(
                    my_plateau,
                    joueur,
                    move,
                ):
                    sandbox = copy.deepcopy(my_plateau)
                    calcul_nouveau_plateau(
                        sandbox,
                        joueur,
                        move,
                    )
                    if move == "A2" or move == "B1" or move == "B2":
                        if not is_valid_move(
                            sandbox, opposite_joueur(joueur), "A1"
                        ):
                            moves.append(move)
                    if move == "G1" or move == "G2" or move == "H2":
                        if not is_valid_move(
                            sandbox, opposite_joueur(joueur), "H1"
                        ):
                            moves.append(move)
                    if move == "A7" or move == "B7" or move == "B8":
                        if not is_valid_move(
                            sandbox, opposite_joueur(joueur), "A8"
                        ):
                            moves.append(move)
                    if move == "H7" or move == "G7" or move == "G8":
                        if not is_valid_move(
                            sandbox, opposite_joueur(joueur), "H8"
                        ):
                            moves.append(move)
        if moves == []:
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
                move,
            )
            gain = score_with_protected(
                joueur, sandbox
            ) - score_with_protected(joueur, my_plateau)
            futur_moves = availableMoves(
                sandbox, opposite_joueur(joueur)
            )
            if not futur_moves:
                gain = gain - 0
            best_down_gain = 0
            for futur_move in futur_moves:
                futur_sandbox = copy.deepcopy(sandbox)
                calcul_nouveau_plateau(
                    futur_sandbox,
                    opposite_joueur(joueur),
                    move,
                )
                down_gain = score_with_protected(
                    opposite_joueur(joueur), futur_sandbox
                ) - score_with_protected(
                    opposite_joueur(joueur), sandbox
                )
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
            move,
        )
        if is_safe_place(
            sandbox,
            joueur,
            int(move[1]) - 1,
            ord(move[0].lower()) - 96 - 1,
        ):
            if compute_args().verbose:
                print(move + " is a safe move")


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


def is_bot(joueur):
    return (joueur == WHITE and compute_args().whitebot > -1) or (
        joueur == BLACK and compute_args().blackbot > -1
    )
