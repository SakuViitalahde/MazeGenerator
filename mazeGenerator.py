import pygame

ROWS = 50
SIZE = 1000
WIN = pygame.display.set_mode((SIZE+2, SIZE+2))
pygame.display.set_caption("Maze generator")

RED = (255, 0, 0)
GREEN = (100, 255, 100)
BLUE = (100, 100, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Square():
    def __init__(self, row, col, size, total_rows):
        self.row = row
        self.col = col
        self.x = row * size
        self.y = col * size
        self.color = WHITE
        self.size = size
        self.top = False
        self.right = False
        self.bottom = False
        self.left = False
    
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.size, self.size))

    def draw_walls(self, win):
        # Top = 1, right = 2, bottom = 3 left = 4
        if self.top:
            pygame.draw.line(win, BLACK, (self.x, self.y), (self.x  + self.size, self.y),2 ) # YLÄVAAKA

        if self.right:
            pygame.draw.line(win, BLACK, (self.x + self.size, self.y), (self.x + self.size, self.y + self.size), 2) # OIKEA PYSTY

        if self.bottom:
            pygame.draw.line(win, BLACK, (self.x, self.y + self.size), (self.x + self.size, self.y + self.size), 2) # ALA VAAKA

        if self.left:
            pygame.draw.line(win, BLACK, (self.x, self.y), (self.x, self.y + self.size), 2) # VASENPYSTY



def make_grid(rows, size):
    """
    Make grid i is rows and j is columns.
    Gap is width and height of spot.
    """
    grid = []
    gap = size // rows
    for i in range(rows):
        row = []
        for j in range(rows):
            square = Square(i, j, gap, rows)
            row.append(square)
        grid.append(row)
    grid[0][0].color = GREEN # Set Start
    grid[-1][-1].color = BLUE # Set End
    return grid

def add_walls_for_square(squares, x, y):
    squares[y][x].top = True
    squares[y][x].left = True
    squares[y][x].right = True
    squares[y][x].bottom = True
    return squares

def calculate_walls(squares):
    """
    Make maze from squares.
    Add walls to maze.
    """
    grid = {}
    grid[(0,0)] = squares[0][0]

    #Add left wall for window
    for x in squares[0]:
        x.left = True

    #Add bottom wall for window
    for x in squares:
        x[-1].bottom = True

    #Add Right wall for window
    for x in squares[-1]:
        x.right = True
    
    #Add left wall for window
    for x in squares:
        x[0].top = True
    
    squares = add_walls_for_square(squares, 1, 1)
    return squares

def draw(window, squares, rows, size):
    window.fill(WHITE)

    # Loops, one draws squares backgrounds and second one walls.
    # If done in one loop walls will go under backgrounds.
    # not perfect solution but works for now.
    for row in squares:
        for square in row:
            if square.color != WHITE:
                square.draw(window)
    
    for row in squares:
        for square in row:
            square.draw_walls(window)

    pygame.display.update()

def main(win):
    squares = make_grid(ROWS, SIZE)
    squares = calculate_walls(squares)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        draw(win, squares, ROWS, SIZE)
main(WIN)
