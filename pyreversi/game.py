"""
pyreversi use case
"""
from pyreversi.human import ask_move
from pyreversi.display import (
    display_plateau_and_score,
    display_endgame,
    display_cant_play,
    display_bot_move,
    debug,
    warning,
    clear
)
from pyreversi.plateau import (
    BLACK,
    WHITE,
    INIT_PLATEAU,
    opposite_joueur,
)
from pyreversi.rules import (
    end_game,
    score,
    calcul_nouveau_plateau,
    can_play,
    end_game,
)
from pyreversi.bot import calcul_bot, level_bot, is_bot
import os
import copy

from pyreversi.args import compute_args


def play():

    try:
        board = copy.deepcopy(INIT_PLATEAU)
        joueur = None
        game=1
        winw=0
        winb=0
        draw=0
        totw=0
        totb=0
        while True:
            joueur = opposite_joueur(joueur)
            display_plateau_and_score(board,score(WHITE,board), score(BLACK,board),game)
            debug("compute if endgame")
            if end_game(board):
                display_endgame(board, score(WHITE,board), score(BLACK,board))
                if compute_args().games == 0:
                    os.sys.exit(0)
                else:
                    totw=totw+score(WHITE,board)
                    totb=totb+score(BLACK,board)
                    if score(WHITE,board)>score(BLACK,board):
                        winw=winw+1
                    elif score(WHITE,board)<score(BLACK,board):
                        winb=winb+1
                    else:
                        draw=draw+1       
                    if game == compute_args().games:
                        clear()
                        if compute_args().whitebot != -1:
                            pw = WHITE + " (IA lvl " + str(compute_args().whitebot) + ")"
                        else:
                            pw = WHITE
                        if compute_args().blackbot != -1:
                            pb = BLACK + " (IA lvl " + str(compute_args().blackbot) + ")"
                        else:
                            pb = BLACK 
                        warning("FIN BATCH : " + pb + " - " + pw)
                        warning("Victories " + BLACK + " : " + str(winb))
                        warning("Victories " + WHITE + " : " + str(winw))
                        warning("Draws : " + str(draw))
                        warning("Points " + BLACK + " : " + str(totb))
                        warning("Points " + WHITE + " : " + str(totw))
                        os.sys.exit(0)
                    else:
                        game=game+1
                        board = copy.deepcopy(INIT_PLATEAU)
                        joueur = None
                        joueur = opposite_joueur(joueur)
                        display_plateau_and_score(board,score(WHITE,board), score(BLACK,board),game)                                        
            debug("compute if " + joueur + " can play")    
            if not can_play(board, joueur):
                display_cant_play(joueur)
                joueur = opposite_joueur(joueur)

            if not is_bot(joueur):
                position = ask_move(board,joueur,game)
            else:
                position = calcul_bot(board, joueur, level_bot(joueur))
                display_bot_move(joueur, position)
            calcul_nouveau_plateau(board, joueur, position)
    except KeyboardInterrupt:
        warning("")
        warning("Game was interrupted by the user. bye!")
        os.sys.exit()

