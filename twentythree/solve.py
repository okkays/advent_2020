print('\n============\n')
import itertools

DUMMY = '389125467'
INPUT = '562893147'


class Cup(int):
  def __init__(self, value):
    self.left = None
    self.right = None

  def __iter__(self):
    yield self
    yield from self.right

  def set_right(self, new):
    # if self.right is not None:
    #   self.right.left = None
    self.right = new
    if new is not None:
      new.left = self

  def to_list(self):
    result = [self]
    for i in self.right:
      if i == self:
        break
      result.append(i)
    return result

  def __str__(self):
    result = [f' {repr(s)} ' for s in self.to_list()]
    result[0] = f'({result[0]})'
    return ' '.join(result)


def solve(raw):
  cups = [Cup(r) for r in list(raw)]
  prev_cup = cups[0]
  for cup in cups[1:]:
    prev_cup.set_right(cup)
    prev_cup = cup
  cups[-1].set_right(cups[0])

  cup = iter(cups[0])
  for i in range(100):
    print(f'\n-- move {i + 1} --')
    current = next(cup)
    print(str(current))
    cut_cup = iter(current.right)
    cut = [next(cut_cup) for _ in range(3)]
    print('pick up: ', cut)
    cut[0].left.set_right(cut[-1].right)
    target = current - 1
    if target < 1:
      target = 9
    while target in cut:
      target -= 1
      if target < 1:
        target = 9
    print('destination: ', target)
    dest = None
    dest_cup = iter(current)
    while dest != target:
      dest = next(dest_cup)
    cut[-1].set_right(dest.right)
    dest.set_right(cut[0])

  print(''.join(repr(c) for c in current.to_list()))


solve(INPUT)

print('done')

