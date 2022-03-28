from pyreversi.display import display_plateau_and_score
from pyreversi.rules import is_valid_move,score, available_moves
from pyreversi.display import warning
from pyreversi.plateau import WHITE,BLACK
import re

def ask_move(board,joueur,game,winb,winw,draw):
    while True:
        answer = input(joueur + " , enter your move : ")
        if not re.match("[a-h][1-8]", answer.lower()):
            display_plateau_and_score(board,score(WHITE,board), score(BLACK,board),game,winb,winw,draw,available_moves(board, joueur))
            warning(
                "invalid place - enter [A-H][1-8] format. For example : B3 or b3"
            )
        elif not is_valid_move(board, joueur, answer):
            display_plateau_and_score(board, score(WHITE,board), score(BLACK,board),game,winb,winw,draw,available_moves(board, joueur))
            warning("invalid move")         
        else:
            return answer
