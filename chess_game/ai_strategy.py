import random
import piece

class AIStrategy:
    def __init__(self):
        self.piece_values = {
            piece.Pawn: 1,
            piece.Knight: 3,
            piece.Bishop: 3,
            piece.Rook: 5,
            piece.Queen: 9,
            piece.King: 100
        }

    def get_best_move(self, board):
        valid_moves = self._get_all_valid_moves(board)
        if not valid_moves:
            return None

        best_move = None
        best_score = float('-inf')

        for move in valid_moves:
            score = self._evaluate_move(board, move)
            if score > best_score:
                best_score = score
                best_move = move

        return best_move

    def _get_all_valid_moves(self, board):
        valid_moves = []
        for from_row in range(8):
            for from_col in range(8):
                piece = board.board[from_row][from_col]
                if piece and piece.color == 'black':
                    for to_row in range(8):
                        for to_col in range(8):
                            move = f"{chr(from_col + ord('a'))}{from_row + 1}{chr(to_col + ord('a'))}{to_row + 1}"
                            if board.is_valid_move(move, color='black'):
                                valid_moves.append(move)
        return valid_moves

    def _evaluate_move(self, board, move):
        from_col, from_row = ord(move[0]) - ord('a'), int(move[1]) - 1
        to_col, to_row = ord(move[2]) - ord('a'), int(move[3]) - 1

        moving_piece = board.board[from_row][from_col]
        captured_piece = board.board[to_row][to_col]

        score = self.piece_values[type(moving_piece)]

        # Evaluate capture
        if captured_piece:
            score += self.piece_values[type(captured_piece)]

        # Evaluate center control
        center_squares = [(3, 3), (3, 4), (4, 3), (4, 4)]
        if (to_row, to_col) in center_squares:
            score += 0.3

        # Penalize moving the king early in the game
        if isinstance(moving_piece, piece.King) and board.move_count < 10:
            score -= 1

        return score