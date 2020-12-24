def read(filename):
  with open(filename, 'r') as f:
    raw = f.read()
  p1, p2 = raw.strip().split('\n\n')
  p1 = [int(c) for c in p1.split('\n')[1:]]
  p2 = [int(c) for c in p2.split('\n')[1:]]
  return p1, p2


def score(p1, p2):
  winner = p1 if p1 else p2
  return sum((i + 1) * card for i, card in enumerate(reversed(winner)))


def solve(filename):
  p1, p2 = read(filename)
  print(p1, p2)
  rounds = 0
  while p1 and p2:
    rounds += 1
    c1 = p1.pop(0)
    c2 = p2.pop(0)
    if c1 > c2:
      p1.extend([c1, c2])
    else:
      p2.extend([c2, c1])
  print(rounds, p1, p2)
  print(score(p1, p2))


solve('input.txt')
