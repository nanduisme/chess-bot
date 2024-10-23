# from .game import ChessBoard,Pawn
from game import ChessBoard, Pawn, Piece

class Bot:
    def evaluate(self):        
        ...

    def minimax(self, board: ChessBoard, depth=0):
        if depth == 0 or board.is_checkmate():
            return ...
        
    def get_piece_val(self, board, pos):
        '''
        This funciton should return the value of a piece in a given position in the gien board
        '''

        piece = board.get_piece(pos)
        row, col = pos
        if isinstance(piece, Piece):  # Check if the piece is a pawn
            if piece.color=='black':
                return -(piece.bonus[::-1][row][col]+piece.value)
            elif piece.color=='white':
                return piece.bonus[row][col]+piece.value
        return 0  # Default if no bonus is applicable



