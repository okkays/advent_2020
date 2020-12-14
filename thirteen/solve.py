import itertools
from functools import reduce
print()

with open('input.txt', 'r') as f:
  raw = [l.strip()for l in f.readlines()]
input_busses = [int(b) if b != 'x' else b for b in raw[1].split(',')]


def normalize(busses, start):
  return ((((start // b) + 1) * b) - start if b != 'x' else 'x' for b in busses)


def part1(busses):
  busses = [b for b in busses if b != 'x']
  start = int(raw[0])
  normalized_departures = list(normalize(busses, start))
  wait = min(normalized_departures)
  bus_id = busses[normalized_departures.index(wait)]
  print('part1', bus_id, wait, bus_id * wait)


part1(input_busses)

# https://rosettacode.org/wiki/Chinese_remainder_theorem#Python


def chinese_remainder(n, a):
  total = 0
  prod = reduce(lambda a, b: a*b, n)
  for n_i, a_i in zip(n, a):
    p = prod // n_i
    total += a_i * mul_inv(p, n_i) * p
  return total % prod


def mul_inv(a, b):
  b0 = b
  x0, x1 = 0, 1
  if b == 1:
    return 1
  while a > 1:
    q = a // b
    a, b = b, a % b
    x0, x1 = x1 - q * x0, x0
  if x1 < 0:
    x1 += b0
  return x1


def part2(busses):
  """Prints busses such that wolframalpha can take it as input.

  e.g.:
  (x mod 7 = 0), (x mod 13 = 1), (x mod 59 = 4), (x mod 31 = 6), (x mod 19 = 7)
  """
  goal = [i for i, b in enumerate(busses) if b != 'x']
  cleaned = [b for b in busses if b != 'x']
  answer = ', '.join([f'(x mod {c} = {g})' for c, g in zip(cleaned, goal)])
  r = chinese_remainder(cleaned, goal)
  p = reduce(lambda a, b: a * b, cleaned)
  return cleaned, goal, p - r


with open('solutions.txt', 'r') as f:
  raw = [l.strip() for l in f.readlines()]
  solutions = []
  for r in raw:
    raw_problem, raw_answer = r.split('=')
    answer = int(raw_answer)
    problem = [int(p) if p != 'x' else p for p in raw_problem.split(',')]
    solutions.append((problem, answer))

  for problem, answer in solutions:
    print(part2(problem), answer)

print(part2(input_busses))
