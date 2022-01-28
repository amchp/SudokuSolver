from typing import List

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
    return not used_in_row(arr, row, num) and not used_in_col(arr, col, num) and not used_in_box(arr, row - row % 3,
                                                                                                 col - col % 3, num)

class Sudoko:

    def __init__(self, arr):
        self.board = [[0] * 9 for i in range(9)]
        self.solution = [[0]*9  for i in range(9)]
        for row in range(0,9):
            for col in range(0, 9):
                self.board[row][col] = arr[row][col]
                self.solution[row][col] = arr[row][col]
        self.solve_sudoku()

    def print_grid(self):
        for row in self.solution:
            print(row)

    def solve_sudoku(self):
        l: List[int] = [0, 0]
        if not find_empty_location(self.solution, l):
            return True
        row = l[0]
        col = l[1]
        # consider digits 1 to 9
        for num in range(1, 10):

            # if looks promising
            if check_location_is_safe(self.solution, row, col, num):
                # make tentative assignment
                self.solution[row][col] = num

                # return, if success, ya!
                if self.solve_sudoku():
                    return True

                # failure, unmake & try again
                self.solution[row][col] = 0
        # this triggers backtracking
        return False
