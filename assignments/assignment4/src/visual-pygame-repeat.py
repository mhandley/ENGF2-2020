from adversary import RandomAdversary
from arguments import parser
from board import Board, Direction, Rotation
from constants import BOARD_WIDTH, BOARD_HEIGHT, DEFAULT_SEED, INTERVAL, BLOCK_LIMIT
from player import Player, SelectedPlayer

import pygame

BLACK = (10, 10, 10)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

CELL_WIDTH = 20
CELL_HEIGHT = 20

EVENT_FORCE_DOWN = pygame.USEREVENT + 1
FRAMES_PER_SECOND = 60


class Square(pygame.sprite.Sprite):
    def __init__(self, color, x, y):
        super().__init__()

        self.image = pygame.Surface([CELL_WIDTH, CELL_HEIGHT])
        self.image.fill(color)

        self.rect = self.image.get_rect()
        self.rect.x = x * CELL_WIDTH
        self.rect.y = y * CELL_HEIGHT


def render(screen, board):
    screen.fill(BLACK)

    sprites = pygame.sprite.Group()

    # Add the cells already on the board for drawing.
    for (x, y) in board:
        sprites.add(Square(pygame.Color(board.cellcolor[x, y]), x, y))

    if board.falling is not None:
        # Add the cells of the falling block for drawing.
        for (x, y) in board.falling:
            sprites.add(Square(pygame.Color(board.falling.color), x, y))

    if board.next is not None:
        for (x, y) in board.next:
            sprites.add(
                Square(
                    pygame.Color(board.next.color),
                    x + board.width + 2,
                    y+1
                )
            )

    sprites.draw(screen)

    pygame.draw.line(
        screen,
        BLUE,
        (board.width * CELL_WIDTH + 2, 0),
        (board.width * CELL_WIDTH + 2, board.height * CELL_HEIGHT)
    )

    # Update window title with score.
    pygame.display.set_caption(f'Score: {board.score}')


class UserPlayer(Player):
    """
    A simple user player that reads moves from the command line.
    """

    key_to_move = {
        pygame.K_RIGHT: Direction.Right,
        pygame.K_LEFT: Direction.Left,
        pygame.K_DOWN: Direction.Down,
        pygame.K_SPACE: Direction.Drop,
        pygame.K_UP: Rotation.Clockwise,
        pygame.K_z: Rotation.Anticlockwise,
        pygame.K_x: Rotation.Clockwise,
    }

    def choose_action(self, board):
        while True:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                raise SystemExit
            elif event.type == pygame.KEYUP:
                if event.key in self.key_to_move:
                    return self.key_to_move[event.key]
                elif event.key == pygame.K_ESCAPE:
                    raise SystemExit
            elif event.type == EVENT_FORCE_DOWN:
                return None


def check_stop():
    for event in pygame.event.get():
        if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
            raise SystemExit
        elif event.type == pygame.QUIT:
            raise SystemExit


def run(seed):
    board = Board(BOARD_WIDTH, BOARD_HEIGHT)
    adversary = RandomAdversary(seed, BLOCK_LIMIT)

    args = parser.parse_args()
    if args.manual:
        player = UserPlayer()
    else:
        player = SelectedPlayer()

    pygame.init()

    screen = pygame.display.set_mode([
        (BOARD_WIDTH + 6) * CELL_WIDTH,
        BOARD_HEIGHT * CELL_HEIGHT
    ])

    clock = pygame.time.Clock()

    # Set timer to force block down when no input is given.
    pygame.time.set_timer(EVENT_FORCE_DOWN, INTERVAL)

    for move in board.run(player, adversary):
        render(screen, board)
        pygame.display.flip()

        # If we are not playing manually, clear the events.
        if not args.manual:
            check_stop()

        clock.tick(FRAMES_PER_SECOND)
    print("Seed:", seed, " Score:", board.score)
    #while True:
    #    check_stop()


if __name__ == '__main__':
    for seed in range(1000):
        run(seed)
