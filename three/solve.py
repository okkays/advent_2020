import math


class Tile:
  def __init__(self, char):
    if char == '#':
      self.kind = 'tree'
    elif char == '.':
      self.kind = 'snow'
    else:
      raise ValueError(f'not a valid char: {char}')

  def hit(self):
    if self.kind == 'tree':
      return 'X'
    elif self.kind == 'snow':
      return 'O'
    return ''

  def __str__(self):
    if self.kind == 'tree':
      return '#'
    elif self.kind == 'snow':
      return '.'
    return ''


class Map:

  def __init__(self):
    with open('input.txt', 'r') as f:
      self.tiles = [[Tile(char) for char in line if char.strip()] for line in f.readlines()]
    self.x = 0
    self.y = 0
    self.row_length = len(self.tiles[0])

  def go_right(self, num):
    next_x = self.x + num
    if next_x >= self.row_length:
      self.x = next_x % self.row_length
      return
    self.x = next_x

  def go_down(self, num):
    self.y += num

  def get_tile(self):
    try:
      row = self.tiles[self.y]
    except IndexError:
      return None
    return row[self.x]

  def __str__(self):
    base = [[str(t) for t in row] for row in self.tiles]
    base[self.y][self.x] = self.tiles[self.y][self.x].hit()
    return '\n'.join(''.join(c for c in row) for row in base)


def count_trees(right, down):
  _map = Map()
  current = None
  num_trees = 0
  while True:
    _map.go_right(right)
    _map.go_down(down)
    current = _map.get_tile()
    if current is None:
      break
    if current.kind == 'tree':
      num_trees += 1
  return num_trees


to_count = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
print(math.prod(count_trees(*i) for i in to_count))
