import collections
import itertools


def evaluate_cell(cube, row, col, z):
  value = 0
  min_z = min(cube.keys())
  max_z = max(cube.keys())
  cell_status = cube[z][row][col]
  for z_diff, row_diff, col_diff in itertools.product(range(-1, 2), range(-1, 2), range(-1, 2)):
    if row_diff == 0 and col_diff == 0 and z_diff == 0:
      continue
    if row + row_diff < 0 or col + col_diff < 0 or z + z_diff < min_z or z + z_diff > max_z:
      continue
    try:
      neighbor_status = cube[z + z_diff][row + row_diff][col + col_diff]
    except IndexError:
      neighbor_status = '.'
    if neighbor_status == '#':
      value += 1
  if cell_status == '#':
    return '#' if value in [2, 3] else '.'
  if cell_status == '.':
    return '#' if value == 3 else '.'
  raise ValueError(f'Not a valid cell: {cell_status}')


def hash_cube(cube):
  return '\n'.join(f'z={z}\n{hash_grid(grid)}\n' for z, grid in cube.items())


def hash_grid(grid):
  return '\n'.join(''.join(row) for row in grid)


def evaluate_cube(cube):
  new_cube = make_empty_cube(len(cube[0]))
  for z, grid in cube.items():
    new_grid = []
    for (rownum, row) in enumerate(grid):
      new_grid.append([
          evaluate_cell(cube, rownum, colnum, z)
          for (colnum, col) in enumerate(row)
      ])
    new_cube[z] = new_grid
  return new_cube


def make_empty_cube(dimension):
  return {z: make_empty_grid(dimension) for z in range(-dimension, dimension + 1)}


def make_empty_grid(dimension):
  return [['.' for col in range(dimension)] for row in range(dimension)]


def count_active_in_cube(cube):
  total = 0
  for grid in cube.values():
    for row in grid:
      for col in row:
        if col == '#':
          total += 1
  return total


def inflate_grid(grid, buffer):
  size = (2 * buffer) + len(grid)
  result = [['.'] * size for row in range(buffer)]
  for row in grid:
    result.append((['.'] * buffer) + list(row) + (['.'] * buffer))
  for row in range(buffer):
    result.append(['.'] * size)
  return result


def solve(filename, iterations):
  with open(filename, 'r') as f:
    problem_grid = [list(row.strip()) for row in f.readlines()]

  problem_grid = inflate_grid(problem_grid, 6)
  print(problem_grid)

  problem_cube = make_empty_cube(len(problem_grid))
  problem_cube[0] = problem_grid

  cube = problem_cube
  print(hash_cube(cube))
  for i in range(iterations):
    cube = evaluate_cube(cube)
    print(f'==========iteration: {i + 1}==========')
    print(hash_cube(cube))
    print(count_active_in_cube(cube))
    # input('Press enter to continue.')
  return count_active_in_cube(cube)


# print(solve('dummy.txt', 6))
print(solve('input.txt', 6))
