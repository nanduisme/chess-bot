from .game import ChessBoard

class Bot:
    def __init__(self, game: ChessBoard):
        self.game: ChessBoard = game

    def evaluate(self, board=None):
        if board is None:
            board = self.board
        
        ...

    def minimax(self, board: ChessBoard=None, depth=0):
        if board is None:
            board = self.game

        if depth == 0 or board.is_checkmate():
            return ...

