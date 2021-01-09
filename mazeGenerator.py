import pygame
from collections import deque
import random
import time

ROWS = 30
SIZE = 1200
WIN = pygame.display.set_mode((SIZE + 2, SIZE + 2))
pygame.display.set_caption("Maze generator")

RED = (255, 0, 0)
GREEN = (100, 255, 100)
BLUE = (100, 100, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class Square:
    def __init__(self, row, col, size, total_rows):
        self.row = row
        self.col = col
        self.x = row * size
        self.y = col * size
        self.color = WHITE
        self.size = size
        self.top = True
        self.right = True
        self.bottom = True
        self.left = True

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.size, self.size))

    def draw_walls(self, win):
        # Top = 1, right = 2, bottom = 3 left = 4
        if self.top:
            pygame.draw.line(
                win, BLACK, (self.x, self.y), (self.x + self.size, self.y), 2
            )  # YLÄVAAKA

        if self.right:
            pygame.draw.line(
                win,
                BLACK,
                (self.x + self.size, self.y),
                (self.x + self.size, self.y + self.size),
                2,
            )  # OIKEA PYSTY

        if self.bottom:
            pygame.draw.line(
                win,
                BLACK,
                (self.x, self.y + self.size),
                (self.x + self.size, self.y + self.size),
                2,
            )  # ALA VAAKA

        if self.left:
            pygame.draw.line(
                win, BLACK, (self.x, self.y), (self.x, self.y + self.size), 2
            )  # VASENPYSTY


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
    grid[0][0].color = GREEN  # Set Start
    grid[-1][-1].color = BLUE  # Set End
    return grid


def random_next(current, used_spots, squares):
    #
    # if squares[0][0] in used_spots:
    #    print("löyty")
    possible_moves = []

    # Check possible moves
    # Left
    if current.row > 0:
        if (current.col, current.row - 1) not in used_spots:
            possible_moves.append(squares[current.row - 1][current.col])

    # Up
    if current.col > 0:
        if (current.col - 1, current.row) not in used_spots:
            possible_moves.append(squares[current.row][current.col - 1])

    # Right
    if current.row < ROWS - 1:
        if (current.col, current.row + 1) not in used_spots:
            possible_moves.append(squares[current.row + 1][current.col])

    # Down
    if current.col < ROWS - 1:
        if (current.col + 1, current.row) not in used_spots:
            possible_moves.append(squares[current.row][current.col + 1])

    if not possible_moves:
        return None

    # Random next direction
    next_move = random.choice(possible_moves)

    # Remove walls to moving direction
    if current.row > 0 and next_move == squares[current.row - 1][current.col]:
        squares[current.row][current.col].left = False
        squares[current.row - 1][current.col].right = False
    elif current.col > 0 and next_move == squares[current.row][current.col - 1]:
        squares[current.row][current.col].top = False
        squares[current.row][current.col - 1].bottom = False
    elif current.row < ROWS - 1 and next_move == squares[current.row + 1][current.col]:
        squares[current.row][current.col].right = False
        squares[current.row + 1][current.col].left = False
    elif current.col < ROWS - 1 and next_move == squares[current.row][current.col + 1]:
        squares[current.row][current.col].bottom = False
        squares[current.row][current.col + 1].top = False

    return next_move


def calculate_walls(squares):
    """
    Make maze from squares.
    Add walls to maze.
    """
    start = squares[0][0]
    used_spots = {(0, 0)}
    stack = deque()
    stack.append(start)
    current = start

    # Add left wall for window
    for x in squares[0]:
        x.left = True

    # Add bottom wall for window
    for x in squares:
        x[-1].bottom = True

    # Add Right wall for window
    for x in squares[-1]:
        x.right = True

    # Add left wall for window
    for x in squares:
        x[0].top = True

    # just for testing
    while len(stack) > 0:
        next = random_next(current, used_spots, squares)
        if next != None:
            print(len(used_spots))
            current = next
            stack.append(current)
            used_spots.add((current.col, current.row))
        else:
            current = stack.pop()
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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    squares = make_grid(ROWS, SIZE)
                    squares = calculate_walls(squares)

        draw(win, squares, ROWS, SIZE)


main(WIN)
