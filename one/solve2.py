import itertools
import functools

numbers = []
with open('input.txt') as infile:
  for raw in infile.readlines():
    try:
      numbers.append(int(raw.strip()))
    except:
      continue


def solve(goal, count_elements):
  for combination in itertools.combinations(numbers, count_elements):
    if sum(combination) == goal:
      product = functools.reduce(lambda a, b: a * b, combination)
      return sum(combination), combination, product


print(solve(2020, 2))
print(solve(2020, 3))
