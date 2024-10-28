from game import ChessBoard, Pawn, Piece, BLACK, WHITE
import time
import random


class Bot:
    def __init__(self):
        self.evaluation_count = 0

    def evaluate(self, board):
        self.evaluation_count += 1
        score = 0
        for row in range(8):
            for col in range(8):
                score += self.get_piece_val(board, (row, col))
        return score

    def order_moves(self, board, moves, white_turn=False):
        # Prioritize moves that capture pieces or achieve promotion
        scored_moves = []
        for move in moves:
            start, end = move
            end_piece = board.get_piece(end)

            move_score = 0
            if end_piece != " ":
                move_score = 10 * abs(self.get_piece_val(board, start)) - abs(
                    self.get_piece_val(board, end)
                )

            if (
                isinstance(end_piece, Pawn)
                and (end[0] == 7 and end_piece.color == WHITE)
                or (end[0] == 0 and end_piece.color == BLACK)
            ):
                move_score += 900  # Queen promotion value

            scored_moves.append((move_score, move))

        # Sort moves by score, higher scores first for better pruning potential
        scored_moves.sort(reverse=True, key=lambda x: x[0])
        return [move for score, move in scored_moves]

    def minimax(self, board, alpha, beta, depth=0, white_turn=False):
        if depth == 0 or board.is_checkmate():
            return self.evaluate(board), None

        valid_moves = []
        for row in range(8):
            for col in range(8):
                piece = board.get_piece((row, col))
                if piece != " " and (
                    (piece.color == WHITE and white_turn)
                    or (piece.color == BLACK and not white_turn)
                ):
                    moves = board.get_valid_moves((row, col))
                    if moves:
                        valid_moves.extend(
                            ((row, col), move) for move in moves
                        )

        valid_moves = self.order_moves(board, valid_moves, white_turn)
        best_move = None

        if white_turn:
            max_eval = float("-inf")
            for move in valid_moves:
                clone = board.clone()
                clone.move_piece(*move, "q")
                eval, _ = self.minimax(
                    clone, alpha, beta, depth - 1, not white_turn
                )
                if eval > max_eval:
                    max_eval, best_move = eval, move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, best_move

        else:
            min_eval = float("inf")
            for move in valid_moves:
                clone = board.clone()
                clone.move_piece(*move, "q")
                eval, _ = self.minimax(
                    clone, alpha, beta, depth - 1, not white_turn
                )
                if eval < min_eval:
                    min_eval, best_move = eval, move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, best_move

    def get_piece_val(self, board, pos):
        piece = board.get_piece(pos)
        row, col = pos
        if isinstance(piece, Piece):
            return (
                piece.bonus[row][col] + piece.value
                if piece.color == WHITE
                else -(piece.bonus[::-1][row][col] + piece.value)
            )
        return 0


def play_vs_bot():
    board = ChessBoard()
    bot = Bot()

    while True:
        board.print_board()
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
            board.move_piece(start, end)
            board.turn = BLACK

            if board.is_in_check(board.turn):
                if board.is_checkmate():
                    print(
                        f"{'Black' if board.turn == WHITE else 'White'} wins!"
                    )
                    break
                else:
                    print("Check!")

            board.print_board()
            print()

            # Bot's move
            bot.evaluation_count = 0
            start_time = time.time()
            val, move = bot.minimax(
                board, float("-inf"), float("inf"), depth=3, white_turn=False
            )
            move_time = time.time() - start_time

            # Execute bot's move
            board.move_piece(*move)
            print(f"Bot played: {move}")
            print(f"Time taken: {move_time:.4f} seconds")
            print(f"Evaluations: {bot.evaluation_count}")

            board.turn = WHITE

            if board.is_in_check(board.turn):
                if board.is_checkmate():
                    print(
                        f"{'Black' if board.turn == WHITE else 'White'} wins!"
                    )
                    break
                else:
                    print("Check!")
        else:
            print("Invalid move. Try again.")


def get_metrics():
    board = ChessBoard.from_fen(
        "r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R"
    )
    bot = Bot()
    board.print_board()
    board.move_piece((6, 4), (2, 0))
    board.print_board()

    bot.evaluation_count = 0
    start = time.time()
    val, move = bot.minimax(board, float("-inf"), float("inf"), 5, False)
    end = time.time() - start

    board.move_piece(*move, "q")
    board.print_board()

    print("Time taken to play: ", end)
    print("Eval count: ", bot.evaluation_count)


if __name__ == "__main__":
    get_metrics()
