import copy 
# Constants
WHITE, BLACK = 'white', 'black'  # Defining constants for white and black pieces

# Chess Pieces Classes
class Piece:
    def __init__(self, color):
        self.value = None
        self.bonus = [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0]
        ]


        self.color = color  # Every piece has a color (white or black)
        self.has_moved = False  # Tracks whether the piece has moved (important for castling)

    def __repr__(self):
        pass

    def valid_moves(self, pos):
        pass  # This is a placeholder method to be implemented by specific piece types

# Class for Pawn Piece
class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.value = 100
        self.bonus = [[0, 0, 0, 0, 0, 0, 0, 0],
                      [50, 50, 50, 50, 50, 50, 50, 50],
                      [10, 10, 20, 30, 30, 20, 10, 10],
                      [5, 5, 10, 25, 25, 10, 5, 5],
                      [0, 0, 0, 20, 20, 0, 0, 0],
                      [5, -5, -10, 0, 0, -10, -5, 5],
                      [5, 10, 10, -20, -20, 10, 10, 5],
                      [0, 0, 0, 0, 0, 0, 0, 0]]

    def valid_moves(self, board, pos, en_passant_target=None):
        moves = []  # List to store valid moves for the pawn
        x, y = pos  # Current position of the pawn
        direction = -1 if self.color == WHITE else 1  # Pawns move up (for white) or down (for black)

        # Move forward by one square
        if 0 <= x + direction and x + direction < 8 and board.get_piece((x + direction, y)) == ' ':
            moves.append((x + direction, y))  # Add the forward move
            # Two-square move from starting position
            if not self.has_moved and 0 <= x + 2 * direction and x + 2 * direction < 8 and board.get_piece((x + 2 * direction, y)) == ' ':
                moves.append((x + 2 * direction, y))  # Add the two-square move

        # Diagonal captures
        for dy in [-1, 1]:  # Check both diagonal directions (left and right)
            if 0 <= y + dy < 8:  # Ensure it's within board limits
                target = board.get_piece((x + direction, y + dy))  # Get the piece diagonally
                if target != " " and target.color != self.color:  # If there's an enemy piece, capture
                    moves.append((x + direction, y + dy))
                # En Passant capture
                if en_passant_target == (x + direction, y + dy):  # Special rule: capture via en passant
                    moves.append((x + direction, y + dy))

        return moves  # Return the list of valid moves
    def __repr__(self):
        return self.color[0].upper() + 'P' 

# Class for Rook Piece
class Rook(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.value = 500
        self.bonus = [
            [0,  0,  0,  5,  5,  0,  0,  0],
            [-5,  0,  0,  0,  0,  0,  0, -5],
            [-5,  0,  0,  0,  0,  0,  0, -5],
            [-5,  0,  0,  0,  0,  0,  0, -5],
            [-5,  0,  0,  0,  0,  0,  0, -5],
            [-5,  0,  0,  0,  0,  0,  0, -5],
            [5, 10, 10, 10, 10, 10, 10,  5],
            [0,  0,  0,  0,  0,  0,  0, 0]]

    def valid_moves(self, board, pos, en_passant_target=None):
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # Rook can move in four directions (up, down, left, right)
        return self._generate_sliding_moves(board, pos, directions)  # Generate all valid moves for rook

    # Helper method for sliding pieces (rook and bishop)
    def _generate_sliding_moves(self, board, pos, directions):
        moves = []  # List to store valid moves
        x, y = pos  # Current position of the rook
        for dx, dy in directions:  # Iterate over each direction
            nx, ny = x + dx, y + dy  # Move in the direction
            while 0 <= nx < 8 and 0 <= ny < 8:  # While the new position is within the board
                target = board.get_piece((nx, ny))  # Get the piece at the new position
                if target == ' ':  # If the square is empty, add it as a valid move
                    moves.append((nx, ny))
                elif target.color != self.color:  # If it's an opponent's piece, capture and stop moving further
                    moves.append((nx, ny))
                    break
                else:
                    break  # Stop moving if it's our own piece
                nx, ny = nx + dx, ny + dy  # Move further in the same direction
        return moves  # Return the list of valid moves
    
    def __repr__(self):
        return self.color[0].upper() + 'R'

# Class for Knight Piece
class Knight(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.value = 320
        self.bonus = [[-50, -40, -30, -30, -30, -30, -40, -50],
                      [-40, -20, 0, 0, 0, 0, -20, -40],
                      [-30, 0, 10, 15, 15, 10, 0, -30],
                      [-30, 5, 15, 20, 20, 15, 5, -30],
                      [-30, 0, 15, 20, 20, 15, 0, -30],
                      [-30, 5, 10, 15, 15, 10, 5, -30],
                      [-40, -20, 0, 5, 5, 0, -20, -40],
                      [-50, -40, -30, -30, -30, -30, -40, -50]]

    def valid_moves(self, board, pos, en_passant_target=None):

        directions = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]  # Knight's L-shaped moves
        x, y = pos  # Current position of the knight
        valid_moves = []  # List to store valid moves
        for dx, dy in directions:  # Iterate over each possible L-shaped move
            nx, ny = x + dx, y + dy  # Calculate the new position
            if 0 <= nx < 8 and 0 <= ny < 8:  # Ensure the new position is within the board
                target = board.get_piece((nx, ny))  # Get the piece at the new position
                if target == " " or target.color != self.color:  # Move if it's empty or an opponent's piece

                    valid_moves.append((nx, ny))
        return valid_moves  # Return the list of valid moves
    
    def __repr__(self):
        return self.color[0].upper() + 'N'

# Class for Bishop Piece
class Bishop(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.value = 330
        self.bonus = [
            [-20, -10, -10, -10, -10, -10, -10, -20],
            [-10, 0, 0, 0, 0, 0, 0, -10],
            [-10, 0, 5, 10, 10, 5, 0, -10],
            [-10, 5, 5, 10, 10, 5, 5, -10],
            [-10, 0, 10, 10, 10, 10, 0, -10],
            [-10, 10, 10, 10, 10, 10, 10, -10],
            [-10, 5, 0, 0, 0, 0, 5, -10],
            [-20, -10, -10, -10, -10, -10, -10, -20]
    ]

    def valid_moves(self, board, pos, en_passant_target=None):
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]  # Bishop moves diagonally in four directions
        return self._generate_sliding_moves(board, pos, directions)  # Generate all valid moves for bishop

    # Helper method for sliding pieces (same as in Rook)
    def _generate_sliding_moves(self, board, pos, directions):
        moves = []  # List to store valid moves
        x, y = pos  # Current position of the bishop
        for dx, dy in directions:  # Iterate over each diagonal direction
            nx, ny = x + dx, y + dy  # Move in the direction
            while 0 <= nx < 8 and 0 <= ny < 8:  # While the new position is within the board
                target = board.get_piece((nx, ny))  # Get the piece at the new position
                if target == ' ':  # If the square is empty, add it as a valid move
                    moves.append((nx, ny))
                elif target.color != self.color:  # If it's an opponent's piece, capture and stop moving further
                    moves.append((nx, ny))
                    break
                else:
                    break  # Stop moving if it's our own piece
                nx, ny = nx + dx, ny + dy  # Move further in the same direction
        return moves  # Return the list of valid moves
    
    def __repr__(self):
        return self.color[0].upper() + 'B'

# Class for Queen Piece
class Queen(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.value = 900
        self.bonus = [
                      [-20, -10, -10, -5, -5, -10, -10, -20],
                      [-10, 0, 0, 0, 0, 0, 0, -10],
                      [-10, 0, 5, 5, 5, 5, 0, -10],
                      [-5, 0, 5, 5, 5, 5, 0, -5],
                      [0, 0, 5, 5, 5, 5, 0, -5],
                      [-10, 5, 5, 5, 5, 5, 0, -10],
                      [-10, 0, 5, 0, 0, 0, 0, -10],
                      [-20, -10, -10, -5, -5, -10, -10, -20]
            ]
    def valid_moves(self, board, pos, en_passant_target=None):
        # Combine Rook and Bishop movement logic since Queen moves like both
        return Rook(self.color).valid_moves(board, pos) + Bishop(self.color).valid_moves(board, pos)
    
    def __repr__(self):
        return self.color[0].upper() + 'Q'

# Class for King Piece
class King(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.value = 20000
        self.bonus = [[-30, -40, -40, -50, -50, -40, -40, -30],
                      [-30, -40, -40, -50, -50, -40, -40, -30],
                      [-30, -40, -40, -50, -50, -40, -40, -30],
                      [-30, -40, -40, -50, -50, -40, -40, -30],
                      [-20, -30, -30, -40, -40, -30, -30, -20],
                      [-10, -20, -20, -20, -20, -20, -20, -10],
                      [20, 20, 0, 0, 0, 0, 20, 20],
                      [20, 30, 10, 0, 0, 10, 30, 20]]

    def valid_moves(self, board, pos, en_passant_target=None):
        directions = [
            (1, 0), (-1, 0), (0, 1), (0, -1),  # King's movement: one square in any horizontal or vertical direction
            (1, 1), (1, -1), (-1, 1), (-1, -1)  # Also one square diagonally
        ]
        moves = []  # List to store valid moves
        x, y = pos  # Current position of the king
        for dx, dy in directions:  # Iterate over each direction
            nx, ny = x + dx, y + dy  # Calculate the new position
            if 0 <= nx < 8 and 0 <= ny < 8:  # Ensure the new position is within the board
                target = board.get_piece((nx, ny))  # Get the piece at the new position
                if target == ' ' or target.color != self.color:  # Move if it's empty or an opponent's piece
                    moves.append((nx, ny))
        
        if not self.has_moved:
            # Castling moves
            if board.castling_rights[self.color]['kingside']:
                if self._can_castle_kingside(board, pos):
                    moves.append((x, y + 2))
            if board.castling_rights[self.color]['queenside']:
                if self._can_castle_queenside(board, pos):
                    moves.append((x, y - 2))
                    
        return moves  # Return the list of valid moves

    def _can_castle_kingside(self, board, pos):
        x, y = pos
        # Ensure the squares between king and rook are empty and not under attack
        return (
            board.get_piece((x, y + 1)) == ' ' and
            board.get_piece((x, y + 2)) == ' ' and
            not board.is_in_check(self.color) and
            not board.is_under_attack((x, y + 1), self.color) and
            not board.is_under_attack((x, y + 2), self.color) and
            isinstance(board.get_piece((x, 7)), Rook) and
            not board.get_piece((x, 7)).has_moved
        )

    def _can_castle_queenside(self, board, pos):
        x, y = pos
        # Ensure the squares between king and rook are empty and not under attack
        return (
            board.get_piece((x, y - 1)) == ' ' and
            board.get_piece((x, y - 2)) == ' ' and
            board.get_piece((x, y - 3)) == ' ' and
            not board.is_in_check(self.color) and
            not board.is_under_attack((x, y - 1), self.color) and
            not board.is_under_attack((x, y - 2), self.color) and
            isinstance(board.get_piece((x, 0)), Rook) and
            not board.get_piece((x, 0)).has_moved
        )
    
    def __repr__(self):
        return self.color[0].upper() + 'K'

# Chess Board Setup
class ChessBoard:
    def __init__(self):
        self.board = self.initialize_board()
        self.turn = WHITE #game starts with the player controlling the white pieces
        self.en_passant_target = None #track the target square for an en passant capture
        self.castling_rights = {
            WHITE: {'kingside': True, 'queenside': True},
            BLACK: {'kingside': True, 'queenside': True}
        } #Both players start with the ability to castle on both the kingside and queenside.


    def clone(self):
        ret = ChessBoard()
        ret.board = copy.deepcopy(self.board)
        ret.turn = self.turn
        ret.en_passant_target = self.en_passant_target
        ret.castling_rights = copy.deepcopy(self.castling_rights)

        return ret


    @classmethod
    def from_fen(cls, fen_str):
        new = cls()
        new.board = [
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        ]
        ranks = fen_str.split("/")
        for i, rank in enumerate(ranks):
            file = 0
            for piece in rank:
                match piece.lower():
                    case 'p':
                        new.board[i][file] = Pawn(WHITE if piece.isupper() else BLACK)
                    case 'n':
                        new.board[i][file] = Knight(WHITE if piece.isupper() else BLACK)
                    case 'b':
                        new.board[i][file] = Bishop(WHITE if piece.isupper() else BLACK)
                    case 'r':
                        new.board[i][file] = Rook(WHITE if piece.isupper() else BLACK)
                    case 'q':
                        new.board[i][file] = Queen(WHITE if piece.isupper() else BLACK)
                    case 'k':
                        new.board[i][file] = King(WHITE if piece.isupper() else BLACK)
                    case n if n.isnumeric():
                        file += int(n) - 1
                file += 1

        return new

    def get_fen(self):
        fen_str = ""
        for rank in self.board:
            space_count = 0
            for file in rank:
                if file != ' ' and space_count > 0:
                    fen_str += str(space_count)
                    space_count = 0
                    
                match file:
                    case file if isinstance(file, Pawn):
                        fen_str += "p" if file.color == BLACK else "P"
                    case file if isinstance(file, Rook):
                        fen_str += "r" if file.color == BLACK else "R"
                    case file if isinstance(file, Knight):
                        fen_str += "n" if file.color == BLACK else "N"
                    case file if isinstance(file, Bishop):
                        fen_str += "b" if file.color == BLACK else "B"
                    case file if isinstance(file, King):
                        fen_str += "k" if file.color == BLACK else "K"
                    case file if isinstance(file, Queen):
                        fen_str += "q" if file.color == BLACK else "Q"
                    case ' ':
                        space_count += 1

            fen_str += (str(space_count) if space_count > 0 else '') + "/"
        return fen_str[:-1]

    @staticmethod
    def file_rank_to_coords(file, rank):
        # File is the letter and rank is the number

        # Returns (rank, file)
        return (8 - int(rank), ord(file) - ord("A"))

    #creates the starting layout of the chessboard.Each list contains the pieces in their starting positions, with the black pieces at the top and white pieces at the bottom. Empty squares are represented by spaces 
    def initialize_board(self):
        return [
            [Rook(BLACK), Knight(BLACK), Bishop(BLACK), Queen(BLACK), King(BLACK), Bishop(BLACK), Knight(BLACK), Rook(BLACK)],
            [Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK)],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE)],
            [Rook(WHITE), Knight(WHITE), Bishop(WHITE), Queen(WHITE), King(WHITE), Bishop(WHITE), Knight(WHITE), Rook(WHITE)]
        ] 

    def print_board(self):
        piece_symbols = {
            Rook: 'R', Knight: 'N', Bishop: 'B', Queen: 'Q', King: 'K', Pawn: 'P'
        } # maps chess piece classes to their standard chess symbols.


        print("A  B  C  D  E  F  G  H\n")
        for i, row in enumerate(self.board):
            print(' '.join([f"{piece.color[0].upper()}{piece_symbols[type(piece)]}" if isinstance(piece, Piece) else '  ' for piece in row]), " ", 8 - i)
        print()

    # takes a position as input and returns the piece located at that position on the board.
    def get_piece(self, pos):
        x, y = pos
        piece = self.board[x][y]
        return piece if piece != ' ' else " "

    def get_valid_moves(self, pos):
        piece = self.get_piece(pos)
        if piece == " ":
            return []
        return piece.valid_moves(self, pos, self.en_passant_target)

    def move_piece(self, start, end):
        """Move the piece and handle special cases like castling."""
        sx, sy = start
        ex, ey = end
        piece = self.get_piece(start)
        
        # Castling move
        if isinstance(piece, King) and abs(ey - sy) == 2:
            if ey > sy:  # Kingside castling
                self.board[sx][sy + 1] = self.board[sx][7]  # Move the rook
                self.board[sx][7] = ' '
            else:  # Queenside castling
                self.board[sx][sy - 1] = self.board[sx][0]  # Move the rook
                self.board[sx][0] = ' '

        self.board[ex][ey] = piece
        self.board[sx][sy] = ' '

        if piece != ' ':
            piece.has_moved = True

    def is_valid_move(self, start, end):
        piece = self.get_piece(start)
        if not piece:
            print("No piece at start position.")
            return False
        if piece.color != self.turn:
            print("Piece belongs to the opponent.")
            return False
        valid_moves = piece.valid_moves(self, start, self.en_passant_target)
        if end not in valid_moves:
            print("End position is not a valid move.")
            return False
        return True
        
    def is_in_check(self, color):
        # Simplified check detection logic
        king_pos = None
        for x in range(8):
            for y in range(8):
                if isinstance(self.get_piece((x, y)), King) and self.get_piece((x, y)).color == color:
                    king_pos = (x, y)
                    break
        for x in range(8):
            for y in range(8):
                target_piece = self.get_piece((x, y))
                if target_piece != ' ' and target_piece.color != color:
                    if king_pos in target_piece.valid_moves(self, (x, y)):
                        return True
        return False

    def is_checkmate(self):
        for x in range(8):
            for y in range(8):
                piece = self.get_piece((x, y))
                if piece != ' ' and piece.color == self.turn:
                    for move in piece.valid_moves(self, (x, y)):
                        start = (x, y)
                        end = move
                        captured_piece = self.get_piece(end)  # Save the captured piece
                        
                        # Manually update the board state
                        self.board[end[0]][end[1]] = piece
                        self.board[start[0]][start[1]] = ' '
                        
                        if not self.is_in_check(self.turn):
                            # Undo the move
                            self.board[start[0]][start[1]] = piece
                            self.board[end[0]][end[1]] = captured_piece
                            return False
                        
                        # Undo the move
                        self.board[start[0]][start[1]] = piece
                        self.board[end[0]][end[1]] = captured_piece
        return True
    
    def is_under_attack(self, pos, color):
        """Check if a square is under attack by any opponent's piece."""
        for x in range(8):
            for y in range(8):
                piece = self.get_piece((x, y))
                if piece != ' ' and piece.color != color:
                    if pos in piece.valid_moves(self, (x, y)):
                        return True
        return False
    
    def find_king(self, color):
        """Find the position of the king of the given color."""
        for x in range(8):
            for y in range(8):
                piece = self.get_piece((x, y))
                if isinstance(piece, King) and piece.color == color:
                    return (x, y)
        return None




# Game Loop without AI
def play_game():
    board = ChessBoard()
    pawn = Pawn(WHITE)
    print(pawn)

    while True:
        board.print_board()

        # Player move (simple manual input for demonstration)
        start = tuple(input(f"{board.turn.capitalize()}'s turn. Enter start position (FileRank): ").upper())
        start = ChessBoard.file_rank_to_coords(start[0], start[1])
        end = tuple(input("Enter the end position (FileRank): ").upper())
        end = ChessBoard.file_rank_to_coords(end[0], end[1])
        

        if board.is_valid_move(start, end):
            board.move_piece(start, end)

            # Switch turns
            board.turn = BLACK if board.turn == WHITE else WHITE
            
            # Check for checkmate

            if board.is_in_check(board.turn):
                if board.check_checkmate():
                    print(f"{'Black' if board.turn == WHITE else 'White'} wins!")
                    break
                else:
                    print("check!!")

        else:
            print("Invalid move. Try again.")

# Run the game
if __name__ == "__main__":
    play_game()
