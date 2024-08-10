import numpy as np

def create_sudoku():
    '''Create a Sudoku grid using DFS and backtracking'''
    sudoku = np.zeros((9, 9), dtype=int)

    # Seed 1-9 randomly across the grid
    indx = list(np.ndindex(sudoku.shape))
    choice = np.random.choice(len(indx), 9, replace=False)
    chosen_indices = [indx[i] for i in choice]
    numbo = np.random.choice(np.arange(1, 10), 9, replace=False)
    for i in range(9):
        x, y = chosen_indices[i]
        sudoku[x, y] = numbo[i]

    # Initialize the possibilities matrix
    psb = np.ones((9, 9, 9), dtype=bool)
    remove_pos(sudoku, psb)
    
    if dfs(sudoku, psb):
        return sudoku
    else:
        raise ValueError("Failed to generate a valid Sudoku grid.")

def dfs(sudoku, psb):
    '''Recursive DFS function to explore the solution space'''
    if np.all(sudoku != 0):
        return True  # All cells are filled, solution found
    
    # Find the cell with the fewest possibilities
    min_choices = 10
    min_cell = None
    
    for i in range(9):
        for j in range(9):
            if sudoku[i, j] == 0:
                choices = np.sum(psb[i, j])
                if choices < min_choices:
                    min_choices = choices
                    min_cell = (i, j)
    
    if min_cell is None or min_choices == 0:
        return False  # Dead-end
    
    x_cord, y_cord = min_cell
    possible_values = np.where(psb[x_cord, y_cord])[0] + 1
    
    # Branching: try each possible value in the selected cell
    for numbo in possible_values:
        sudoku[x_cord, y_cord] = numbo
        
        old_psb = psb.copy()  # Save the current state of possibilities
        remove_pos(sudoku, psb)
        
        if dfs(sudoku, psb):
            return True  # Found a solution along this branch
        
        # Backtrack if this branch doesn't lead to a solution
        sudoku[x_cord, y_cord] = 0
        psb = old_psb.copy()  # Revert to previous state
    
    print("backtracking branch")
    return False  # No valid solution found along this branch

def remove_pos(sudoku, psb):
    '''Update possible values for each cell according to the current Sudoku grid'''
    psb.fill(True)  # Reset possibilities
    for i in range(9):
        for j in range(9):
            if sudoku[i, j] != 0:
                num = sudoku[i, j]
                psb[i, :, num - 1] = False
                psb[:, j, num - 1] = False  # Remove from column

                # Block removal
                block_x = (i // 3) * 3
                block_y = (j // 3) * 3
                psb[block_x:block_x + 3, block_y:block_y + 3, num - 1] = False
                psb[i, j] = False  # The cell itself is no longer changeable


def rule1(sudoku) -> bool:
    '''Rule to ensure that each block contains unique numbers within 1-9'''
    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            block = sudoku[i:i+3, j:j+3].flatten()
            block = block[block != 0]  # Remove zeros
            if len(block) != len(set(block)):
                return False
    return True

def rule2(sudoku) -> bool:
    '''Rule to ensure that each row and column contains unique numbers within 1-9'''
    for i in range(9):
        row = sudoku[i]
        col = sudoku[:, i]
        row = row[row != 0]  # Remove zeros
        col = col[col != 0]  # Remove zeros
        if len(row) != len(set(row)) or len(col) != len(set(col)):
            return False
    return True

result = create_sudoku()
print(result)
