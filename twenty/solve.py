import itertools
import functools
import numpy
print()
print('============')

BORDERS = {
    'north': 0,
    'east': 1,
    'south': 2,
    'west': 3,
}


class Tile:
  def orient(self, rotate, flip_v, flip_h):
    array = [list(row) for row in self.grid]
    if flip_v:
      array = numpy.flipud(array)
    if flip_h:
      array = numpy.fliplr(array)
    array = numpy.rot90(array, rotate)
    return Tile(self.num, [''.join(row) for row in array])

  def try_match_fixed(self, other_tile):
    for this_border in BORDERS.values():
      other_border = (this_border + 2) % 4
      if self[this_border] != other_tile[other_border]:
        continue
      self[this_border] = other_tile
      other_tile[other_border] = self
      return True
    return False

  def get_full(self):
    grid = []
    leftmost = self
    while leftmost is not None:
      row = leftmost.get_row()
      grid.append(row)
      leftmost = leftmost.nodes[BORDERS['south']]
    return grid

  def get_row(self):
    row = []
    node = self
    while node is not None:
      row.append(node)
      node = node.nodes[BORDERS['east']]
    return row

  @property
  def is_complete(self):
    return all(self.nodes.values())

  @property
  def is_corner(self):
    north = bool(self.nodes[BORDERS['north']])
    south = bool(self.nodes[BORDERS['south']])
    east = bool(self.nodes[BORDERS['east']])
    west = bool(self.nodes[BORDERS['west']])
    result = ((north and east) ^
              (east and south) ^
              (south and west) ^
              (north and west))
    return result

  @property
  def is_northwest(self):
    north = bool(self.nodes[BORDERS['north']])
    south = bool(self.nodes[BORDERS['south']])
    east = bool(self.nodes[BORDERS['east']])
    west = bool(self.nodes[BORDERS['west']])
    return east and south and not west and not north

  def __setitem__(self, direction, node):
    if isinstance(direction, str):
      raise ValueError('use int')
    self.nodes[direction] = node

  def __getitem__(self, direction):
    if isinstance(direction, str):
      raise ValueError('use int')
    border = self.borders[direction]
    return border

  def __init__(self, num, grid):
    self.num = num
    self.grid = grid

    self.borders = {
        BORDERS['north']: grid[0],
        BORDERS['east']: ''.join([r[-1] for r in grid]),
        BORDERS['south']: grid[-1],
        BORDERS['west']: ''.join([r[0] for r in grid]),
    }

    self.nodes = {
        BORDERS['north']: None,
        BORDERS['east']: None,
        BORDERS['south']: None,
        BORDERS['west']: None,
    }

  def __repr__(self):
    return f'<{self.num}>'

  def __str__(self):
    north = self.nodes[BORDERS['north']]
    north_num = north.num if north else '    '
    south = self.nodes[BORDERS['south']]
    south_num = south.num if south else '    '
    east = self.nodes[BORDERS['east']]
    east_num = east.num if east else '    '
    west = self.nodes[BORDERS['west']]
    west_num = west.num if west else '    '
    return (f'     {north_num}    \n'
            f'{west_num} {self.num} {east_num}\n'
            f'     {south_num}    \n')


def join_row(row):
  joined_grid = list(zip(*[tile.grid for tile in row]))
  result = []
  for joined_row in joined_grid:
    result.append(' '.join(joined_row))
  return '\n'.join(result)


def solve(filename):
  with open(filename, 'r') as f:
    raw = f.read()
  raw_tiles = raw.split('\n\n')
  tiles = []
  for raw_tile in raw_tiles:
    lines = [l for l in raw_tile.strip().split('\n') if l]
    num = int(lines[0].strip(':').split(' ')[1])
    grid = lines[1:]
    tiles.append(Tile(num, grid))

  solved = [tiles.pop()]
  left_tiles = tiles
  right_tiles = []
  while left_tiles or right_tiles:
    while left_tiles:
      other_tile = left_tiles.pop()
      max_tile = None
      max_matches = 0
      for orients in itertools.product(range(4), range(2), range(2)):
        matches = 0
        oriented = other_tile.orient(*orients)
        for solved_tile in solved:
          matches += int(solved_tile.try_match_fixed(oriented))
        if matches > max_matches:
          max_tile = oriented
          max_matches = matches
      if not max_matches:
        right_tiles.append(other_tile)
      else:
        solved.append(max_tile)
    left_tiles, right_tiles = right_tiles, left_tiles

  corners = [tile.num for tile in solved if tile.is_corner]
  print(''.join([str(s) for s in solved]))
  print('part1', functools.reduce(lambda a, b: a * b, corners))

  leftmost = next(tile for tile in solved if tile.is_northwest)
  grid = leftmost.get_full()
  for row in grid:
    print(''.join([str(c) for c in row]))
    print(row)
  image = '\n\n'.join([join_row(row) for row in grid])
  print(image)

  print('done')


solve('input.txt')
