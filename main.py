from _tkinter import Tk, Canvas, Frame, Button, BOTH, TOP, BOTTOM, SIDE, MARGIN, HEIGHT, WIDTH

class SudokuUI(Frame):
    def __init__(self, parent):
        self.parent = parent
        Frame.__init__(self, parent)

        self.row, self.col = 0, 0

        self.__initUI()

        def __initUI(self):
            self.parent.title("Sudokoid")
            self.pack(fill=BOTH, expand = 1)
            self.canvas = Canvas(self, width = WIDTH,
                                 height = HEIGHT)
            
            self.canvas.pack(fill = BOTH, side = TOP)
        
            self.__draw_grid()
            self.__draw_puzzle(0)
        
        def __draw_grid(self):

            for i in range(1, 10):
                color = "blue" if i % 3 == 0 else "gray"

                x0 = MARGIN + i * SIDE
                y0 = MARGIN
                x1 = MARGIN + i * SIDE
                y1 = HEIGHT - MARGIN
                self.canvas.create_line(x0, y0, x1, y1, fill = color)

                x0 = MARGIN
                y0 = MARGIN + i * SIDE
                x1 = WIDTH - MARGIN
                y1 = MARGIN + i * SIDE
                self.canvas.create_line(x0, y0, x1, y1, fill = color)

        def __draw_puzzle(self):
            self.canvas.delete("numbers")
            for i in range(1, 9):


