import pygame
import random

# creating the data structure for pieces
# setting up global vars
# functions
# - create_grid
# - draw_grid
# - draw_window
# - rotating shape in main
# - setting up the main

"""
10 x 20 square grid
shapes: S, Z, I, O, J, L, T
represented in order by 0 - 6
"""

pygame.font.init()

# GLOBALS VARIABLES
# s_width tells screen width
s_width = 800
# s_heigth tells screen heigth
s_height = 700
play_width = 300  # meaning 300 // 10 = 30 width per block
play_height = 600  # meaning 600 // 20 = 20 height per block
block_size = 30

# Top_left position of play area
top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height


# SHAPE FORMATS

S = [['.....',
      '......',
      '..00..',
      '.00...',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]


# Holds all the shapes in an array
shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255),
                (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]
# index 0 - 6 represent shape


class Piece(object):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape

        # gets the equivelant color
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0


def create_grid(locked_pos={}):
    # ten colors since there are ten squares in each row. 20 Rows in total
    # (0, 0, 0 stands for black)
    grid = [[(0, 0, 0) for x in range(10)] for x in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_pos:
                c = locked_pos[(j, i)]
                grid[i][j] = c
    return grid


# Converts the shapes so that computer can understand the shapes
def convert_shape_format(shape):
    positions = []
    # gets the leftover shape, meaning the shape that will be used
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        # '..0..' (j is 0, column is period )
        for j, column in enumerate(row):
            if column == '0':
                # current column, current row
                positions.append((shape.x + j, shape.y + i))

    # Remove the trailing periods (..0..) Everything has to be offset down (meaning - 2 and - 4) This will move everything left and up. This results in more accuracy to the screen
    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    # Return the list
    return positions


def clear_rows(grid, locked):

    incrament = 0
    # Loops through grid backwards (-1, -1, -1)
    for i in range(len(grid)-1, -1, -1):
        # row is equal to every row in our grid
        row = grid[i]
        # (0, 0, 0 means color black)
        if (0, 0, 0) not in row:
            # add a row to incrament variable (Tells how many rows have to be cleared)
            incrament += 1
            # index tells what positions to shift
            index = i
            # Getting every position in the row
            # Because we are in the current row, i stays static
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue

    if incrament > 0:
        #  For every key in lockedpositions, based on y values
        # Starting from the bottom so that values aren't overwritten
        # [::-1] looks at things backwards
        # [(0,1), (0,0)]
        # --> [(0,0), (0,1)]
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            # getting every x & y position of each key in locked positions
            x, y = key
            if y < index:
                # Adding to the y value to shift it down
                newKey = (x, y + incrament)
                # Add an empty row on top
                locked[newKey] = locked.pop(key)

    # Returns how many rows has been cleared
    return incrament


def valid_space(shape, grid):
    # Every single position for 10 20 grid
    # Only adding a position into accepted_pos if it is empty
    # Imbedded for loops to create a list
    accepted_pos = [[(j, i) for j in range(10) if grid[i]
                     [j] == (0, 0, 0)] for i in range(20)]

    # Flattens the list, so it is one dimensional. [[(0,1)], [(2,3)]] --> [(0,1), (2,3)]
    accepted_pos = [j for sub in accepted_pos for j in sub]

    formatted = convert_shape_format(shape)

    for pos in formatted:
        if pos not in accepted_pos:
            if pos[1] > -1:
                return False
    return True


# Checks if any of the positions are above the screen
def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True

    return False


def get_shape():
    return Piece(5, 0, random.choice(shapes))


def draw_next_shape(shape, surface):
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Next Shape', 1, (255, 255, 255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height/2 - 100

    # Get the actual sublist that is needed (the shape that will be shown next)
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color, (sx + j*block_size,
                                 sy + i*block_size, block_size, block_size), 0)

    surface.blit(label, (sx + 10, sy - 30))


def draw_text_middle(text, size, color, surface):
    pass

# Draws the gray lines on top of the grid


def draw_grid(surface, grid):
    sx = top_left_x
    sy = top_left_y

    for i in range(len(grid)):
        pygame.draw.line(surface, (128, 128, 128), (sx, sy +
                         i*block_size), (sx+play_width, sy + i*block_size))
        for j in range(len(grid[i])):
            pygame.draw.line(surface, (128, 128, 128), (sx + j *
                             block_size, sy), (sx+j*block_size, sy + play_height))

            # Default value of 0


def draw_window(surface, grid, score=0):
    surface.fill((0, 0, 0))
    pygame.font.init()
    font = pygame.font.SysFont('comicsans', 60)
    title_label = font.render('Tetris Seminaari', 1, (255, 255, 255))

    font = pygame.font.SysFont('comicsans', 30)
    score_label = font.render('Your score: ' + str(score), 1, (255, 255, 255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height/2 - 100

    # Attach at the top middle of the screen # Automatically adapt to screen size
    surface.blit(title_label, (top_left_x + play_width /
                 2 - (title_label.get_width() / 2), 17))

    surface.blit(score_label, (sx + 10, sy + 160))

    # Loop for drawing the grid
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j*block_size,
                             top_left_y + i*block_size, block_size, block_size), 0)

    # Draws the game grid
    pygame.draw.rect(surface, (255, 0, 0),
                     (top_left_x, top_left_y, play_width, play_height), 5)

    draw_grid(surface, grid)


def main(win):

    locked_positions = {}
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.27
    level_time = 0
    score = 0

    while run:
        grid = create_grid(locked_positions)

        # get_rawtime gets the amount of time since clock.tick() ticked
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()

        # The speed is increased every five minutes
        if level_time/1000 > 5:
            level_time = 0
            if fall_speed > 0.11:
                # Takes about minute and fourty seconds before reaching terminal velocity
                fall_speed -= 0.004

        # Automatically moves peace down
        if fall_time/1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            # Moves a piece back if hits the walls
            if not (valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.x += 1
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.x -= 1
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.y -= 1
                if event.key == pygame.K_UP:
                    current_piece.rotation += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.rotation -= 1

        # Check all the positions falling down, if their hitting the ground etc..
        shape_pos = convert_shape_format(current_piece)

        # Drawing colors for the shapes
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            # Checks if a position is above the screen
            if y > -1:
                grid[y][x] = current_piece.color

        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                # Checks whether the piece is not moving anymore.
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            # Change piece will be set false because a new piece is spawned at the top of the screen
            change_piece = False
            score += clear_rows(grid, locked_positions) * 10

        draw_window(win, grid, score)
        draw_next_shape(next_piece, win)
        pygame.display.update()

        # Breaks the while loop and ends the game
        if check_lost(locked_positions):
            run = False

    pygame.display.quit()


def main_menu(win):  # *
    main(win)


win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Seminaari Tetris')
main_menu(win)


main_menu()  # start game
