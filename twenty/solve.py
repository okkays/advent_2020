import collections
import itertools
import functools
import numpy
import re
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
  def image(self):
    return [row[1:-1] for row in self.grid[1:-1]]

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

  def clone(self):
    new = Tile(self.num, list(self.grid))
    new.nodes = self.nodes
    return new

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
  joined_grid = list(zip(*[tile.image for tile in row]))
  result = []
  for joined_row in joined_grid:
    result.append(''.join(joined_row))
  return '\n'.join(result)


def place(tiles):
  solved = [tiles.pop()]
  left_tiles = tiles
  right_tiles = []
  while left_tiles or right_tiles:
    while left_tiles:
      other_tile = left_tiles.pop()
      max_tile = None
      max_matches = 0
      max_solved = []
      for orients in itertools.product(range(4), range(2), range(2)):
        matches = 0
        oriented = other_tile.orient(*orients)
        solved_clone = [s.clone() for s in solved]
        for solved_tile in solved_clone:
          matches += int(solved_tile.try_match_fixed(oriented))
        if matches > max_matches:
          max_tile = oriented
          max_matches = matches
          max_solved = solved_clone
      if not max_matches:
        right_tiles.append(other_tile)
      else:
        solved = max_solved
        solved.append(max_tile)
    left_tiles, right_tiles = right_tiles, left_tiles

  # Clean up references
  tiles = {}
  for s in solved:
    tiles[s.num] = s
  for s in solved:
    for direction, node in s.nodes.items():
      if not node:
        continue
      s[direction] = tiles[node.num]
  return solved


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

  borders = collections.defaultdict(lambda: 0)
  for tile in tiles:
    for border in tile.borders.values():
      borders[border] += 1

  print('border match counts', set(borders.values()))

  print('num tiles', len(tiles))
  solved = place(tiles)
  for s in solved:
    print(s.nodes)

  corners = [tile for tile in solved if tile.is_corner]
  c_nums = [c.num for c in corners]
  print('SOLVED:')
  print(''.join([str(s) for s in solved]))
  print('CORNERS:')
  print(''.join([str(s) for s in corners]))
  print('part1', functools.reduce(lambda a, b: a * b, c_nums))
  return corners


def find_indexes(regexes, grid):
  rowspan = len(regexes)
  num_monsters = 0
  for row_index in range(len(grid) - (rowspan - 1)):
    rows = grid[row_index:row_index + rowspan]
    matches = [{r.start(1) for r in regex.finditer(row)}
               for regex, row in zip(regexes, rows)]
    monsters = set.intersection(*matches)
    # print('monster: ', row_index, matches, monsters)
    num_monsters += len(monsters)
  return num_monsters


def solve2(corners, monster):
  leftmost = next(tile for tile in corners if tile.is_northwest)
  grid = leftmost.get_full()
  joined = [join_row(row) for row in grid]
  image = '\n'.join(joined)
  print(image)
  regexes = []
  for line in monster:
    regex = line.replace(' ', '.')
    regexes.append(re.compile(f'(?=({regex}))'))
  sea = image.split('\n')
  for rotate, fliph, flipv in itertools.product(range(4), range(2), range(2)):
    sea_copy = list(list(s) for s in sea)
    sea_copy = numpy.rot90(sea_copy, rotate)
    if fliph:
      sea_copy = numpy.fliplr(sea_copy)
    if flipv:
      sea_copy = numpy.flipud(sea_copy)
    sea_copy = [''.join(s) for s in sea_copy]
    monsters = find_indexes(regexes, sea_copy)
    if monsters:
      break

  num_per_monster = sum(1 for c in ''.join(monster) if c == '#')
  num_in_sea = sum(1 for c in ''.join(sea) if c == '#')
  print(num_per_monster, monsters, num_in_sea - (monsters * num_per_monster))


corners = solve('input.txt')
monster = [
    "                  # ",
    "#    ##    ##    ###",
    " #  #  #  #  #  #   ",


]
solve2(corners, monster)
print('done')
