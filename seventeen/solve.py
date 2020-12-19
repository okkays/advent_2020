import copy
import itertools


def evaluate_cell(cube, cell_status, active_cells, *dims):
  value = 0
  maxs = []
  mins = []
  layer = cube
  while not isinstance(layer, bool):
    try:
      mins.insert(0, min(layer.keys()))
      maxs.insert(0, max(layer.keys()))
      layer = layer[0]
    except AttributeError:
      mins.insert(0, 0)
      maxs.insert(0, None)
      layer = layer[0]
  for diffs in itertools.product(*[range(-1, 2) for _ in dims]):
    if all(d == 0 for d in diffs):
      continue
    if any(c + d < m for c, m, d in zip(dims, mins, diffs)):
      continue
    if any(m is not None and c + d > m for c, m, d in zip(dims, maxs, diffs)):
      continue
    try:
      neighbor_status = tuple(dim + diff for dim, diff in zip(dims, diffs)) in active_cells
    except IndexError:
      neighbor_status = False
    if neighbor_status:
      value += 1
  if cell_status:
    return value in [2, 3]
  if not cell_status:
    return value == 3
  raise ValueError(f'Not a valid cell: {cell_status}')


def hash_cube(cube):
  return '\n'.join(f'z={z}\n{hash_grid(grid)}\n' for z, grid in cube.items())


def hash_grid(grid):
  return '\n'.join(''.join(row) for row in grid)


def evaluate_cube(cube, active_cells, depth):
  new_cube = cube
  new_active_cells = []
  to_check = set(active_cells)
  for dims in active_cells:
    for diffs in itertools.product(*[range(-1, 2) for _ in dims]):
      to_check.add(tuple(dim + diff for dim, diff in zip(dims, diffs)))
  for cell in to_check:
    new_row = new_cube
    for dim in reversed(cell[1:]):
      new_row = new_row[dim]
    cell_status = cell in active_cells
    value = evaluate_cell(cube, cell_status, active_cells, *cell)
    new_row[cell[0]] = value
    if value:
      new_active_cells.append(cell)
  return new_cube, new_active_cells


def make_empty_cube(dimension):
  return {d: make_empty_grid(dimension) for d in range(-dimension, dimension + 1)}


def make_empty_hcube(dimension):
  return {d: make_empty_cube(dimension) for d in range(-dimension, dimension + 1)}


def make_empty_grid(dimension):
  return [[False for col in range(dimension)] for row in range(dimension)]


def inflate_grid(grid, buffer):
  size = (2 * buffer) + len(grid)
  result = [[False] * size for row in range(buffer)]
  for row in grid:
    result.append(([False] * buffer) + list(row) + ([False] * buffer))
  for row in range(buffer):
    result.append([False] * size)
  return result


def solve(filename, iterations, depth):
  with open(filename, 'r') as f:
    problem_grid = [[c == '#' for c in row.strip()] for row in f.readlines()]

  problem_grid = inflate_grid(problem_grid, 6)

  problem_cube = make_empty_hcube(len(problem_grid))
  problem_cube[0][0] = problem_grid
  active_cells = []
  for y, row in enumerate(problem_grid):
    for x, cell in enumerate(row):
      if cell:
        active_cells.append((x, y, *[0 for i in range(depth)]))

  cube = problem_cube
  for i in range(iterations):
    cube, active_cells = evaluate_cube(cube, active_cells, depth)
    print(f'==========iteration: {i + 1}==========')
    # print(hash_cube(cube))
    print(len(active_cells))
  return len(active_cells)


# print(solve('dummy.txt', 6, 2))
print(solve('input.txt', 6, 2))
