import cProfile
import collections
print()

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
  return list(sorted(direction))


def remove_duplicates(directions):
  counts = collections.defaultdict(lambda: 0)
  for direction in directions:
    counts[tuple(direction)] += 1
  return [list(d) for d, count in counts.items() if count % 2 != 0]


def get_adjacents(direction):
  return [reduce(direction + [c]) for c in compass]


def should_be_black(direction, black_tiles):
  black_tiles = {tuple(b) for b in black_tiles}
  neighbors = get_adjacents(direction)
  black_neighbors = sum(1 for n in neighbors if tuple(n) in black_tiles)
  is_black = tuple(direction) in black_tiles
  if is_black:
    return not (black_neighbors == 0 or black_neighbors > 2)
  return black_neighbors == 2


def step(black_tiles):
  to_check = []
  for black in black_tiles:
    to_check.extend(get_adjacents(black))
  reduced = {tuple(reduce(d)) for d in to_check}
  reduced = [list(d) for d in reduced]
  stepped = [d for d in reduced if should_be_black(d, black_tiles)]
  deduped = remove_duplicates(stepped)
  return deduped


def solve(filename):
  directions = read_directions(filename)
  reduced = [reduce(direction) for direction in directions]
  unique_reduced = remove_duplicates(reduced)
  print('part1: ', len(unique_reduced))
  directions = unique_reduced
  for i in range(100):
    directions = step(directions)
    print(i, len(directions))


# solve('dummy.txt')
solve('input.txt')
# cProfile.run("solve('dummy.txt')")
print('done')
