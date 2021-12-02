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


def create_grid(locked_positions={}):
    # ten colors since there are ten squares in each row. 20 Rows in total
    # (0, 0, 0 stands for black)
    grid = [[(0, 0, 0) for x in range(10)] for x in range(20)]

    # Checks which positions are locked when peaces have fallen down
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_positions:
                c = locked_positions[(j, i)]
                # Freezes the positions
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


def update_totalscore(nscore):
    with open('scoreboard.txt', 'r') as f:
        lines = f.readlines()
        score = lines[0].strip()

    with open('scoreboard.txt', 'w') as f:
        if int(score) > nscore:
            f.write(str(score))
        else:
            f.write(str(nscore))


def high_score():
    with open('scoreboard.txt', 'r') as f:
        lines = f.readlines()
        score = lines[0].strip()

    return score


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

    # Returns how many rows have been cleared
    return incrament


def valid_space(shape, grid):
    # Every single position for 10 20 grid
    # Only adding a position into accepted_pos if it is empty
    # Imbedded for-loops to create a list
    valid_position = [[(j, i) for j in range(10) if grid[i]
                       [j] == (0, 0, 0)] for i in range(20)]

    # Flattens the list, so it is one dimensional. [[(0,1)], [(2,3)]] --> [(0,1), (2,3)]
    valid_position = [j for sub in valid_position for j in sub]

    formatted_positions = convert_shape_format(shape)

    for position in formatted_positions:
        if position not in valid_position:
            # Tells whether we'are on the grid or not
            if position[1] > -1:
                return False
    return True


# Checks if any of the positions are above the screen
def check_lost(positions):
    for pos in positions:
        x, y = pos
        # If every position is creater than 1, return
        if y < 1:
            return True

    return False


def get_shape():
    return Piece(5, 0, random.choice(shapes))


def draw_text_middle(surface, text, size, color):
    font = pygame.font.SysFont("mvboli", size)
    label = font.render(text, 1, color)

    surface.blit(label, (top_left_x + play_width/2 - (label.get_width()/2),
                 top_left_y + play_height/2 - label.get_height()/2))


def draw_text_top(last_score, surface, text, size, color):
    full_text = text + last_score
    font = pygame.font.SysFont("mvboli", size)
    label = font.render(full_text, last_score, 1, color)

    sx = top_left_x - 200
    sy = top_left_y + 360

    surface.blit(label, (sx + 270, sy))


def draw_next_shape(shape, surface):
    font = pygame.font.SysFont('mvboli', 26)
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
                                 sy + 17 + i*block_size, block_size, block_size), 0)

    surface.blit(label, (sx + 10, sy - 30))


def draw_grid(surface, grid):
    sx = top_left_x
    sy = top_left_y

    for i in range(len(grid)):
        pygame.draw.line(surface, (0, 247, 255), (sx, sy +
                         i*block_size), (sx+play_width, sy + i*block_size))
        for j in range(len(grid[i])):
            pygame.draw.line(surface, (0, 247, 255), (sx + j *
                             block_size, sy), (sx+j*block_size, sy + play_height))

            # Default value of 0


def draw_window(surface, grid, score=0, last_score=0):
    surface.fill((0, 0, 0))
    pygame.font.init()
    font = pygame.font.SysFont(
        'mvboli', 40)
    title_label = font.render('Tetris Seminaari', 1, (255, 255, 255))

    font = pygame.font.SysFont(
        'mvboli', 23)
    score_label = font.render('Your score: ' + str(score), 1, (255, 255, 255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height/2 - 100

    # Attach at the top middle of the screen # Automatically adapt to screen size
    surface.blit(title_label, (top_left_x + play_width /
                 2 - (title_label.get_width() / 2), 17))

    surface.blit(score_label, (sx + 10, sy - 211))

    # High-score
    score_label = font.render('High score: ' + last_score, 1, (255, 255, 255))

    sx = top_left_x - 230
    sy = top_left_y + 200

    surface.blit(score_label, (sx + 10, sy - 211))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j*block_size,
                             top_left_y + i*block_size, block_size, block_size), 0)

    # Draws the game grid
    pygame.draw.rect(surface, (86, 0, 199),
                     (top_left_x, top_left_y, play_width, play_height), 5)

    draw_grid(surface, grid)


def main(window):
    last_score = high_score()
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

        # The speed is increased every five seconds
        if level_time/1000 > 5:
            level_time = 0
            if fall_speed > 0.11:
                # Takes about minute and 50 seconds before getting closer to reaching terminal velocity
                fall_speed -= 0.004

        # Automatically moves peace down
        if fall_time/1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            # Moves a piece back if hits the walls or is not valid
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

        # Check all the positions falling down, if they're hitting the ground etc..
        shape_positions = convert_shape_format(current_piece)

        # Drawing colors for the shapes
        for i in range(len(shape_positions)):
            x, y = shape_positions[i]
            # Checks if a position is above the screen
            if y > -1:
                grid[y][x] = current_piece.color

        if change_piece:
            for position in shape_positions:
                p = (position[0], position[1])
                # Checks whether the piece is not moving anymore.
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            # Change piece will be set false because a new piece is spawned at the top of the screen
            change_piece = False
            score += clear_rows(grid, locked_positions) * 100

        draw_window(window, grid, score, last_score)
        draw_next_shape(next_piece, window)
        pygame.display.update()

        # Breaks the while loop and ends the game
        if check_lost(locked_positions):
            draw_text_middle(window, "YOU LOST! YOUR SCORE: " +
                             str(score), 38, (255, 222, 0))
            pygame.display.update()
            pygame.time.delay(2000)
            run = False
            update_totalscore(score)
            main_menu(window, last_score)

    pygame.display.quit()


def main_menu(win, last_score):  # *
    run = True
    while run:
        win.fill((0, 0, 0))
        draw_text_middle(
            win, 'Press Any Key To Play This Fabulous Tetris Game', 29, (40, 255, 255))

        draw_text_top(
            last_score, win, 'Highscore: ', 29, (222, 90, 90))

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main(win)
    # View disappears
    pygame.display.quit()


last_score = high_score()
win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Seminaari Tetris')
main_menu(win, last_score)
