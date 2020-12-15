import collections
print()
with open('input.txt', 'r') as f:
  problems = [l.strip().split(',') for l in f.readlines()]
  problems = [[int(p) for p in problem] for problem in problems]


def p1(problem, iterations=2020):
  ages = collections.defaultdict(list)
  for i, p in enumerate(problem):
    ages[p].append(i)
  last_spoken = problem[-1]

  for age in range(len(problem), iterations):
    if len(ages[last_spoken]) == 1:
      last_spoken = 0
    else:
      last_spoken = ages[last_spoken][-1] - ages[last_spoken][-2]
    ages[last_spoken].append(age)
  return last_spoken


print(p1(problems[0], 10))
print('part1', [p1(problem, 2020) for problem in problems])
# print('part2', p1([3, 2, 1], 30000000))
