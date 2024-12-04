import numpy as np
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level = logging.DEBUG)

class Sudoku1():
    def __init__(self, seed = None):
        self.seed = seed
        self.solution = self.create_sudoku()

    def get_solution(self):
        logger.debug(self.solution)
        return self.solution
    
    def get_problem(self, difficulty = 'easy'):
        #problem instance is iniated as a copy of the solution
        self.problem = self.solution.copy()

        logger.debug(f"problem initalized as:  \n {self.problem}")

        #potentially redundant assignment of problem shape seeing as sudoku will always be 9x9
        n = self.problem.shape[0]

        #create dicts for all diagonals (incl. primary and secondary)
        diag_list1 = [(i, "up") for i in range(-n + 1, n)]
        diag_list2 = [(i, "down") for i in range(-n + 1, n)]
        diag_list = diag_list1 + diag_list2

        #difficulty sought, easy was determined according to refrenced work
        if difficulty == 'easy':
            r_times = 20
        else:
            raise ValueError("Difficulty not recognized")

        #assigning x = 0 to ensure 20 iterations of placing 0s is carried out.
        x = 0
        while x < r_times:
            #Ensure there is a previous copy to go back to
            previous_step = self.problem.copy()
            choice = np.random.choice(len(diag_list))
            choice_offset, choice_direction = diag_list[choice]

            #logic for normal bottom left to upper right diagonals
            if choice_direction == 'up':
                chosen_diag = self.problem.diagonal(choice_offset)
                zero_count = np.count_nonzero(chosen_diag == 0)
                lanzo = len(chosen_diag)
                
                #ensure that diagonal is not over saturated
                if zero_count > x:
                    continue
                
                # ensure that diagonal is longer than 4 (redundant as we also want diagonals with less than four values to be targeted)
                if lanzo >= 4:
                    chosen_indices = np.random.choice(lanzo, 4, replace = False)
                    for idx in chosen_indices:
                        i = idx if choice_offset >= 0 else idx - choice_offset
                        j = idx + choice_offset if choice_offset >= 0 else idx
                        self.problem[i][j] == 0

                    #test if adjustments still keep the sudoku puzzle having one solution
                    if self.test_single_solution():
                        pass

                        x += 1

            #logic for reversed top left to bottom right diagonals
            elif choice_direction == 'down':
                chosen_diag = np.fliplr(self.problem).diagonal(choice_offset)
                zero_count = np.count_nonzero(chosen_diag == 0)
                lanzo = len(chosen_diag)

                #ensure that diagonal is not over saturated
                if zero_count > x:
                    continue
                
                # ensure that diagonal is longer than 4 (redundant as we also want diagonals with less than four values to be targeted)
                if lanzo >= 4:
                    chosen_indices = np.random.choice(lanzo, 4, replace=False)
                    for idx in chosen_indices:
                        i = idx if choice_offset >= 0 else idx - choice_offset
                        j = 8 - (idx + choice_offset if choice_offset >= 0 else idx)
                        self.problem[i, j] = 0
                

                    #test if adjustments still keep the sudoku puzzle having one solution
                    if self.test_single_solution():
                        pass

                        x += 1

        return self.problem



    def test_single_solution(self):
        pass




    def create_sudoku(self):
        '''Create a Sudoku grid using DFS and backtracking'''
        np.random.seed(self.seed)
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
        self.remove_pos(sudoku, psb)
        
        if self.dfs(sudoku, psb):
            return sudoku
        else:
            raise ValueError("Failed to generate a valid Sudoku grid.")

    def dfs(self, sudoku, psb):
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
            self.remove_pos(sudoku, psb)
            
            if self.dfs(sudoku, psb):
                return True  # Found a solution along this branch
            
            # Backtrack if this branch doesn't lead to a solution
            sudoku[x_cord, y_cord] = 0
            psb = old_psb.copy()  # Revert to previous state
        
        logger.debug("backtracking branch")
        return False  # No valid solution found along this branch

    def remove_pos(self, sudoku, psb):
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


    def rule1(self, sudoku) -> bool:
        '''Rule to ensure that each block contains unique numbers within 1-9'''
        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                block = sudoku[i:i+3, j:j+3].flatten()
                block = block[block != 0]  # Remove zeros
                if len(block) != len(set(block)):
                    return False
        return True

    def rule2(self, sudoku) -> bool:
        '''Rule to ensure that each row and column contains unique numbers within 1-9'''
        for i in range(9):
            row = sudoku[i]
            col = sudoku[:, i]
            row = row[row != 0]  # Remove zeros
            col = col[col != 0]  # Remove zeros
            if len(row) != len(set(row)) or len(col) != len(set(col)):
                return False
        return True

if __name__ == '__main__':
    test_sudoku = Sudoku1(1)
    solution = test_sudoku.create_sudoku()
    prol = test_sudoku.get_problem()
    print(prol)
