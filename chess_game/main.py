import chess_board
import ai_strategy

def main():
    board = chess_board.ChessBoard()
    ai = ai_strategy.AIStrategy()

    print("Welcome to the Interactive Chess Game!")
    print("You are playing as White. Enter your moves in algebraic notation (e.g., 'e2e4').")

    while not board.is_game_over():
        print(board)
        
        # Player's turn
        while True:
            move = input("Enter your move: ")
            if board.is_valid_move(move):
                board.make_move(move)
                break
            else:
                print("Invalid move. Please try again.")
        
        if board.is_game_over():
            break
        
        # AI's turn
        ai_move = ai.get_best_move(board)
        print(f"AI's move: {ai_move}")
        board.make_move(ai_move)

    print(board)
    print("Game Over!")
    print(f"Result: {board.get_result()}")

if __name__ == "__main__":
    main()