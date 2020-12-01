GOAL = 2020
solutions = dict()

with open('input.txt') as infile:
  for raw in infile.readlines():
    try:
      number = int(raw.strip())
    except:
      continue
    solutions[number] = GOAL - number

for left, right in solutions.items():
  if right in solutions:
    print(left, right, left * right)
    break
