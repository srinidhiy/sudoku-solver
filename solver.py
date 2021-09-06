#implements the backtracking method to solve the puzzle

def find(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return (i, j)  #row, column
    return None

def is_valid(board, input_val, pos):
    #check the row
    for i in range(len(board[0])):
        if board[pos[0]][i] == input_val and pos[1] != i:
            return False
    
    #check the column
    for i in range(len(board)):
        if board[i][pos[1]] == input_val and pos[0] != i:
            return False
    
    #check box
    row = pos[0] // 3
    col = pos[1] // 3

    for i in range(row*3, row*3 + 3):
        for j in range(col*3, col*3 + 3):
            if board[i][j] == input_val and (i,j) != pos:
                return False

    return True

def solve(board):
    #base case = solved board
    valid_spaces = find(board)
    if not valid_spaces:
        return True
    else:
        i, j = valid_spaces
    
    for k in range(1,10):
        #if a number CAN be placed in a spot, place it there --> check if it can be solved --> if not, reset value
        if is_valid(board, k, (i,j)):
            board[i][j] = k
            if solve(board):
                return True
            else:
                board[i][j] = 0
    
    return False
