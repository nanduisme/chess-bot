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
    from rich.prompt import Prompt

    board = ChessBoard()
    bot = Bot()

    history = open("./prev.txt", "w")

    while True:
        board.print_board()
        print()

        # Player move (simple manual input for demonstration)
        while True:
            start = tuple(
                Prompt.ask(
                    f"{board.turn.capitalize()}'s turn. Enter start position (FileRank)"
                ).upper()
            )
            start = ChessBoard.file_rank_to_coords(start[0], start[1])

            if (piece := board.get_piece(start)) == " ":
                print("[red b]X[/] Please enter a valid starting move")
                continue

            if not (moves := piece.valid_moves(board, start)):
                print(f"[red b]X[/] Piece cannot move")
                continue

            end = Prompt.ask(
                "Enter the end position (FileRank)",
                choices=[ChessBoard.coords_to_file_rank(*move) for move in moves],
                case_sensitive=False,
            ).upper()
            end = ChessBoard.file_rank_to_coords(end[0], end[1])

            break

        if board.is_valid_move(start, end):
            board.move_piece(start, end)
            history.write(
                ChessBoard.coords_to_file_rank(*start)
                + ChessBoard.coords_to_file_rank(*end)
                + "\n"
            )

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

            val, move = bot.minimax(board, 3, False)
            board.move_piece(*move)
            history.write(
                ChessBoard.coords_to_file_rank(*move[0])
                + ChessBoard.coords_to_file_rank(*move[1])
                + "\n"
            )

            board.turn = WHITE

            if board.is_in_check(board.turn):
                if board.is_checkmate():
                    print(f"{'Black' if board.turn == WHITE else 'White'} wins!")
                    break
                else:
                    print("check!!")

        else:
            print("Invalid move. Try again.")

    history.close()


if __name__ == "__main__":
    play_vs_bot()
