import random

class AIStrategy:
    def __init__(self):
        pass

    def get_best_move(self, board):
        valid_moves = self._get_all_valid_moves(board)
        return random.choice(valid_moves) if valid_moves else None

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