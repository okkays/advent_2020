import itertools


def evaluate_cell(cube, cell_status, *dims):
  value = 0
  maxs = []
  mins = []
  layer = cube
  while not isinstance(layer, str):
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
      neighbor_status = cube
      for dim, diff in zip(reversed(dims), reversed(diffs)):
        neighbor_status = neighbor_status[dim + diff]
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


def evaluate_cube(cube, active_cells):
  new_cube = make_empty_cube(len(cube[0]))
  new_active_cells = []
  to_check = set(active_cells)
  for dims in active_cells:
    for diffs in itertools.product(*[range(-1, 2) for _ in dims]):
      to_check.add(tuple(dim + diff for dim, diff in zip(dims, diffs)))
  for cell in to_check:
    row = cube
    new_row = new_cube
    for dim in reversed(cell[1:]):
      new_row = new_row[dim]
      row = row[dim]
    cell_status = row[cell[0]]
    value = evaluate_cell(cube, cell_status, *cell)
    new_row[cell[0]] = value
    if value == '#':
      new_active_cells.append(cell)
  return new_cube, new_active_cells


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

  problem_cube = make_empty_cube(len(problem_grid))
  problem_cube[0] = problem_grid
  active_cells = []
  for y, row in enumerate(problem_grid):
    for x, cell in enumerate(row):
      if cell == '#':
        active_cells.append((x, y, 0))

  cube = problem_cube
  for i in range(iterations):
    cube, active_cells = evaluate_cube(cube, active_cells)
    print(f'==========iteration: {i + 1}==========')
    # print(hash_cube(cube))
    print(len(active_cells))
  return len(active_cells)


print(solve('dummy.txt', 6))
# print(solve('input.txt', 6))
