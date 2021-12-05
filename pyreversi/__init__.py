"""
pyreversi init
"""


from pyreversi.args import compute_args
from pyreversi.game import play
from pyreversi.plateau import BLACK,WHITE
from pyreversi.update import update
from pyreversi.display import display_rules, warning
from pyreversi.bot import is_bot
import os


def pyreversi():
    """
    pyreversi entry point
    """
    

    args = compute_args()
    if args.update:
        update()
    elif args.rules:
        display_rules()
    else:
        if compute_args().silent and (not is_bot(BLACK) or not is_bot(WHITE)):
            warning("use --silent only for two bots player")
            os.sys.exit(0)
        play()

