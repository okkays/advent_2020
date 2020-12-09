import itertools

with open('input.txt', 'r') as f:
  puzzle = [int(l) for l in f.readlines()]


def checksum(source, goal, count_elements):
  for combination in itertools.combinations(source, count_elements):
    if sum(combination) == goal:
      return True
  return False


def find_invalid(source, index, preamble_size):
  while index < len(source):
    preamble = source[index - preamble_size:index]
    if not checksum(preamble, source[index], 2):
      return source[index]
    index += 1
  return None


def find_contig(source, goal):
  for low_index, low in enumerate(source):
    total = low
    high_index = low_index + 1
    lowest = float("inf")
    highest = 0
    while total < goal:
      high = source[high_index]
      lowest = min(low, lowest)
      highest = max(high, highest)
      total += high
      if total == goal:
        return lowest + highest
      high_index += 1


preamble_size = 25
index = preamble_size
part1 = find_invalid(puzzle, index, preamble_size)
print('part1', part1)
print('part2', find_contig(puzzle, part1))
