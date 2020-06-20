from collections import defaultdict
import pygame, sys
from pygame.locals import *
assignments = []

rows = 'ABCDEFGHI'
cols = '123456789'

def cross(A, B):
    cross_prod = [x + y for x in A for y in B]
    return cross_prod

boxes = cross(rows, cols)
# components of all the units
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]
# Create a list of all units of a sudoku, unit list is same as peers,
# except it is inclusive of the current cell being looked at
unitlist = row_units + column_units + square_units
# Create a dictionary of peers of each box
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s], [])) - set([s])) for s in boxes)

def display(values, assignments, alpha):
    pygame.init()
    print(len(assignments))
    display_width = 600
    display_height = 600

    window = pygame.display.set_mode((display_width, display_height))
    pygame.display.set_caption('AI Sudoku Solver')

    image = pygame.image.load("sudoku-template-blank-sudoku-grid.png").convert_alpha()
    sprite = pygame.sprite.Sprite()
    sprite.image = image
    sprite.rect = image.get_rect()

    clock = pygame.time.Clock()

    black = (0, 0, 0)
    white = (255, 255, 255)
    red = (255, 0, 0)
    numberfont = pygame.font.Font('freesansbold.ttf', 25)
    gameLoop = True

    counter = -1
    ints = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    while (gameLoop):
        pygame.event.get()
        if counter < (len(assignments)) and not counter == -1:
            values = assignments[counter]
            pygame.time.wait(500)
        window.fill(black)
        window.blit(image, (45, 45))
        pygame.display.flip()
        for key, value in values.items():
            x = 30 + (alpha[key[0]] * 55)
            y = 30 + ((int(key[1]) - 1) * 55)
            if int(value) < 10:
                cellSurf = numberfont.render('%s' % (int(value)), True, black)
                cellRect = cellSurf.get_rect()
                cellRect.topleft = (x, y)
            else:
                sprite.image.fill(white, (x, y, 25, 25))
            sprite.image.fill(white, (x, y, 25, 25))
            sprite.image.blit(cellSurf, cellRect)
        counter = counter + 1
        if counter == len(assignments):
            pygame.event.get()
            window.fill(black)
            window.blit(image, (45, 45))
            pygame.display.flip()
            sprite.image.fill(white, (x, y, 25, 25))
            sprite.image.blit(cellSurf, cellRect)
            pygame.time.wait(5000)
            gameLoop = False

    pygame.quit()

def assign_value(values, box, value):
    if values[box] == value:
        return values
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_triples(values):
    final_triple_dict = {}
    for unit in unitlist:
        # First, check for cells with only three possible values
        # as they are potential candidates
        potential = {}
        for box in unit:
            if len(values[box]) == 3:
                if not values[box] in potential:
                    potential[values[box]] = [box]
                else:
                    potential[values[box]].append(box)
        # Select candidates that are a true naked triple pair
        for key in potential:
            if len(potential[key]) == 3:
                if not key in final_triple_dict:
                    final_triple_dict[key] = [unit]
                else:
                    final_triple_dict[key].append(unit)
    # Eliminate naked triples from other possible values
    for key in final_triple_dict:
        for unit in final_triple_dict[key]:
            for box in unit:
                if values[box] != key:
                    assign_value(values, box, values[box].replace(key[0], ''))
                    assign_value(values, box, values[box].replace(key[1], ''))
                    assign_value(values, box, values[box].replace(key[2], ''))
    return values

def naked_twins(values):
    final_twin_dict = {}
    for unit in unitlist:
        # First, check for cells with only two possible values
        # as they are potential candidates
        potential = {}
        for box in unit:
            if len(values[box]) == 2:
                if not values[box] in potential:
                    potential[values[box]] = [box]
                else:
                    potential[values[box]].append(box)
        # Select candidates that are a true naked twin pair
        for key in potential:
            if len(potential[key]) == 2:
                if not key in final_twin_dict:
                    final_twin_dict[key] = [unit]
                else:
                    final_twin_dict[key].append(unit)
    # Eliminate naked twins from other possible values
    for key in final_twin_dict:
        for unit in final_twin_dict[key]:
            for box in unit:
                if values[box] != key:
                    assign_value(values, box, values[box].replace(key[0], ''))
                    assign_value(values, box, values[box].replace(key[1], ''))
    return values

# Assigns input to cells
def cell_values(grid):
    values = []
    all_digits = '123456789'
    for num in grid:
        if num == '.':
            values.append(all_digits)
        elif num in all_digits:
            values.append(num)
    if len(values) == 81:
        return dict(zip(boxes, values))

# If a value is assigned to a cell, eliminate it from the possible values of its peers
def eliminate(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    # for all solved values, eliminate that value as a possibility from its peers
    for solved_val in solved_values:
        num = values[solved_val]
        peers_solv = peers[solved_val]
        for peer in peers_solv:
            values[peer] = values[peer].replace(num, '')
            values = assign_value(values, peer, values[peer].replace(num, ''))
    return values

# Assigns possible value to a cell if doesn't appear in
# any other cell's possibilities
def only_choice(values):
    for unit in unitlist:
        for digit in '123456789':
            dplaces = []
            for box in unit:
                if digit in values[box]:
                    dplaces.append(box)
            if len(dplaces) == 1:
                assign_value(values, dplaces[0], digit)
    return values

# Runs through each heuristic until no more progress is made
def reduce_puzzle(values):
    stalled = False
    while not stalled:
        values_before = values.copy()
        values = eliminate(values)
        values = naked_twins(values)
        values = naked_triples(values)
        values = only_choice(values)
        stalled = values_before == values
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

# If the reduce_puzzle method stalls, copy the board and guess a value for the cell with the least potential solutions,
# Once chosen, call the reduce_puzzle method again, back track if the attempt fails.
def search(values):
    values = reduce_puzzle(values)
    if all(len(values[s]) == 1 for s in boxes):
        return values
    n, s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

def main():
    sudoku_grid = input()
    originalValues = cell_values(sudoku_grid)
    values = cell_values(sudoku_grid)
    values = search(values)
    assignments.append(values.copy())

    alpha = {}
    alpha['A'] = 0
    alpha['B'] = 1
    alpha['C'] = 2
    alpha['D'] = 3
    alpha['E'] = 4
    alpha['F'] = 5
    alpha['G'] = 6
    alpha['H'] = 7
    alpha['I'] = 8
    display(originalValues, assignments, alpha)

main()
#Valid Input:2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3