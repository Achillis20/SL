PLAYER, AI, EMPTY = 'X', 'O', ' ' 

# Initialize and print the board
def initialize_board(): 
    return [[EMPTY] * 3 for _ in range(3)] 

def print_board(board): 
    for row in board: 
        print('|'.join(row)) 
    print("-" * 5) 

# Check for winner and full board
def check_winner(board): 
    # Check rows
    for row in board: 
        if row[0] == row[1] == row[2] != EMPTY:
            return row[0]
    
    # Check columns
    for col in range(3): 
        if board[0][col] == board[1][col] == board[2][col] != EMPTY:
            return board[0][col]
    
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] != EMPTY:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != EMPTY:
        return board[0][2]
    
    return None 

def is_full(board): 
    return all(EMPTY not in row for row in board) 

# Alpha-Beta Pruning
def alpha_beta(board, alpha, beta, maximizing): 
    winner = check_winner(board)
    # Score based on the game outcome
    score = {'O': 10, 'X': -10, None: 0}[winner]
    
    if winner or is_full(board):  # If game is over, return score
        return score

    if maximizing:  # AI's turn (maximizing)
        value = -float('inf') 
        for i in range(3): 
            for j in range(3): 
                if board[i][j] == EMPTY: 
                    board[i][j] = AI
                    value = max(value, alpha_beta(board, alpha, beta, False))
                    board[i][j] = EMPTY
                    alpha = max(alpha, value)
                    if beta <= alpha:
                        return value  # Beta cut-off
        return value

    else:  # Player's turn (minimizing)
        value = float('inf') 
        for i in range(3): 
            for j in range(3): 
                if board[i][j] == EMPTY: 
                    board[i][j] = PLAYER
                    value = min(value, alpha_beta(board, alpha, beta, True))
                    board[i][j] = EMPTY
                    beta = min(beta, value)
                    if beta <= alpha:
                        return value  # Alpha cut-off
        return value

# AI finds the best move using Alpha-Beta Pruning
def find_best_move(board): 
    best_val, best_move = -float('inf'), (-1, -1) 
    for i in range(3): 
        for j in range(3): 
            if board[i][j] == EMPTY: 
                board[i][j] = AI
                move_val = alpha_beta(board, -float('inf'), float('inf'), False)
                board[i][j] = EMPTY
                if move_val > best_val:
                    best_val, best_move = move_val, (i, j)
    return best_move 

# Player's move input
def player_move(board): 
    while True: 
        try:
            row, col = map(int, input("Enter your move (row column): ").split())
            if board[row][col] == EMPTY: 
                board[row][col] = PLAYER 
                break
            else:
                print("Cell already occupied. Try again.")
        except (ValueError, IndexError):
            print("Invalid input. Please enter row and column as two numbers between 0 and 2.")

# Main game loop
def play_game(): 
    board = initialize_board() 
    print("Welcome to Tic-Tac-Toe!") 
    print_board(board) 

    while True: 
        # Player's move
        player_move(board) 
        print_board(board) 
        if check_winner(board) == PLAYER:
            print("Player wins!")
            break
        if is_full(board):
            print("It's a tie!")
            break

        # AI's move
        ai_move = find_best_move(board) 
        board[ai_move[0]][ai_move[1]] = AI 
        print("AI's Move:")
        print_board(board) 
        if check_winner(board) == AI:
            print("AI wins!")
            break
        if is_full(board):
            print("It's a tie!")
            break

# Menu to start or exit the game
def menu(): 
    while True: 
        choice = input("\n1. Play Tic-Tac-Toe\n2. Exit\nEnter your choice: ") 
        if choice == '1':
            play_game() 
        elif choice == '2':
            break 
        else:
            print("Invalid choice. Please try again.")

# Ensure the menu runs only when the script is executed directly
if __name__ == "__main__": 
    menu()
