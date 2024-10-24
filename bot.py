from game import ChessBoard, Pawn, Piece, BLACK, WHITE


class Bot:
    def evaluate(self, board):
        score = 0
        for row in range(8):
            for col in range(8):
                score += self.get_piece_val(board, (row, col))
        return score

    def minimax(self, board: ChessBoard, depth=0, white_turn=False):
        if depth == 0 or board.is_checkmate():
            return self.evaluate(board), (-1, -1)

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

        ret = float("-inf") if white_turn else float("inf")
        ret_move = ((-1, -1), (-1, -1))
        for move in valid_moves:
            clone = board.clone()
            clone.move_piece(*move)
            val, _ = self.minimax(clone, depth - 1, not white_turn)

            if (val < ret and not white_turn) or (val > ret and white_turn):
                ret = val
                ret_move = move

        return ret, ret_move

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
    board = ChessBoard()
    bot = Bot()

    while True:
        board.print_board()
        print()

        # Player move (simple manual input for demonstration)
        start = tuple(
            input(
                f"{board.turn.capitalize()}'s turn. Enter start position (FileRank): "
            ).upper()
        )
        start = ChessBoard.file_rank_to_coords(start[0], start[1])
        end = tuple(input("Enter the end position (FileRank): ").upper())
        end = ChessBoard.file_rank_to_coords(end[0], end[1])

        if board.is_valid_move(start, end):
            board.move_piece(start, end)

            # Switch turns
            board.turn = BLACK

            # Check for checkmate

            if board.is_in_check(board.turn):
                if board.is_checkmate():
                    print(f"{'Black' if board.turn == WHITE else 'White'} wins!")
                    break
                else:
                    print("check!!")

            board.print_board()
            print()

            val, move = bot.minimax(board, 2, False)
            board.move_piece(*move)
            board.turn = WHITE

            if board.is_in_check(board.turn):
                if board.is_checkmate():
                    print(f"{'Black' if board.turn == WHITE else 'White'} wins!")
                    break
                else:
                    print("check!!")

        else:
            print("Invalid move. Try again.")


if __name__ == "__main__":
    play_vs_bot()
