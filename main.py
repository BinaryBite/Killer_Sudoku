from tkinter import Tk, Canvas, Frame, BOTH
from sudokoid import Sudoku1

# Define constants
MARGIN = 20  # Margin around the grid
SIDE = 50    # Width of each cell
WIDTH = HEIGHT = MARGIN * 2 + SIDE * 9  # Overall dimensions of the board

class SudokuUI(Frame):
    def __init__(self, parent):
        self.parent = parent
        Frame.__init__(self, parent)

        self.row, self.col = 0, 0

        self.__initUI()

    def __initUI(self):
        self.parent.title("Sudokoid")
        self.pack(fill=BOTH, expand=1)
        self.canvas = Canvas(self, width=WIDTH, height=HEIGHT)
        self.canvas.pack(fill=BOTH)

        self.__draw_grid()
        self.__draw_puzzle()

    def __draw_grid(self):
        """Draws grid lines for the Sudoku board."""
        for i in range(10):
            color = "blue" if i % 3 == 0 else "gray"

            # Vertical lines
            x0 = MARGIN + i * SIDE
            y0 = MARGIN
            x1 = MARGIN + i * SIDE
            y1 = HEIGHT - MARGIN
            self.canvas.create_line(x0, y0, x1, y1, fill=color)

            # Horizontal lines
            x0 = MARGIN
            y0 = MARGIN + i * SIDE
            x1 = WIDTH - MARGIN
            y1 = MARGIN + i * SIDE
            self.canvas.create_line(x0, y0, x1, y1, fill=color)

    def __draw_puzzle(self):
        """Draws the Sudoku puzzle numbers"""
        self.canvas.delete("numbers")
        # Placeholder logic: Drawing numbers can be implemented later
        sudokid = Sudoku1.create_sudoku()
        solution = sudokid.get_solution()

        for i in range(9):
            for j in range(9):

                number = solution[i][j]
                x = MARGIN + j * SIDE + SIDE // 2
                y = MARGIN + i * SIDE + SIDE // 2
            
                self.canvas.create_text(x, y, text = str(number), tags = "numbers", fill = "black", font = ("Arial", 16))

if __name__ == "__main__":
    root = Tk()
    SudokuUI(root)
    root.geometry(f"{WIDTH}x{HEIGHT}")
    root.mainloop()



