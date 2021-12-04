"""
pyreversi init
"""


from pyreversi.args import compute_args
from pyreversi.game import play
from pyreversi.update import update
from pyreversi.display import display_rules
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
        display_rules()
    else:
        play()

