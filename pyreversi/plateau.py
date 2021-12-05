from pyreversi.args import compute_args
import platform

CORNERS = ["A1", "A8", "H1", "H8"]
BLACK = "\U000026AB"
WHITE = "\U000026AA"
if compute_args().nocolor or platform.system().lower() in "windows":
    BLACK = "X"
    WHITE = "O"    
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


def opposite_joueur(joueur):
    if joueur == BLACK:
        joueur_against = WHITE
    else:
        joueur_against = BLACK
    return joueur_against