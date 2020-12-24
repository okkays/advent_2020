def read(filename):
  with open(filename, 'r') as f:
    raw = f.read()
  p1, p2 = raw.strip().split('\n\n')
  p1 = [int(c) for c in p1.split('\n')[1:]]
  p2 = [int(c) for c in p2.split('\n')[1:]]
  return p1, p2


def get_score(p1, p2):
  winner = p1 if p1 else p2
  w = 'p1' if p1 else 'p2'
  return w, sum((i + 1) * card for i, card in enumerate(reversed(winner)))


def combat(p1, p2):
  history = set()
  while p1 and p2:
    # Check for recursion break.
    turn_key = ','.join(str(p) for p in p1) + '|' + ','.join(str(p) for p in p2)
    if turn_key in history:
      p2 = []
      break
    history.add(turn_key)

    # Draw
    c1 = p1.pop(0)
    c2 = p2.pop(0)

    # Maybe recurse
    if c1 <= len(p1) and c2 <= len(p2):
      winner, _ = combat(p1[:c1], p2[:c2])
      if winner == 'p1':
        p1.extend([c1, c2])
      else:
        p2.extend([c2, c1])
      continue

    # Normal mode
    if c1 > c2:
      p1.extend([c1, c2])
    else:
      p2.extend([c2, c1])
  winner, score = get_score(p1, p2)
  return winner, score


def solve(filename):
  p1, p2 = read(filename)
  print(p1, p2)
  winner, score = combat(p1, p2)
  print(winner, score)


solve('input.txt')
