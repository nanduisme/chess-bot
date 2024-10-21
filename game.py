# Constants
WHITE, BLACK = 'white', 'black'

# Chess Pieces Classes
class Piece:
    def __init__(self, color):
        self.color = color
        self.has_moved = False  # For castling

    def valid_moves(self, pos):
        pass  # To be implemented in subclasses

class Pawn(Piece):
    def valid_moves(self, board, pos, en_passant_target=None):
        moves = []
        x, y = pos
        direction = -1 if self.color == WHITE else 1

        # Move forward
        if 0 <= x + direction < 8 and board.get_piece((x + direction, y)) == ' ':
            moves.append((x + direction, y))
            # Two-square move from start
            if not self.has_moved and 0 <= x + 2 * direction < 8 and board.get_piece((x + 2 * direction, y)) == ' ':
                moves.append((x + 2 * direction, y))

        # Captures
        for dy in [-1, 1]:
            if 0 <= y + dy < 8:
                target = board.get_piece((x + direction, y + dy))
                if target != " " and target.color != self.color:
                    moves.append((x + direction, y + dy))
                # En Passant capture
                if en_passant_target == (x + direction, y + dy):
                    moves.append((x + direction, y + dy))

        return moves

class Rook(Piece):
    def valid_moves(self, board, pos, en_passant_target=None):
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        return self._generate_sliding_moves(board, pos, directions)

    def _generate_sliding_moves(self, board, pos, directions):
        moves = []
        x, y = pos
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            while 0 <= nx < 8 and 0 <= ny < 8:
                if 0 <= nx < 8 and 0 <= ny < 8:
                    target = board.get_piece((nx, ny))
                    if target == ' ':
                        moves.append((nx, ny))
                    elif target.color != self.color:
                        moves.append((nx, ny))
                        break
                    else:
                        break
                nx, ny = nx + dx, ny + dy
        return moves

class Knight(Piece):
    def valid_moves(self, board, pos, en_passant_target=None):
        directions = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
        x, y = pos
        valid_moves = []
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 8 and 0 <= ny < 8:
                target = board.get_piece((nx, ny))
                if target == " " or target.color != self.color:
                    valid_moves.append((nx, ny))
        return valid_moves

class Bishop(Piece):
    def valid_moves(self, board, pos, en_passant_target=None):
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        return self._generate_sliding_moves(board, pos, directions)

    def _generate_sliding_moves(self, board, pos, directions):
        moves = []
        x, y = pos
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            while 0 <= nx < 8 and 0 <= ny < 8:
                target = board.get_piece((nx, ny))
                if target == ' ':
                    moves.append((nx, ny))
                elif target.color != self.color:
                    moves.append((nx, ny))
                    break
                else:
                    break
                nx, ny = nx + dx, ny + dy
        return moves

class Queen(Piece):
    def valid_moves(self, board, pos, en_passant_target=None):
        return Rook(self.color).valid_moves(board, pos) + Bishop(self.color).valid_moves(board, pos)

class King(Piece):
    def valid_moves(self, board, pos, en_passant_target=None):
        directions = [
            (1, 0), (-1, 0), (0, 1), (0, -1),  # Horizontal and vertical moves
            (1, 1), (1, -1), (-1, 1), (-1, -1)  # Diagonal moves
        ]
        moves = []
        x, y = pos
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 8 and 0 <= ny < 8:
                target = board.get_piece((nx, ny))
                if target == ' ' or target.color != self.color:
                    moves.append((nx, ny))
        return moves

# Chess Board Setup
class ChessBoard:
    def __init__(self):
        self.board = self.initialize_board()
        self.turn = WHITE
        self.en_passant_target = None
        self.castling_rights = {
            WHITE: {'kingside': True, 'queenside': True},
            BLACK: {'kingside': True, 'queenside': True}
        }

    @staticmethod
    def file_rank_to_coords(file, rank):
        # File is the letter and rank is the number

        # Returns (rank, file)
        return (int(rank) - 1, ord(file) - ord("A"))

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
        }

        print("A  B  C  D  E  F  G  H\n")
        for i, row in enumerate(self.board):
            print(' '.join([f"{piece.color[0].upper()}{piece_symbols[type(piece)]}" if isinstance(piece, Piece) else '  ' for piece in row]), " ", i + 1)
        print()

    def get_piece(self, pos):
        x, y = pos
        piece = self.board[x][y]
        return piece if piece != ' ' else " "

    def move_piece(self, start, end):
        sx, sy = start
        ex, ey = end
        self.board[ex][ey] = self.board[sx][sy]
        self.board[sx][sy] = ' '
        piece = self.get_piece(end)
        piece.has_moved = True  # Track if the piece has moved

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

    def check_checkmate(self):
        for x in range(8):
            for y in range(8):
                piece = self.get_piece((x, y))
                if piece != ' ' and piece.color == self.turn:
                    for move in piece.valid_moves(self, (x, y)):
                        start = (x, y)
                        end = move
                        self.move_piece(start, end)
                        if not self.is_in_check(self.turn):
                            self.move_piece(end, start)  # Undo move
                            return False
                        self.move_piece(end, start)  # Undo move
        return True


# Tree for Move History
class TreeNode:
    def __init__(self, board_state, move=None, parent=None):
        self.board_state = board_state  # Current state of the board
        self.move = move  # Move that led to this state
        self.children = []  # Subsequent game states (valid moves)
        self.parent = parent  # Previous state for backtracking

    def add_child(self, child_node):
        # Add a child node representing a subsequent game state
        self.children.append(child_node)

    def get_children(self):
         # Return the list of child nodes
        return self.children

    def get_parent(self):
        # Return the parent node representing the previous game state
        return self.parent

"""
ChessGameTree allows for tracking the progression of a chess game, 
maintaining a history of moves and board states in a tree structure. 
This can be useful for features like undoing moves, analyzing game history, 
or exploring different move sequences.
"""
class ChessGameTree:
    def __init__(self, initial_board):
         # Initialize the tree with the initial board state
        self.root = TreeNode(initial_board)  # Initial game state
         # Set the current node to the root node
        self.current_node = self.root

    def make_move(self, new_board_state, move):
         # Create a new node for the new board state and move
        new_node = TreeNode(new_board_state, move, self.current_node)
         # Add the new node as a child of the current node
        self.current_node.add_child(new_node)
         # Update the current node to the new node
        self.current_node = new_node

    def undo_move(self):
        if self.current_node.get_parent():
            self.current_node = self.current_node.get_parent()

"""
Chess Graph for Move Validation
This class represents a graph structure where each node is a square on the chessboard.
Edges between nodes represent valid moves from one square to another.
"""
class ChessGraph:
    def __init__(self):
         # Initialize the graph as an empty dictionary
        self.graph = {}

    def add_node(self, square):
         # Add a node to the graph if it doesn't already exist
        if square not in self.graph:
            self.graph[square] = []

    def add_edge(self, from_square, to_square):
         # Add an edge from one square to another, representing a valid move
        if from_square in self.graph:
            self.graph[from_square].append(to_square)

    def get_neighbors(self, square):
        # Get all squares that can be reached from the given square
        return self.graph.get(square, [])

"""
ChessBoardGraph builds on ChessGraph by adding chess-specific methods for initializing the board and generating moves.
"""
class ChessBoardGraph:
    def __init__(self):
        self.graph = ChessGraph()
        self.initialize_graph()

    def initialize_graph(self):
         # Initialize the graph with all squares on the chessboard
        for x in range(8):
            for y in range(8):
                self.graph.add_node((x, y))  # Add each square

    def generate_moves(self, pos):
        # Generate valid moves from the graph
        return self.graph.get_neighbors(pos)

    def move_piece(self, start, end):
        # Ensure there is an edge (valid move) between start and end
        if end in self.graph.get_neighbors(start):
            return True
        return False

# Heap for Move Prioritization
class CustomHeap:
    def __init__(self):
        self.heap = []

    def insert(self, priority, move):
        self.heap.append((priority, move))
        self._heapify_up(len(self.heap) - 1)

    def _heapify_up(self, index):
        while index > 0:
            parent = (index - 1) // 2
            if self.heap[index][0] > self.heap[parent][0]:
                self.heap[index], self.heap[parent] = self.heap[parent], self.heap[index]
                index = parent
            else:
                break

    def extract_max(self):
        if len(self.heap) > 1:
            self._swap(0, len(self.heap) - 1)
            max_value = self.heap.pop()
            self._heapify_down(0)
        elif len(self.heap) == 1:
            max_value = self.heap.pop()
        else:
            return None
        return max_value[1]

    def _heapify_down(self, index):
        last_index = len(self.heap) - 1
        while index <= last_index:
            left_child = 2 * index + 1
            right_child = 2 * index + 2
            largest = index

            if left_child <= last_index and self.heap[left_child][0] > self.heap[largest][0]:
                largest = left_child
            if right_child <= last_index and self.heap[right_child][0] > self.heap[largest][0]:
                largest = right_child

            if largest != index:
                self._swap(index, largest)
                index = largest
            else:
                break

    def _swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

class ChessMoveHeap:
    def __init__(self):
        self.move_heap = CustomHeap()

    def add_move(self, move, priority):
        self.move_heap.insert(priority, move)

    def get_best_move(self):
        return self.move_heap.extract_max()

    def generate_priority_moves(self, moves):
        for move in moves:
            priority = self.evaluate_move(move)
            self.add_move(move, priority)

    def evaluate_move(self):
        return 1  # Placeholder: actual evaluation logic

# Directed Acyclic Graph (DAG) for Transposition Table (Move History Tracking)
class ChessDAG:
    def __init__(self):
        self.nodes = {}

    def add_node(self, board_hash):
        if board_hash not in self.nodes:
            self.nodes[board_hash] = []

    def add_edge(self, from_board, to_board):
        if from_board in self.nodes:
            self.nodes[from_board].append(to_board)

    def has_seen(self, board_hash):
        return board_hash in self.nodes

    def get_transitions(self, board_hash):
        return self.nodes.get(board_hash, [])

class ChessTranspositionDAG:
    def __init__(self):
        self.dag = ChessDAG()

    def hash_board(self, board):
        return hash(str(board))  # Simple board hashing based on its string representation

    def store_position(self, board):
        board_hash = self.hash_board(board)
        self.dag.add_node(board_hash)

    def check_repetition(self, board):
        board_hash = self.hash_board(board)
        return self.dag.has_seen(board_hash)

    def add_transition(self, from_board, to_board):
        from_hash = self.hash_board(from_board)
        to_hash = self.hash_board(to_board)
        self.dag.add_edge(from_hash, to_hash)

# Game Loop without AI
def play_game():
    board = ChessBoard()
    game_tree = ChessGameTree(initial_board=board.board)
    transposition_dag = ChessTranspositionDAG()
    # board_graph = ChessBoardGraph()
    # move_heap = ChessMoveHeap()

    while True:
        board.print_board()

        # Player move (simple manual input for demonstration)
        start = tuple(input(f"{board.turn.capitalize()}'s turn. Enter start position (FileRank): ").upper())
        start = ChessBoard.file_rank_to_coords(start[0], start[1])
        print(start)
        end = tuple(input("Enter the end position (FileRank): ").upper())
        end = ChessBoard.file_rank_to_coords(end[0], end[1])
        print(end)

        if board.is_valid_move(start, end):
            board.move_piece(start, end)
            transposition_dag.store_position(board.board)
            game_tree.make_move(board.board, (start, end))
            # Switch turns
            board.turn = BLACK if board.turn == WHITE else WHITE
            
            # Check for checkmate
            if board.check_checkmate():
                print(f"{'Black' if board.turn == WHITE else 'White'} wins!")
                break
        else:
            print("Invalid move. Try again.")

# Run the game
play_game()
