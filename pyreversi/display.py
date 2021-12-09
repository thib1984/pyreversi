"""
pyreversi use case
"""
from pyreversi.plateau import BLACK, WHITE, VIDEE
from columnar import columnar
from click import style
import os
import platform

from pyreversi.args import compute_args


def clear():
    if not compute_args().verbose and not compute_args().silent:
        command = "clear"
        if os.name in (
            "nt",
            "dos",
        ):  # If Machine is running on Windows, use cls
            command = "cls"
        os.system(command)


def display_plateau_and_score(plateau, scorew, scoreb,game):
    if not compute_args().silent:
        clear()
        data = []
        headers = ["", "A", "B", "C", "D", "E", "F", "G", "H"]
        for i in range(1, 9):
            ligne = []
            ligne.append(i)
            for j in range(0, 8):
                ligne.append(plateau[i - 1][j])
            data.append(ligne)
        if not compute_args().nocolor and not platform.system().lower() in "windows":    
            patterns = [
                (WHITE, lambda text: style(text, bg="green")),
                (BLACK, lambda text: style(text, bg="green")),
                (VIDEE, lambda text: style(text, bg="green")),
            ]
            maxcol=2
        else:
             patterns =[]
             maxcol=3   
        try:
            table = columnar(
                data,
                headers,
                no_borders=False,
                wrap_max=0,
                patterns=patterns,
                justify="c",
                max_column_width=maxcol,
            )
        except Exception:
            table = columnar(
                data,
                headers,
                no_borders=False,
                wrap_max=0,
                #patterns=patterns,
                justify="c",
                max_column_width=2,
            )                
        if compute_args().games!=0:
            info("BATCH MODE : game " + str(game) + " / " + str(compute_args().games))
        info(table)
        if compute_args().whitebot != -1:
            pw = WHITE + " (IA lvl " + str(compute_args().whitebot) + ")"
        else:
            pw = WHITE
        if compute_args().blackbot != -1:
            pb = BLACK + " (IA lvl " + str(compute_args().blackbot) + ")"
        else:
            pb = BLACK
        info(
            "score : "
            + pb
            + " "
            + str(scoreb).rjust(2, "0")
            + " - "
            + str(scorew).rjust(2, "0")
            + " "
            + pw
        )


def display_endgame(board, scorew, scoreb):
    info("game over!")
    if scorew > scoreb:
        info(WHITE + " wins !")
    elif scorew < scoreb:
        info(BLACK + " wins !")
    else:
        info("draw match !")


def display_cant_play(joueur):
    inputauto(joueur + " , no move available, press 'enter'")


def display_bot_move(joueur, position):
    info(joueur + " , plays move : " + position)
    inputauto("press any 'enter'")


def display_rules():
    warning("RULES OF REVERSI : ")
    warning(
        "- Reversi is a two-player strategy game played on an 8x8 board using discs that are colored white on one side and black on the other. One player plays the discs black side up while his opponent plays the discs white side up."
    )
    warning(
        "- The object of the game is to place your discs on the board so as to outflank your opponent's discs, flipping them over to your color. The player who has the most discs on the board at the end of the game wins."
    )
    warning(
        "- Note: For convenience, board positions are denoted by a letter representing the column (A through H) and a number representing the row (1 through 8). For example, the top-left square on the board is referred to as A1 while the square to the right of it is referred to as B1."
    )
    warning(
        "- Every game starts with four discs placed in the center of the board"
    )
    warning("- Black begins")
    warning(
        "- Players take turns making moves. A move consists of a player placing a disc of his color on the board. The disc must be placed so as to outflank one or more opponent discs, which are then flipped over to the current player's color."
    )
    warning(
        "- Outflanking your opponent means to place your disc such that it traps one or more of your opponent's discs between another disc of your color along a horizontal, vertical or diagonal line through the board square "
    )
    warning(
        "- If a player cannot make a legal move, he forfeits his turn and the other player moves again (this is also known as passing a turn). Note that a player may not forfeit his turn voluntarily. If a player can make a legal move on his turn, he must do so."
    )
    warning(
        "- The game ends when neither player can make a legal move. This includes when there are no more empty squares on the board or if one player has flipped over all of his opponent's discs (a situation commonly known as a wipeout)."
    )
    warning(
        "- The player with the most discs of his color on the board at the end of the game wins. The game is a draw if both players have the same number of discs."
    )
    warning(
        "- When making a move, you may outflank your opponent's discs in more than one direction. All outflanked discs are flipped."
    )
    warning(
        "source : https://documentation.help/Reversi-Rules/rules.htm"
    )


def debug(phrase):
    if compute_args().verbose:
        print("debug : " + phrase)

def info(phrase):
    if not compute_args().silent:
        print(phrase)

def warning(phrase):
    print(phrase)  

def inputauto(phrase):
    if not compute_args().auto and not compute_args().silent:    
        input(phrase)      
