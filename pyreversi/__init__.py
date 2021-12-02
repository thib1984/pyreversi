"""
pyreversi init
"""


from pyreversi.args import compute_args
from pyreversi.pyreversi import play
from pyreversi.update import update
import colorama


def pyreversi():
    """
    pyreversi entry point
    """
    
    colorama.init()

    args = compute_args()
    if args.update:
        update()
    elif args.rules:
        print("RULES OF REVERSI : ")
        print("- Reversi is a two-player strategy game played on an 8x8 board using discs that are colored white on one side and black on the other. One player plays the discs black side up while his opponent plays the discs white side up.")
        print("- The object of the game is to place your discs on the board so as to outflank your opponent's discs, flipping them over to your color. The player who has the most discs on the board at the end of the game wins.")
        print("- Note: For convenience, board positions are denoted by a letter representing the column (A through H) and a number representing the row (1 through 8). For example, the top-left square on the board is referred to as A1 while the square to the right of it is referred to as B1.")
        print("- Every game starts with four discs placed in the center of the board")
        print("- Black begins")
        print("- Players take turns making moves. A move consists of a player placing a disc of his color on the board. The disc must be placed so as to outflank one or more opponent discs, which are then flipped over to the current player's color.")
        print("- Outflanking your opponent means to place your disc such that it traps one or more of your opponent's discs between another disc of your color along a horizontal, vertical or diagonal line through the board square ")
        print("- If a player cannot make a legal move, he forfeits his turn and the other player moves again (this is also known as passing a turn). Note that a player may not forfeit his turn voluntarily. If a player can make a legal move on his turn, he must do so.")
        print("- The game ends when neither player can make a legal move. This includes when there are no more empty squares on the board or if one player has flipped over all of his opponent's discs (a situation commonly known as a wipeout).")
        print("- The player with the most discs of his color on the board at the end of the game wins. The game is a draw if both players have the same number of discs.")
        print("- When making a move, you may outflank your opponent's discs in more than one direction. All outflanked discs are flipped.")
        print("source : https://documentation.help/Reversi-Rules/rules.htm")
    else:
        play()
