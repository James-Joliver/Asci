import time

import numpy as np


class Cell:
    def __init__(self, x: int, y: int, type: str):
        self.x = x
        self.y = y
        self.type = type
        self.visual = "0"
        if self.type == "BLINKER":
            self.visual = "0"
            self.itter = 0

        elif self.type == "BOARDER":
            self.visual = "#"

        elif self.type == "STANDARD":
            self.visual = "/"
        else:
            raise TypeError(f"{self.type} is not a valid type")

    def update(self, left, right, up, down):
        if self.type == "BLINKER":
            if self.itter > 10:
                if self.visual == "0":
                    self.visual = "o"
                elif self.visual == "o":
                    self.visual = "0"
                self.itter = 0
            else:
                self.itter += 1

        elif self.type == "BOARDER":
            self.visual = "#"

        elif self.type == "STANDARD":
            if left.visual != self.visual and left.type != "BOARDER":
                self.visual = left.visual
            elif up.visual != self.visual and up.type != "BOARDER":
                self.visual = up.visual
            elif right.visual != self.visual and right.type != "BOARDER":
                self.visual = right.visual
            elif down.visual != self.visual and down.type != "BOARDER":
                self.visual = down.visual
            else:
                pass
        else:
            raise TypeError(f"{self.type} is not a valid type")


class Grid:
    def __init__(self, rows, columns):
        self.column = columns  # x
        self.row = rows  # y
        self.columns = np.arange(columns)
        self.rows = np.arange(rows)
        # self.grid = [[Cell(x, y) for y in range(self.row)] for x in range(self.column)]
        self.grid = [
            [Cell(x, y, "BOARDER") for y in range(self.row)] for x in range(self.column)
        ]

        print("\033[2J")

    def update_grid(self):

        # TODO: Impliment a better Boundary compensation method
        for x in np.arange(1, (self.column - 1)):
            for y in np.arange(1, (self.row - 1)):
                current = self.grid[x][y]
                left = self.grid[x - 1][y]
                right = self.grid[x + 1][y]
                up = self.grid[x][y - 1]
                down = self.grid[x][y + 1]

                current.update(left, right, up, down)

    def draw_grid(self):

        # Build Visual Of Grid
        grid_visual = [
            [self.grid[x][y].visual for x in self.columns] for y in range(self.row)
        ]

        # Draw Frame
        output = "\033[H" + "\n".join("".join(row) for row in grid_visual)
        print(output, end="")

    def add_cell(self, x1, y1, x2, y2, cell_type):
        # TODO: make it so that (0, 0) is top left of inside of boarder
        # TODO: Handle "Point" Cells better (So add_cell(3,3,3,3,"BLINKER") will be a valid input)

        for column in range(x1, x2):
            for row in range(y1, y2):
                self.grid[column][row] = Cell(column, row, cell_type)


ROWS = 50
COLUMNS = 100

grid = Grid(ROWS, COLUMNS)
grid.add_cell(1, 1, COLUMNS - 1, ROWS - 1, "STANDARD")
# grid.add_cell(COLUMNS - 2, ROWS - 2, COLUMNS - 1, ROWS - 1, "BLINKER")
grid.add_cell(COLUMNS - 2, 1, COLUMNS - 1, ROWS - 2, "BLINKER")
grid.add_cell(1, ROWS - 2, COLUMNS - 1, ROWS - 1, "BLINKER")

try:
    while True:
        grid.update_grid()
        grid.draw_grid()
        time.sleep(0.1)
except KeyboardInterrupt:
    print("\nStopped")
