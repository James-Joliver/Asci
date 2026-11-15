import time

import numpy as np


class Cell:
    def __init__(self, x: int, y: int, type: str, initial_temp: float = 0.0):
        self.x = x
        self.y = y
        self.type = type
        self.visual = "0"
        self.temperature = initial_temp

        if self.type == "CONST":
            self.visual = "0"

        elif self.type == "BOARDER":
            self.visual = "#"

        elif self.type == "STANDARD":
            self.visual = "/"
        else:
            raise TypeError(f"{self.type} is not a valid type")

    def update(self, left, right, up, down):
        if self.type == "CONST":
            self.temperature = self.temperature

        elif self.type == "BOARDER":
            pass

        elif self.type == "STANDARD":
            self.temperature = (
                left.temperature + right.temperature + up.temperature + down.temperature
            ) / 4
        else:
            raise TypeError(f"{self.type} is not a valid type")

        # if self.type == "STANDARD":
        #     if self.temperature <= 15:
        #         self.visual = "."
        #     elif self.temperature > 15 and self.temperature <= 30:
        #         self.visual = "-"
        #     elif self.temperature > 30 and self.temperature <= 45:
        #         self.visual = ":"
        #     elif self.temperature > 45 and self.temperature <= 60:
        #         self.visual = "*"
        #     elif self.temperature > 60 and self.temperature <= 75:
        #         self.visual = "o"
        #     elif self.temperature > 75 and self.temperature <= 90:
        #         self.visual = "O"
        #     elif self.temperature > 90:
        #         self.visual = "0"
        #


class Grid:
    def __init__(self, rows, columns):
        self.column = columns + 2  # x : Leave room for the boarder
        self.row = rows + 2  # y : Leave room for the boarder
        self.columns = np.arange(columns)
        self.rows = np.arange(rows)
        # self.grid = [[Cell(x, y) for y in range(self.row)] for x in range(self.column)]
        self.grid = [
            [Cell(x, y, "BOARDER") for y in range(self.row)] for x in range(self.column)
        ]
        print("\033[2J")

    def update_grid(self):

        # TODO: Impliment a better Boundary compensation method
        #
        # for x in range(1, self.column + 1):
        for x in range(1, self.column - 1):
            for y in range(1, self.row - 1):
                current = self.grid[x][y]
                left = self.grid[x - 1][y]
                right = self.grid[x + 1][y]
                up = self.grid[x][y - 1]
                down = self.grid[x][y + 1]

                current.update(left, right, up, down)

    def draw_grid(self):

        # Build Visual Of Grid
        grid_visual = [
            [self.grid[x][y].visual for x in range(self.column)]
            for y in range(self.row)
        ]

        # Draw Frame
        output = "\033[H" + "\n".join("".join(row) for row in grid_visual)
        print(output, end="")

    def add_cell(self, x1, y1, x2, y2, cell_type, initial_temp=0.0):
        # TODO: make it so that (0, 0) is top left of inside of boarder
        # TODO: Handle "Point" Cells better (So add_cell(3,3,3,3,"BLINKER") will be a valid input)

        for column in range(x1 + 1, x2 + 1):
            for row in range(y1 + 1, y2 + 1):
                self.grid[column][row] = Cell(column, row, cell_type, initial_temp)


ROWS = 50
COLUMNS = 100

grid = Grid(ROWS, COLUMNS)


grid.add_cell(0, 0, COLUMNS, ROWS, "STANDARD")
grid.add_cell(COLUMNS, ROWS, COLUMNS, ROWS, "CONST")
# grid.add_cell(COLUMNS, 0, COLUMNS, ROWS, "CONST", initial_temp=100.0)  # Right wall
# grid.add_cell(0, ROWS, COLUMNS, ROWS, "CONST", initial_temp=0.0)  # Bottom wall
# grid.add_cell(0, 0, 0, ROWS, "CONST", initial_temp=30.0)  # Left Wall
# grid.add_cell(0, 0, COLUMNS, 0, "CONST", initial_temp=50.0)  # Top Wall

try:
    while True:
        grid.update_grid()
        grid.draw_grid()
        # time.sleep(0.01)
        # print(grid.grid[COLUMNS - 1][ROWS - 5].temperature)
except KeyboardInterrupt:
    print("\nStopped")
