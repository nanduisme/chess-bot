from game import ChessBoard, Pawn, Piece

class Bot:
    def evaluate(self,board):        
        score = 0
        for row in range(8):
            for col in range (8):
                score+=self.get_piece_val(board,(row,col))
        return score         

    def minimax(self, board: ChessBoard, depth=0, to_min=True):
        if depth == 0 or board.is_checkmate():
            return self.evaluate(board)

        ret = float("inf") if to_min else float("-inf")
        valid_moves = []
        for row in range(8):
            for col in range(8):
                moves = board.get_valid_moves((row, col))
                if moves: 
                    valid_moves.extend(list(map(lambda x: ((row, col), x), moves)))

        return valid_moves

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
    moves = bot.minimax(board, 1)
    print(len(moves))

    print(board.get_valid_moves((6, 0)))

    # for start, stop in moves:
    #     clone = board.clone()
    #     clone.move_piece(start, stop)
    #     print(start, stop)
    #     clone.print_board()
    #     print("-----------------------")
    

