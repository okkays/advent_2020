import collections

compass = ['e', 'se', 'sw', 'w', 'nw', 'ne']
reductions = [
    (['e', 'w'], []),
    (['se', 'nw'], []),
    (['sw', 'ne'], []),
    (['ne', 'se'], ['e']),
    (['nw', 'sw'], ['w']),
    (['e', 'nw'], ['ne']),
    (['w', 'ne'], ['nw']),
    (['e', 'sw'], ['se']),
    (['w', 'se'], ['sw']),
]


def read_directions(filename):
  to_flip = []
  current_row = []
  with open(filename, 'r') as f:
    while True:
      c = f.read(1)
      if c == '':
        break
      if c == '\n':
        to_flip.append(current_row)
        current_row = []
        continue
      if c in ['s', 'n']:
        c += f.read(1)
      current_row.append(c)
  return to_flip


def reduce(direction):
  while True:
    changed = False
    for condition, replacement in reductions:
      if not all(c in direction for c in condition):
        continue
      for c in condition:
        direction.remove(c)
      direction.extend(replacement)
      changed = True
    if not changed:
      break
  return tuple(sorted(direction))


def remove_duplicates(directions):
  counts = collections.defaultdict(lambda: 0)
  for direction in directions:
    counts[direction] += 1
  return {direction for direction, count in counts.items() if count % 2 != 0}


def get_adjacents(direction):
  return [reduce(direction + [c]) for c in compass]


def should_flip(direction, black_tiles):
  neighbors = get_adjacents(direction)
  black_neighbors = sum(1 for n in neighbors if n in black_tiles)
  is_black = direction in black_tiles
  if is_black and black_neighbors == 0 or black_neighbors > 2:
    return True
  if not is_black and black_neighbors == 2:
    return True
  return False


def step(directions):
  reduced = [reduce(direction) for direction in directions]
  unique_reduced = remove_duplicates(reduced)
  print(len(reduced), len(unique_reduced))


def solve(filename):
  directions = read_directions(filename)
  # print(directions)
  step(directions)


solve('input.txt')
