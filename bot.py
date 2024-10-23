# from .game import ChessBoard,Pawn
from game import ChessBoard, Pawn, Piece

class Bot:
    def evaluate(self,board):        
        score = 0
        for row in range(8):
            for col in range (8):
                score+=self.get_piece_val(board,(row,col))
        return score         

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


if __name__ == "__main__":
    board = ChessBoard()
    bot = Bot()
    board.print_board()
    board.move_piece(ChessBoard.file_rank_to_coords("D",2),ChessBoard.file_rank_to_coords("D",4))
    board.print_board()
    print(bot.evaluate(board))
    