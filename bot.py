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



# Assume ChessBoard and Pawn are correctly implemented and imported

def test_get_piece_val():
    # Initialize ChessBoard
    board = ChessBoard()

    # Place a Pawn at position (1, 0) (or any desired position)
    board.print_board()
    
    # Test position (1, 0) where the Pawn is placed
    position = (0, 1)
    
    # Call get_piece_val method and print the result
    value = Bot.get_piece_val(board, position)
    print(board.get_piece(position))
    print(f"Value of piece at {position}: {value}")

# Run the test
test_get_piece_val()
