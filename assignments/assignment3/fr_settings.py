# Simple Frogger Game.  Mark Handley, UCL, 2018

from enum import Enum

CANVAS_WIDTH = 1000
CANVAS_HEIGHT = 700
GRID_SIZE = 40
LOG_HEIGHT = 30

class Direction(Enum):
    UP = 0
    LEFT = 1
    RIGHT = 2
    DOWN = 3

