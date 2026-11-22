import numpy as np


class Cell:
    def __init__(
        self,
        x: int,
        y: int,
        type: str,
        initial_temp: float = 0.0,
        q_dot: float = 0.0,
        k: float = 0.0,
        dx: float = 0.0,
    ):
        self.x = x
        self.y = y
        self.type = type
        self.visual = "0"
        self.temperature = initial_temp
        self.q_dot = q_dot
        self.k = k
        self.dx = dx

        # Initialize Visual
        if self.type == "CONST":
            self.visual = "0"
        elif self.type == "BOARDER":
            self.visual = "#"
        elif self.type == "STANDARD":
            self.visual = "/"
        elif self.type == "SIN":
            self.visual = "%"
            self.itterator = 0
            self.multiplyer = initial_temp
        else:
            raise TypeError(f"{self.type} is not a valid type")

    def update(self, left, right, up, down):

        # Temperature Logic
        if self.type == "CONST":
            self.temperature = self.temperature
        elif self.type == "BOARDER":
            pass
        elif self.type == "STANDARD":
            temps = [
                x.temperature for x in [left, right, up, down] if x.type != "BOARDER"
            ]
            self.temperature = sum(temps) / len(temps) + (self.q_dot * self.dx**2) / (
                len(temps) * self.k
            )
        elif self.type == "SIN":
            self.itterator += 0.001
            self.temperature = np.sin(self.itterator) * self.multiplyer

        else:
            raise TypeError(f"{self.type} is not a valid type")

        # Choose Visual
        if self.type != "BOARDER":
            if self.temperature <= 15:
                self.visual = "."
            elif self.temperature > 15 and self.temperature <= 30:
                self.visual = "-"
            elif self.temperature > 30 and self.temperature <= 45:
                self.visual = ":"
            elif self.temperature > 45 and self.temperature <= 60:
                self.visual = "*"
            elif self.temperature > 60 and self.temperature <= 75:
                self.visual = "o"
            elif self.temperature > 75 and self.temperature <= 90:
                self.visual = "O"
            elif self.temperature > 90:
                self.visual = "0"


class Grid:
    def __init__(self, rows, columns):
        self.column = columns + 2  # x : Leave room for the boarder
        self.row = rows + 2  # y : Leave room for the boarder

        # Initialize Grids
        self.grid = [
            [Cell(x, y, "BOARDER") for y in range(self.row)] for x in range(self.column)
        ]
        self.grid_visual = [
            [self.grid[x][y].visual for x in range(self.column)]
            for y in range(self.row)
        ]

        # Clear Screen
        print("\033[2J")

    def update_grid(self):

        # Update Each Cell
        for x in range(1, self.column - 1):
            for y in range(1, self.row - 1):
                current = self.grid[x][y]
                left = self.grid[x - 1][y]
                right = self.grid[x + 1][y]
                up = self.grid[x][y - 1]
                down = self.grid[x][y + 1]

                current.update(left, right, up, down)

                # y and x are inversed here because of how the output is formulated
                self.grid_visual[y][x] = current.visual

    def draw_grid(self):

        # Draw Frame
        output = "\033[H" + "\n".join("".join(row) for row in self.grid_visual)
        print(output, end="")

    def add_cell(
        self,
        row1,
        column1,
        row2,
        column2,
        cell_type,
        initial_temp=0.0,
        q_dot=0.0,
        k=0.0,
        dx=0.0,
    ):

        for column in range(column1, column2 + 1):
            for row in range(row1, row2 + 1):
                self.grid[column][row] = Cell(
                    column, row, cell_type, initial_temp, q_dot, k, dx
                )


ROWS = 50
COLUMNS = 100

# Initialize Grid
grid = Grid(ROWS, COLUMNS)

# Add Cells to Grid
grid.add_cell(1, 1, ROWS, COLUMNS, "STANDARD", 0.0, 0.5, 1, 1)
# grid.add_cell(1, 1, ROWS, COLUMNS, "STANDARD")
grid.add_cell(ROWS, 1, ROWS, COLUMNS, "CONST", initial_temp=0.0)  # Bottom wall
grid.add_cell(1, 1, 1, COLUMNS, "CONST", initial_temp=100.0)  # Top Wall
grid.add_cell(1, 1, ROWS, 1, "CONST", initial_temp=0.0)  # Left Wall
grid.add_cell(1, COLUMNS, ROWS, COLUMNS, "CONST", initial_temp=80.0)  # Right wall
# grid.add_cell(20, 50, 30, 60, "SIN", initial_temp=100.0)  # Center ish box

# grid.add_cell(1, 1, 1, 1, "CONST", initial_temp=100)

try:
    while True:
        grid.update_grid()
        grid.draw_grid()
except KeyboardInterrupt:
    print("\nStopped")
