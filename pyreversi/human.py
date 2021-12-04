from pyreversi.display import display_plateau
from pyreversi.rules import is_valid_move
import re

def ask_move(my_plateau,joueur):
    while True:
        answer = input(joueur + " , enter your move : ")
        if not re.match("[A-H][1-8]", answer):
            display_plateau(my_plateau)
            print(
                "no valid place - enter [A-H][1-8] format. For example : B3"
            )
        elif not is_valid_move(my_plateau, joueur, answer):
            display_plateau(my_plateau)
            print("no valid move")         
        else:
            return answer