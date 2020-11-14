from copy import deepcopy
WIN_IMMEDIATE = 0
WIN = 1
LOSE = 2
DRAW = 3

class Board:
    def __init__(self):
        self.reset_board()

    # reset the board to empty
    def reset_board(self):
        self.pieces = [['.', '.', '.'],\
                       ['.', '.', '.'],\
                       ['.', '.', '.']]
        self.count = 0   # number of pieces already played
        
    def __str__(self):
        s = ""
        for y in range(0,3):
            for x in range(0,3):
                s += self.pieces[y][x]
            s += "\n"
        return s

    # helper function to quickly set board position from list of three strings
    def set(self, row1, row2, row3):
        board = [row1, row2, row3]
        self.count = 0
        y = 0
        for row in board:
            for x in range(0,3):
                if row[x] != ".":
                    self.count += 1
                self.pieces[y][x] = row[x]
            y += 1

    # is there still somewhere to play
    def unfinished(self):
        return self.count < 9

    # wins returns True if "player" has won?
    def wins(self, player):
        colcounts = [0,0,0]
        d1count = 0
        d2count = 0
        for y in range(0,3):
            rowcount = 0
            for x in range(0,3):
                if self.pieces[y][x] == player:
                    rowcount+=1
                    colcounts[x] += 1
                    if colcounts[x] == 3:
                        return True
                    if x == y:
                        d1count += 1
                        if d1count == 3:
                            return True
                    if x == 2 - y:
                        d2count += 1
                        if d2count == 3:
                            return True
            if rowcount == 3:
                return True
        return False

    # play a move for "player" at position "pos"
    def play(self, pos, player):
        x,y = pos
        self.pieces[y][x] = player
        self.count += 1

    # is the square at position "pos" empty?
    def empty(self, pos):
        x,y = pos
        return self.pieces[y][x] == "."

# helper function to alternate between players
def other_player(player):
    if player == "X":
        return "O"
    elif player == "O":
        return "X"
    else:
        print("Bad player: ", player)

# The main class to play the game        
class Oxo:
    def __init__(self):
        self.board = Board()

    # clone the game state, so we can try out moves without affecting
    # the current board
    def clone(self):
        return deepcopy(self)

    # choose the best move for "player" starting from the current
    # board position.  Return whether this move will result in a win,
    # draw, or lose
    def choose_best_move(self, player):
        if self.board.unfinished() == False:
            return DRAW
        winning_move = None
        drawing_move = None
        losing_move = None
        for y in range(0,3):
            for x in range(0,3):
                pos = x,y
                if not self.board.empty(pos):
                    continue
                result = self.test_move(pos, player)
                if result == WIN_IMMEDIATE:
                    self.board.play(pos, player)
                    return WIN
                if result == WIN:
                    winning_move = pos
                if result == DRAW:
                    drawing_move = pos
                if result == LOSE:
                    losing_move = pos
        # player has not won
        if winning_move:
            self.board.play(winning_move, player)
            return WIN
        if drawing_move:
            self.board.play(drawing_move, player)
            return DRAW
        if losing_move:
            self.board.play(losing_move, player)
            return LOSE
        assert(False)
        return DRAW

    def test_move(self, pos, player):
        game = self.clone()
        game.board.play(pos, player)
        if game.board.wins(player):
            return WIN_IMMEDIATE
        result = game.choose_best_move(other_player(player))
        if result == WIN:
            return LOSE
        elif result == LOSE:
            return WIN
        return DRAW

    # Ask the user to choose their move.  Moves are comma-separated
    # pairs of x, y coordinates, with x, y in range 1..3 as humans
    # don't usually count from zero
    def input_move(self):
        while True:
            print("Enter move: x, y where 1 <= x <= 3 and 1 <= y <= 3")
            st = input()
            lst = st.split(",")
            if len(lst) != 2:
                print("Invalid move")
                continue
            x = int(lst[0])
            y = int(lst[1])
            if x < 1 or x > 3 or y < 1 or y > 3:
                print("Invalid move")
                continue
            x -= 1
            y -= 1
            if self.board.empty( (x,y) ) == False:
                print("Invalid move (position occupied)")
                continue
            return x,y

    # play a game
    def play(self):
        while self.board.unfinished():
            # player's move
            move = self.input_move()
            self.board.play(move, "X")
            print("X plays:\n\n" + str(self.board))
            if self.board.wins("X"):
                print("You win!")
                return

            # computer's move
            result = self.choose_best_move("O")
            print("O plays:\n\n" + str(self.board))
            if result == WIN:
                print("You lose!")
                return
            if result == LOSE:
                print("You win!")
                return
        
if __name__ == "__main__":
    game = Oxo()
    game.play()
