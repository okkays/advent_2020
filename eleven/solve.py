import copy

def evaluate_cell_p1(grid, row, col):
  occupied = 0
  seat_value = grid[row][col]
  for row_diff in range(-1, 2):
    for col_diff in range(-1, 2):
      if row_diff == 0 and col_diff == 0:
        continue
      if row + row_diff < 0 or col + col_diff < 0:
        value = '.'
      else:
        try:
          value = grid[row + row_diff][col + col_diff]
        except IndexError:
          value = '.'
      if value == '#':
        occupied += 1
  if seat_value == 'L' and occupied == 0:
    return '#'
  if seat_value == '#' and occupied >= 4:
    return 'L'
  return seat_value

def evaluate_direction(grid, row, col, row_diff, col_diff):
  if row + row_diff < 0 or col + col_diff < 0:
    return '.'
  try:
    value = grid[row + row_diff][col + col_diff]
  except IndexError:
    return '.'
  if value != '.':
    return value
  return evaluate_direction(grid, row + row_diff, col + col_diff, row_diff, col_diff)

def evaluate_cell(grid, row, col):
  occupied = 0
  seat_value = grid[row][col]
  for row_diff in range(-1, 2):
    for col_diff in range(-1, 2):
      if row_diff == 0 and col_diff == 0:
        continue
      value = evaluate_direction(grid, row, col, row_diff, col_diff)
      if value == '#':
        occupied += 1
  if seat_value == 'L' and occupied == 0:
    return '#'
  if seat_value == '#' and occupied >= 5:
    return 'L'
  return seat_value

def hash_grid(grid):
  return '\n'.join(''.join(row) for row in grid)

def evaluate_grid(grid):
  new_grid = []
  for (rownum, row) in enumerate(grid):
    new_grid.append([
      evaluate_cell(grid, rownum, colnum)
      for (colnum, col) in enumerate(row)
    ])
  return new_grid


with open('input.txt', 'r') as f:
  problem_grid = [list(row.strip()) for row in f.readlines()]

prev_grid = problem_grid
iterations = 0
while True:
  next_grid = evaluate_grid(prev_grid)
  iterations += 1
  if hash_grid(prev_grid) == hash_grid(next_grid):
    break
  prev_grid = next_grid

total = 0
for row in prev_grid:
  total += sum(1 for seat in row if seat == '#')
print(total)
