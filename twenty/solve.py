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
  def try_match(self, other_tile):
    for _ in BORDERS:
      for _ in range(2):
        for _ in range(2):
          if self.try_match_fixed(other_tile):
            return True
          self.flip_v()
        self.flip_h()
      self.rotate()
    return False

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

  @property
  def offset(self):
    return self.rotation

  @property
  def is_complete(self):
    return all(self.nodes.values())

  @property
  def is_corner(self):
    north = bool(self.nodes[BORDERS['north']])
    east = bool(self.nodes[BORDERS['east']])
    south = bool(self.nodes[BORDERS['south']])
    west = bool(self.nodes[BORDERS['west']])
    result = ((north and east) ^
            (east and south) ^
            (south and west) ^
            (north and west))
    return result


  def __setitem__(self, direction, node):
    if isinstance(direction, str):
      raise ValueError('use int')
    self.nodes[(direction + self.offset) % 4] = node

  def __getitem__(self, direction):
    if isinstance(direction, str):
      raise ValueError('use int')
    num = (direction + self.offset) % 4
    border = self.borders[num]
    if num in [BORDERS['north'], BORDERS['south']] and self.flipped_h:
      return ''.join(reversed(border))
    if num in [BORDERS['east'], BORDERS['west']] and self.flipped_v:
      return ''.join(reversed(border))
    return border

  def get_node(self, direction):
    if isinstance(direction, str):
      raise ValueError('use int')
    num = direction + self.offset
    if num in [BORDERS['north'], BORDERS['south']] and self.flipped_v:
      num += 2
    if num in [BORDERS['east'], BORDERS['west']] and self.flipped_h:
      num += 2
    return self.nodes[num % 4]

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
    north = self.nodes[BORDERS['north']]
    north_num = north.num if north else '    '
    south = self.nodes[BORDERS['south']]
    south_num = south.num if south else '    '
    east = self.nodes[BORDERS['east']]
    east_num = east.num if east else '    '
    west = self.nodes[BORDERS['west']]
    west_num = west.num if west else '    '
    this = self.num
    return (f'{this}:\n'
            f'    {north_num}    \n'
            f'{west_num}    {east_num}\n'
            f'    {south_num}    \n')


def solve(filename):
  with open(filename, 'r') as f:
    raw = f.read()
  raw_tiles = raw.split('\n\n')
  tiles = [Tile(raw_tile) for raw_tile in raw_tiles]

  solved = [tiles.pop()]
  found = False
  left_tiles = tiles
  right_tiles = []
  while left_tiles or right_tiles:
    while left_tiles:
      other_tile = left_tiles.pop()
      for solved_tile in solved:
        if solved_tile.try_match(other_tile):
          found = True
      if not found:
        right_tiles.append(other_tile)
      else:
        solved.append(other_tile)
    left_tiles, right_tiles = right_tiles, left_tiles

  corners = [tile.num for tile in solved if tile.is_corner]
  print(functools.reduce(lambda a, b: a * b, corners))

  print('done')

solve('input.txt')
