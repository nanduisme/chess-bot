from game import ChessBoard, Pawn, Piece, BLACK, WHITE
import time

class Bot:
    def __init__(self):
        self.evaluation_count = 0

    def evaluate(self, board):
        score = 0
        for row in range(8):
            for col in range(8):
                score += self.get_piece_val(board, (row, col))
        return score

    def minimax(self, board: ChessBoard, alpha , beta,depth=0, white_turn=False):
        self.evaluation_count = 0

        if depth == 0 or board.is_checkmate():
            return self.evaluate(board), None

        valid_moves = []
        for row in range(8):
            for col in range(8):
                if (piece := board.get_piece((row, col))) != " " and (
                    (piece.color == WHITE and white_turn)
                    or (piece.color == BLACK and not white_turn)
                ):
                    moves = board.get_valid_moves((row, col))
                    if moves:
                        valid_moves.extend(list(map(lambda x: ((row, col), x), moves)))

        if white_turn:
            ret = float("-inf")
            ret_move = ((-1, -1), (-1, -1))
            for move in valid_moves:
                self.evaluation_count += 1
                clone = board.clone()
                clone.move_piece(*move)
                val, _ = self.minimax(clone,alpha,beta, depth - 1, not white_turn)
                ret = max(ret, val )
                alpha = max(alpha, ret)
                ret_move=move
                if beta <= alpha:
                     break
                else:
                    self.evaluation_count += 1
            return ret, ret_move
        else:
            ret = float("+inf")
            ret_move = ((-1, -1), (-1, -1))
            for move in valid_moves:
                self.evaluation_count += 1
                clone = board.clone()
                clone.move_piece(*move)
                val,_ = self.minimax(clone,alpha,beta,depth - 1, white_turn)
                ret = min(ret, val)
                beta = min(beta, ret)
                ret_move = move
                if beta <= alpha:
                    break
            return ret, ret_move
    
    def evaluation_counter(self):
        '''
        Returns the times the board was evaluated
        '''
        return self.evaluation_count
        

    def get_piece_val(self, board, pos):
        """
        This funciton should return the value of a piece in a given position in the gien board
        """

        piece = board.get_piece(pos)
        row, col = pos
        if isinstance(piece, Piece):  # Check if the piece is a pawn
            if piece.color == "black":
                return -(piece.bonus[::-1][row][col] + piece.value)
            elif piece.color == "white":
                return piece.bonus[row][col] + piece.value
        return 0  # Default if no bonus is applicable


                
def play_vs_bot():
    board = ChessBoard()  # Initialize the chessboard
    bot = Bot()  # Initialize the bot

    while True:
        board.print_board()  # Display the board
        print()

        # Player move
        try:
            start = tuple(
                input(
                    f"{board.turn.capitalize()}'s turn. Enter start position (FileRank): "
                ).upper()
            )
            start = ChessBoard.file_rank_to_coords(start[0], start[1])
            end = tuple(input("Enter the end position (FileRank): ").upper())
            end = ChessBoard.file_rank_to_coords(end[0], end[1])
        except Exception as e:
            print(f"Invalid input: {e}. Please try again.")
            continue

        if board.is_valid_move(start, end):
            board.move_piece(start, end)  # Execute player's move

            # Switch to bot's turn
            board.turn = BLACK

            # Check for checkmate or check
            if board.is_in_check(board.turn):
                if board.is_checkmate():
                    print(f"{'Black' if board.turn == WHITE else 'White'} wins!")
                    break
                else:
                    print("Check!")

            board.print_board()
            print()

            # Bot's move
            start_time = time.time()  # Start time for bot’s move
            val, move = bot.minimax(board, float("-inf"), float("+inf"), depth=3, white_turn=False)
            move_time = time.time() - start_time  # Calculate time taken

            # Execute bot's move
            board.move_piece(*move)
            print(f"Bot played: {move}")
            print(f"Time taken: {move_time:.4f} seconds")
            print(f"Evaluations: {bot.evaluation_counter()}")

            # Switch back to player's turn
            board.turn = WHITE

            # Check for checkmate or check
            if board.is_in_check(board.turn):
                if board.is_checkmate():
                    print(f"{'Black' if board.turn == WHITE else 'White'} wins!")
                    break
                else:
                    print("Check!")
        else:
            print("Invalid move. Try again.")

if __name__ == "__main__":
    play_vs_bot()