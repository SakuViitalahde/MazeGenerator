import pygame

ROWS = 50
SIZE = 1000
WIN = pygame.display.set_mode((SIZE, SIZE))
pygame.display.set_caption("Maze generator")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
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
    
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.size, self.size))

        pygame.draw.line(win, BLACK, (self.x, self.y), (self.x, self.y + self.size),2 ) # VASENPYSTY

        pygame.draw.line(win, BLACK, (self.x, self.y), (self.x  + self.size, self.y),2 ) # YLÄVAAKA

        pygame.draw.line(win, BLACK, (self.x, self.y + self.size), (self.x + self.size, self.y + self.size), 2) # ALA VAAKA

        pygame.draw.line(win, BLACK, (self.x + self.size, self.y), (self.x + self.size, self.y + self.size), 2) # OIKEA PYSTY

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
    return grid

def draw(window, squares, rows, size):
    window.fill(WHITE)

    for row in squares:
        for square in row:
            square.draw(window)

    pygame.display.update()

def main(win):
    squares = make_grid(ROWS, SIZE)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        draw(win, squares, ROWS, SIZE)
main(WIN)
