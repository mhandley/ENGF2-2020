from oxo import Board, WIN, LOSE, DRAW

def test_board():
    board = Board()
    board.set("X..",
              "X..",
              "..X")
    assert(not board.wins("X"))
    board.play((0,2),"X")
    assert(board.wins("X"))

    board.set("X..",
              "X..",
              "X..")
    assert(board.wins("X"))

    board.set("..X",
              "..X",
              "..X")
    assert(board.wins("X"))
    
    board.set("XXX",
              "...",
              "...")
    assert(board.wins("X"))

    board.set("...",
              "...",
              "XXX")
    assert(board.wins("X"))

    board.set("X..",
              ".X.",
              "..X")
    assert(board.wins("X"))

    board.set("..X",
              ".X.",
              "X..")
    assert(board.wins("X"))

    board.set("OOO",
              "...",
              "...")
    assert(not board.wins("X"))
    assert(board.wins("O"))

