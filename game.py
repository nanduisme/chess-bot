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
        if 0 <= x + direction < 8 and board.get_piece((x + direction, y)) == ' ':
            moves.append((x + direction, y))  # Add the forward move
            # Two-square move from starting position
            if not self.has_moved and 0 <= x + 2 * direction < 8 and board.get_piece((x + 2 * direction, y)) == ' ':
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
        return moves  # Return the list of valid moves

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

    def clone(self):
        ret = ChessBoard()
        ret.board = self.board
        ret.turn = self.turn
        ret.en_passant_target = self.en_passant_target
        ret.castling_rights = self.castling_rights

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
            print(' '.join([f"{piece.color[0].upper()}{piece_symbols[type(piece)]}" if isinstance(piece, Piece) else '  ' for piece in row]), " ", 8 - i)
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

    def is_checkmate(self):
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

# Custom heap implementation to prioritize chess moves based on their evaluation
class CustomHeap:
    def __init__(self):
        self.heap = []  # Initialize an empty list to represent the heap

    # Method to insert a move with its priority into the heap
    def insert(self, priority, move):
        self.heap.append((priority, move))  # Add the move and its priority as a tuple
        self._heapify_up(len(self.heap) - 1)  # Ensure heap property by adjusting upwards

    # Internal method to maintain heap property by "bubbling up" the inserted element
    def _heapify_up(self, index):
        while index > 0:  # While the element is not at the root
            parent = (index - 1) // 2  # Get the parent index
            if self.heap[index][0] > self.heap[parent][0]:  # Compare priorities (max heap)
                # Swap with the parent if the current element has a higher priority
                self.heap[index], self.heap[parent] = self.heap[parent], self.heap[index]
                index = parent  # Move the index to the parent and repeat
            else:
                break  # Stop if the heap property is satisfied

    # Method to extract the highest priority move (the root of the heap)
    def extract_max(self):
        if len(self.heap) > 1:  # If there are multiple elements in the heap
            self._swap(0, len(self.heap) - 1)  # Swap the root with the last element
            max_value = self.heap.pop()  # Remove and store the last element (which was the root)
            self._heapify_down(0)  # Restore the heap property by adjusting downwards
        elif len(self.heap) == 1:  # If there's only one element
            max_value = self.heap.pop()  # Just pop the only element
        else:
            return None  # Return None if the heap is empty
        return max_value[1]  # Return the move (ignoring the priority)

    # Internal method to maintain heap property by "bubbling down" the root element
    def _heapify_down(self, index):
        last_index = len(self.heap) - 1  # Get the index of the last element
        while index <= last_index:  # While we haven't reached the end of the heap
            left_child = 2 * index + 1  # Left child index
            right_child = 2 * index + 2  # Right child index
            largest = index  # Assume the current element is the largest

            # Compare with the left child
            if left_child <= last_index and self.heap[left_child][0] > self.heap[largest][0]:
                largest = left_child  # Update largest if the left child has a higher priority

            # Compare with the right child
            if right_child <= last_index and self.heap[right_child][0] > self.heap[largest][0]:
                largest = right_child  # Update largest if the right child has a higher priority

            # If the largest is not the current element, swap and continue bubbling down
            if largest != index:
                self._swap(index, largest)
                index = largest
            else:
                break  # Stop if the heap property is satisfied

    # Helper method to swap two elements in the heap
    def _swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]  # Swap elements at indices i and j

# Wrapper class to manage chess moves using the heap
class ChessMoveHeap:
    def _init_(self):
        self.move_heap = CustomHeap()  # Create an instance of the custom heap to store moves

    # Method to add a move with its priority to the heap
    def add_move(self, move, priority):
        self.move_heap.insert(priority, move)  # Insert the move and its priority into the heap

    # Method to get the move with the highest priority
    def get_best_move(self):
        return self.move_heap.extract_max()  # Extract and return the highest priority move

    # Method to generate priority moves from a list of moves
    def generate_priority_moves(self, moves):
        for move in moves:  # Iterate through each move
            priority = self.evaluate_move(move)  # Evaluate the priority of the move
            self.add_move(move, priority)  # Add the move to the heap with its evaluated priority

    # Placeholder method for evaluating a move's priority (to be implemented)
    def evaluate_move(self):
        return 1  # Placeholder: actual move evaluation logic should be implemented here

# Directed Acyclic Graph (DAG) for Transposition Table (Move History Tracking)

# Class representing a Directed Acyclic Graph (DAG) where each node is a board state
class ChessDAG:
    def _init_(self):
        self.nodes = {}  # Initialize an empty dictionary to store nodes (board positions)

    # Method to add a node (board state) to the DAG
    def add_node(self, board_hash):
        if board_hash not in self.nodes:  # Check if the board position (hash) is already in the graph
            self.nodes[board_hash] = []  # If not, create an empty list of transitions for this node

    # Method to add an edge between two nodes (representing a transition between board states)
    def add_edge(self, from_board, to_board):
        if from_board in self.nodes:  # Check if the starting board state exists in the graph
            self.nodes[from_board].append(to_board)  # Add the transition to the list of edges (moves)

    # Method to check if a board state has been seen before (exists in the DAG)
    def has_seen(self, board_hash):
        return board_hash in self.nodes  # Return True if the board state is already in the graph

    # Method to retrieve transitions (next possible moves) from a given board state
    def get_transitions(self, board_hash):
        return self.nodes.get(board_hash, [])  # Return the list of transitions or an empty list if none exist

# Wrapper class to manage transposition tables using a DAG (tracking repeated board states)
class ChessTranspositionDAG:
    def _init_(self):
        self.dag = ChessDAG()  # Initialize an instance of the DAG for move history tracking

    # Method to hash the board state (to use as a unique identifier in the DAG)
    def hash_board(self, board):
        return hash(str(board))  # Convert the board to a string and hash it to get a unique identifier

    # Method to store the current board position in the DAG
    def store_position(self, board):
        board_hash = self.hash_board(board)  # Hash the board state to get its unique identifier
        self.dag.add_node(board_hash)  # Add the board state as a node in the DAG

    # Method to check if a board position has occurred before (for repetition detection)
    def check_repetition(self, board):
        board_hash = self.hash_board(board)  # Hash the board state
        return self.dag.has_seen(board_hash)  # Check if the hashed board state exists in the DAG

    # Method to add a transition (move) from one board position to another
    def add_transition(self, from_board, to_board):
        from_hash = self.hash_board(from_board)  # Hash the starting board state
        to_hash = self.hash_board(to_board)  # Hash the resulting board state
        self.dag.add_edge(from_hash, to_hash)  # Add an edge between the two board states in the DAG

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
        end = tuple(input("Enter the end position (FileRank): ").upper())
        end = ChessBoard.file_rank_to_coords(end[0], end[1])

        if board.is_valid_move(start, end):
            board.move_piece(start, end)
            # transposition_dag.store_position(board.board)
            game_tree.make_move(board.board, (start, end))
            # Switch turns
            board.turn = BLACK if board.turn == WHITE else WHITE
            
            # Check for checkmate
            if board.is_checkmate():
                print(f"{'Black' if board.turn == WHITE else 'White'} wins!")
                break
        else:
            print("Invalid move. Try again.")

# Run the game
if __name__ == "__main__":
    play_game()
