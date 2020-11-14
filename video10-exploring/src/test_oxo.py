from oxo import Board, Oxo, WIN, LOSE, DRAW

def test_gameplay():
    game = Oxo()
    game.board.set("XO.",
                   "XO.",
                   "...")
    assert(game.choose_best_move("X") == WIN)

    game.board.set("XOX",
                   "OXO",
                   "O.O")
    assert(game.choose_best_move("X") == DRAW)
    
    game.board.set("O.O",
                   "X..",
                   "XXO")
    assert(game.choose_best_move("X") == LOSE)

    # extra test to ensure that O wins immediately if it can, rather
    # than winning sometime later.
    game.board.set("X.X",
                   "OO.",
                   "X..")
    assert(game.choose_best_move("O") == WIN)
    # not only should O win, but it must win by playing at 2,1
    assert(game.board.pieces[0][1] == '.')
    assert(game.board.pieces[2][1] == '.')
    assert(game.board.pieces[2][2] == '.')
    assert(game.board.pieces[1][2] == 'O')

    game.board.set("...",
                   "...",
                   "...")
    assert(game.choose_best_move("X") == DRAW)
    
