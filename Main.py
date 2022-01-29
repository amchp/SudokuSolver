import tkinter as tk

from typing import List
	
import time

# Returns a boolean which indicates whether any assigned entry
# in the specified row matches the given number.
def used_in_row(arr, row, num):
    for i in range(9):
        if (arr[row][i] == num):
            return True
    return False


# Returns a boolean which indicates whether any assigned entry
# in the specified column matches the given number.
def used_in_col(arr, col, num):
    for i in range(9):
        if (arr[i][col] == num):
            return True
    return False


# Returns a boolean which indicates whether any assigned entry
# within the specified 3x3 box matches the given number
def used_in_box(arr, row, col, num):
    for i in range(3):
        for j in range(3):
            if (arr[i + row][j + col] == num):
                return True
    return False


def find_empty_location(arr, l):
    for row in range(9):
        for col in range(9):
            if arr[row][col] == 0:
                l[0] = row
                l[1] = col
                return True
    return False


def check_location_is_safe(arr, row, col, num):
    # Check if 'num' is not already placed in current row,
    # current column and current 3x3 box
    return not used_in_row(arr, row, num) and not used_in_col(arr, col, num) and not used_in_box(arr, row - row % 3,col - col % 3, num)


class Main(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.canvas = tk.Canvas(master, width=460, height=460)
        self.canvas.grid()
        self.selectedI = -1
        self.selectedJ = -1
        self.board = []
        self.solving = False
        for i in range(9):
            self.board.append([0] * 9)
        self.drawBoard()

    def drawBoard(self):
        self.canvas.create_rectangle(5,5,455,455, width="4")
        for i in range(0,9):
            for j in range(0,9):
                filler = "#FFFFFF"
                if(self.selectedI == i and self.selectedJ == j):
                    filler = "#AAFFAA"
                self.canvas.create_rectangle(i*50+5, j*50+5, i*50+55, j*50+55, fill=filler)
                if self.board[i][j] != 0:
                    self.canvas.create_text(i*50+30, j*50+30, font="Times 32", text=self.board[i][j], fill="#000000")
        self.canvas.create_line(155,0,155,455, width="4")
        self.canvas.create_line(305,0,305,455, width="4")
        self.canvas.create_line(0,155,455,155, width="4")
        self.canvas.create_line(0,305,455,305, width="4")
        

    def solve(self):
        self.selectedI = -1
        self.selectedJ = -1
        self.initial_board = [[0]*9  for i in range(9)]
        for row in range(0,9):
            for col in range(0, 9):
                self.initial_board[row][col] = self.board[row][col]
        result = self.solve_sudoku()
        print(result)
        if result:
            pass
        else:
            for row in range(0,9):
                for col in range(0, 9):
                    self.board[row][col] = self.initial_board[row][col]
        self.solving = False
        self.mainloop()

    def solve_sudoku(self):
        l: List[int] = [0, 0]
        if not find_empty_location(self.board, l):
            return True
        row = l[0]
        col = l[1]
        # consider digits 1 to 9
        for num in range(1, 10):
            # if looks promising
            if check_location_is_safe(self.board, row, col, num):
                # make tentative assignment
                self.board[row][col] = num
                # return, if success, ya!
                self.drawBoard()
                self.canvas.update()
                if self.solve_sudoku():
                    return True

                # failure, unmake & try again
                self.board[row][col] = 0
        # this triggers backtracking
        return False

    def click(self, event):
        if self.solving:
            return
        self.mouseX, self.mouseY = event.x, event.y
        Pass = False 
        for i in range(9):
            for j in range(9):
                if(self.mouseX > 5 + 50*i and
                    self.mouseX < 5 + 50*(i) + 55 and
                    self.mouseY > 5 + 50*j and
                    self.mouseY < 5 + 50*j + 55):
                    self.selectedI = i
                    self.selectedJ = j
                    Pass = True
        if not Pass:
            self.selectedI = -1
            self.selectedJ = -1
        self.drawBoard()

    def onKeyPress(self, event):
        if self.solving:
            return
        i = self.selectedI
        j = self.selectedJ
        if(event.char.isdigit() and 
            i != -1 and
            j!= -1):
            self.board[i][j] = int(event.char)
        elif(event.char == " "):
            self.master.quit()
            self.solving = True
            self.solve()
        if(event.keysym == "BackSpace"):
            self.board = []
            for i in range(9):
                self.board.append([0] * 9)
        self.drawBoard()
        

def main():
    root = tk.Tk()
    app = Main(master=root)
    root.bind('<ButtonRelease-1>', app.click)
    root.bind('<KeyPress>', app.onKeyPress)
    app.mainloop()

if __name__ == "__main__":
    main()
