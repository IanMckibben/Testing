import piece

class ChessBoard:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self._initialize_pieces()

    def _initialize_pieces(self):
        # Initialize pawns
        for col in range(8):
            self.board[1][col] = piece.Pawn('white')
            self.board[6][col] = piece.Pawn('black')

        # Initialize other pieces
        piece_order = [piece.Rook, piece.Knight, piece.Bishop, piece.Queen, piece.King, piece.Bishop, piece.Knight, piece.Rook]
        for col in range(8):
            self.board[0][col] = piece_order[col]('white')
            self.board[7][col] = piece_order[col]('black')

    def __str__(self):
        result = "  a b c d e f g h\n"
        for row in range(7, -1, -1):
            result += f"{row + 1} "
            for col in range(8):
                piece = self.board[row][col]
                if piece is None:
                    result += ". "
                else:
                    result += f"{piece} "
            result += f"{row + 1}\n"
        result += "  a b c d e f g h"
        return result

    def is_valid_move(self, move, color='white'):
        if len(move) != 4:
            return False
        
        from_col, from_row = ord(move[0]) - ord('a'), int(move[1]) - 1
        to_col, to_row = ord(move[2]) - ord('a'), int(move[3]) - 1
        
        if not (0 <= from_col < 8 and 0 <= from_row < 8 and 0 <= to_col < 8 and 0 <= to_row < 8):
            return False
        
        moving_piece = self.board[from_row][from_col]
        if moving_piece is None or moving_piece.color != color:
            return False
        
        # Check if the destination is empty or contains an opponent's piece
        dest_piece = self.board[to_row][to_col]
        if dest_piece and dest_piece.color == color:
            return False
        
        # Check piece-specific movement rules
        if isinstance(moving_piece, piece.Pawn):
            return self._is_valid_pawn_move(from_row, from_col, to_row, to_col, color)
        elif isinstance(moving_piece, piece.Rook):
            return self._is_valid_rook_move(from_row, from_col, to_row, to_col)
        elif isinstance(moving_piece, piece.Knight):
            return self._is_valid_knight_move(from_row, from_col, to_row, to_col)
        elif isinstance(moving_piece, piece.Bishop):
            return self._is_valid_bishop_move(from_row, from_col, to_row, to_col)
        elif isinstance(moving_piece, piece.Queen):
            return self._is_valid_queen_move(from_row, from_col, to_row, to_col)
        elif isinstance(moving_piece, piece.King):
            return self._is_valid_king_move(from_row, from_col, to_row, to_col)
        
        return False

    def _is_valid_pawn_move(self, from_row, from_col, to_row, to_col, color):
        direction = 1 if color == 'white' else -1
        if from_col == to_col:  # Moving forward
            if to_row == from_row + direction and self.board[to_row][to_col] is None:
                return True
            if (from_row == 1 and color == 'white' or from_row == 6 and color == 'black') and \
               to_row == from_row + 2 * direction and \
               self.board[from_row + direction][from_col] is None and \
               self.board[to_row][to_col] is None:
                return True
        elif abs(to_col - from_col) == 1 and to_row == from_row + direction:  # Capturing diagonally
            return self.board[to_row][to_col] is not None and self.board[to_row][to_col].color != color
        return False

    def _is_valid_rook_move(self, from_row, from_col, to_row, to_col):
        if from_row != to_row and from_col != to_col:
            return False
        return self._is_path_clear(from_row, from_col, to_row, to_col)

    def _is_valid_knight_move(self, from_row, from_col, to_row, to_col):
        row_diff = abs(to_row - from_row)
        col_diff = abs(to_col - from_col)
        return (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2)

    def _is_valid_bishop_move(self, from_row, from_col, to_row, to_col):
        if abs(to_row - from_row) != abs(to_col - from_col):
            return False
        return self._is_path_clear(from_row, from_col, to_row, to_col)

    def _is_valid_queen_move(self, from_row, from_col, to_row, to_col):
        if from_row == to_row or from_col == to_col or abs(to_row - from_row) == abs(to_col - from_col):
            return self._is_path_clear(from_row, from_col, to_row, to_col)
        return False

    def _is_valid_king_move(self, from_row, from_col, to_row, to_col):
        return abs(to_row - from_row) <= 1 and abs(to_col - from_col) <= 1

    def _is_path_clear(self, from_row, from_col, to_row, to_col):
        row_step = 1 if to_row > from_row else -1 if to_row < from_row else 0
        col_step = 1 if to_col > from_col else -1 if to_col < from_col else 0
        row, col = from_row + row_step, from_col + col_step
        while (row, col) != (to_row, to_col):
            if self.board[row][col] is not None:
                return False
            row += row_step
            col += col_step
        return True

    def make_move(self, move):
        from_col, from_row = ord(move[0]) - ord('a'), int(move[1]) - 1
        to_col, to_row = ord(move[2]) - ord('a'), int(move[3]) - 1
        
        piece = self.board[from_row][from_col]
        self.board[to_row][to_col] = piece
        self.board[from_row][from_col] = None

    def is_game_over(self):
        # Simplified game over check: game ends if either king is captured
        white_king = any(isinstance(p, piece.King) and p.color == 'white' for row in self.board for p in row if p)
        black_king = any(isinstance(p, piece.King) and p.color == 'black' for row in self.board for p in row if p)
        return not (white_king and black_king)

    def get_result(self):
        if not self.is_game_over():
            return "Game in progress"
        white_king = any(isinstance(p, piece.King) and p.color == 'white' for row in self.board for p in row if p)
        if white_king:
            return "White wins"
        else:
            return "Black wins"