class Piece:
    ...
    
class Pos:
    @classmethod
    def from_pair(cls, rank, file) -> Pos:
        '''
        returns a Pos object where self.pos is a 6 bit number where the number is 0brrrfff
        '''

        return cls()

    def get_rank(self) -> int:
        return 0

    def get_file(self) -> int:
        return 0
    

class Board:
    '''
    Main class where the game takes place
    '''

    @classmethod
    def from_fen(cls, fen) -> Board:
        '''
        Returns a Board object that corresponds to the given fen 
        '''

        return cls()

    def get_piece(self, pos: Pos) -> Piece | None:
        '''
        Returns the piece at given position
        '''
        return None

    def get_plays(self, pos: Pos) -> list[Pos]:
        '''
        Returns a list of all legal plays given a position
        '''

        return []

    def get_fen(self) -> str:
        '''
        Returns the fen string of the current board
        '''

        return ""
