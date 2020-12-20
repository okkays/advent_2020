import itertools
import functools
print()
print('============')

BORDERS = {
  'north': 0,
  'east': 1,
  'south': 2,
  'west': 3,
}

class Tile:
  def orient(self, rotation, flipped_h, flipped_v):
    self.rotation = rotation
    self.flipped_h = bool(flipped_h)
    self.flipped_v = bool(flipped_v)

  def try_match_fixed(self, other_tile):
    for this_border in BORDERS.values():
      other_border = (this_border + 2) % 4
      if self[this_border] != other_tile[other_border]:
        continue
      self[this_border] = other_tile
      other_tile[other_border] = self
      return True
    return False

  def rotate(self):
    self.rotation = (self.rotation + 1) % 4

  def flip_h(self):
    self.flipped_h = not self.flipped_h

  def flip_v(self):
    self.flipped_v = not self.flipped_v

  def to_image(self):
    grid = list(self.grid)
    if self.flipped_v:
      grid = grid[::-1]
    if self.flipped_h:
      grid = [''.join(reversed(row)) for row in grid]
    return grid

  def get_full(self):
    grid = []
    leftmost = self
    while leftmost is not None:
      row = leftmost.get_row()
      rows.append(leftmost)
      leftmost = leftmost.get_node(BORDERS['south'])

  def get_row(self):
    row = [self]
    node = self
    while node is not None:
      node = node.get_node(BORDERS['east'])
      row.append(node)
    return row

  @property
  def is_complete(self):
    return all(self.nodes.values())

  @property
  def is_corner(self):
    north = bool(self.get_node(BORDERS['north']))
    south = bool(self.get_node(BORDERS['south']))
    east = bool(self.get_node(BORDERS['east']))
    west = bool(self.get_node(BORDERS['west']))
    result = ((north and east) ^
            (east and south) ^
            (south and west) ^
            (north and west))
    return result

  @property
  def is_northwest(self):
    north = bool(self.get_node(BORDERS['north']))
    south = bool(self.get_node(BORDERS['south']))
    east = bool(self.get_node(BORDERS['east']))
    west = bool(self.get_node(BORDERS['west']))
    return east and south and not west and not north

  def __setitem__(self, direction, node):
    if isinstance(direction, str):
      raise ValueError('use int')
    self.nodes[(direction + self.rotation) % 4] = node

  def __getitem__(self, direction):
    if isinstance(direction, str):
      raise ValueError('use int')
    num = (direction + self.rotation) % 4
    border = self.borders[num]
    if num in [BORDERS['north'], BORDERS['south']] and self.flipped_v:
      return ''.join(reversed(border))
    if num in [BORDERS['east'], BORDERS['west']] and self.flipped_h:
      return ''.join(reversed(border))
    return border

  def get_node(self, direction):
    if self.flipped_v:
      if direction == BORDERS['east']:
        direction = BORDERS['west']
      elif direction == BORDERS['west']:
        direction = BORDERS['east']
    return self.nodes[(direction + self.rotation) % 4]

  def __init__(self, raw):
    lines = [l for l in raw.strip().split('\n') if l]
    self.flipped_h = False
    self.flipped_v = False
    self.rotation = 0
    self.num = int(lines[0].strip(':').split(' ')[1])
    self.grid = lines[1:]

    self.borders = {
      BORDERS['north']: lines[1],
      BORDERS['east']: ''.join([r[-1] for r in lines[1:]]),
      BORDERS['south']: lines[-1],
      BORDERS['west']: ''.join([r[0] for r in lines[1:]]),
    }

    self.nodes = {
      BORDERS['north']: None,
      BORDERS['east']: None,
      BORDERS['south']: None,
      BORDERS['west']: None,
    }

  def __str__(self):
    north = self.get_node(BORDERS['north'])
    north_num = north.num if north else '    '
    south = self.get_node(BORDERS['south'])
    south_num = south.num if south else '    '
    east = self.get_node(BORDERS['east'])
    east_num = east.num if east else '    '
    west = self.get_node(BORDERS['west'])
    west_num = west.num if west else '    '
    this = self.num
    return (f'(h: {self.flipped_h}, v: {self.flipped_v}, r: {self.rotation}):\n'
            f'     {north_num}    \n'
            f'{west_num} {self.num} {east_num}\n'
            f'     {south_num}    \n')


def join_image(northwest):
  pass


def solve(filename):
  with open(filename, 'r') as f:
    raw = f.read()
  raw_tiles = raw.split('\n\n')
  tiles = [Tile(raw_tile) for raw_tile in raw_tiles]

  solved = [tiles.pop()]
  left_tiles = tiles
  right_tiles = []
  while left_tiles or right_tiles:
    while left_tiles:
      other_tile = left_tiles.pop()
      matches_to_orients = {}
      for orients in itertools.product(range(4), range(2), range(2)):
        matches = 0
        other_tile.orient(*orients)
        for solved_tile in solved:
          matches += int(solved_tile.try_match_fixed(other_tile))
        if matches:
          matches_to_orients[matches] = orients
      if not matches_to_orients:
        right_tiles.append(other_tile)
      else:
        other_tile.orient(*matches_to_orients[max(matches_to_orients)])
        solved.append(other_tile)
    left_tiles, right_tiles = right_tiles, left_tiles

  corners = [tile.num for tile in solved if tile.is_corner]
  print('part1', functools.reduce(lambda a, b: a * b, corners))

  print('\n'.join([str(s) for s in solved]))
  # leftmost = next(tile for tile in solved if tile.is_northwest)
  # rows = []
  # print(leftmost)

  # top_row = leftmost.get_row()
  # print(top_row)
  # print([n.to_image() for n in top_row])
  # print('\n'.join(leftmost.to_image()))

  print('done')

solve('dummy.txt')
