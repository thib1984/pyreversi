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
    else:
        play()
