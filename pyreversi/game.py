"""
pyreversi use case
"""
from pyreversi.human import ask_move
from pyreversi.display import (
    display_plateau,
    display_endgame,
    display_cant_play,
    display_bot_move
)
from pyreversi.plateau import (
    INIT_PLATEAU,
    opposite_joueur,
)
from pyreversi.rules import (
    end_game,
    is_valid_move,
    calcul_nouveau_plateau,
    can_play,
    end_game,
)
from pyreversi.bot import calcul_bot, level_bot, is_bot
import os
import re


from pyreversi.args import compute_args


def play():

    board = INIT_PLATEAU
    joueur = None

    while True:
        joueur = opposite_joueur(joueur)
        display_plateau(board)
        
        if end_game(board):
            display_endgame(board)
            os.sys.exit(0)
        if not can_play(board, joueur):
            display_cant_play(joueur)
            joueur = opposite_joueur(joueur)

        if not is_bot(joueur):
            position = ask_move
        else:
            position = calcul_bot(board, joueur, level_bot(joueur))
            display_bot_move(joueur, position)
        calcul_nouveau_plateau(board, joueur, position)


