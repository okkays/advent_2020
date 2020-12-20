print()
print('============')

BORDERS = {
  'north': 0,
  'east': 1,
  'south': 2,
  'west': 3,
}

class Tile:
  def rotate(self):
    self.rotation = (self.rotation + 1) % 4

  def flip(self):
    self.flipped = not self.flipped

  @property
  def offset(self):
    return (self.flipped * 2) + self.rotation

  def __setitem__(self, direction, node):
    pass

  def __getitem__(self, direction):
    return self.borders[BORDERS[direction] + self.offset]

  def __init__(self, raw):
    lines = [l for l in raw.strip().split('\n') if l]
    self.flipped = False
    self.rotation = 0
    self.num = int(lines[0].strip(':').split(' ')[1])
    self.grid = lines[1:]
    self.borders = {
      BORDERS['north']: lines[1],
      BORDERS['east']: ''.join([r[-1] for r in lines[1:]]),
      BORDERS['south']: lines[-1],
      BORDERS['west']: ''.join([r[0] for r in lines[1:]]),
    }
    self._north = None
    self._east = None
    self._south = None
    self._west = None

  def __str__(self):
    grid = "\n".join(self.grid)
    borders = "\n".join(self.borders.values())
    return f'Tile {self.num}:\n{borders}'


def solve(filename):
  with open(filename, 'r') as f:
    raw = f.read()
  raw_tiles = raw.split('\n\n')
  tiles = [Tile(raw_tile) for raw_tile in raw_tiles]
  tile = next(filter(lambda t: t.num == 3079, tiles))
  print(tile)
  print('===')
  print(tile['north'])
  tile.rotate()
  print(tile['north'])
  tile.rotate()
  print(tile['north'])
  tile.rotate()
  print(tile['north'])
  tile.rotate()
  # print('\n\n'.join(str(t) for t in tiles))

solve('dummy.txt')
