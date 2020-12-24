import collections
import itertools
import re

inputmatcher = re.compile(r'^([\w\s]+)\(contains ([\w\s,]+)\)$')


def readinput(filename):
  with open(filename, 'r') as f:
    raw = [l.strip() for l in f.readlines()]
  pairs = []
  for line in raw:
    match = inputmatcher.fullmatch(line)
    ingredients = match[1].strip()
    allergens = match[2].strip()
    pairs.append((set(ingredients.split(' ')), set(allergens.split(', '))))
  return pairs


def reduce(pairs):
  reduced = {}
  for ingredients, allergens in pairs:
    for allergen in allergens:
      if not reduced.get(allergen):
        reduced[allergen] = set(ingredients)
      else:
        reduced[allergen] = reduced[allergen] & ingredients
  return reduced


def solve(filename):
  pairs = readinput(filename)
  pairs.sort(key=lambda p: -len(p[1]))
  all_ingredients = set.union(*[p[0] for p in pairs])
  reduced = list(reduce(pairs).items())
  solution = {}
  while reduced:
    reduced.sort(key=lambda p: len(p[1]))
    next_reduced = []
    allergen, ingredients = reduced.pop(0)
    solution[allergen] = ingredients
    for other_allergen, other_ingredients in reduced:
      next_reduced.append((other_allergen, other_ingredients - ingredients))
    reduced = next_reduced
  solution = list(sorted(solution.items(), key=lambda i: i[0]))
  solution = [s[1].pop() for s in solution]
  print('solution', ','.join(solution))


solve('input.txt')
