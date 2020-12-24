print('\n============\n')
import itertools
import sys

DUMMY = '389125467'
INPUT = '562893147'


class Cup(int):
  def __init__(self, value):
    self.left = None
    self.right = None

  def set_right(self, new):
    self.right = new
    if new is not None:
      new.left = self

  def to_list(self):
    result = [self]
    current = self.right
    while current != self:
      result.append(current)
      current = current.right
    return result

  def __str__(self):
    result = [f' {repr(s)} ' for s in self.to_list()]
    result[0] = f'({result[0]})'
    return ' '.join(result)


def solve(raw, num_rounds=100, num_cups=10):
  cups = [Cup(r) for r in list(raw)] + [Cup(i) for i in range(10, num_cups)]
  cups_by_value = {int(c): c for c in cups}
  prev_cup = cups[0]
  for cup in cups[1:]:
    prev_cup.set_right(cup)
    prev_cup = cup
  cups[-1].set_right(cups[0])

  current = cups[0]
  for i in range(num_rounds):
    cut = [current.right, current.right.right, current.right.right.right]
    cut[0].left.set_right(cut[-1].right)
    target = current - 1
    if target < 1:
      target = num_cups - 1
    while target in cut:
      target -= 1
      if target < 1:
        target = num_cups - 1
    dest = cups_by_value[target]
    cut[-1].set_right(dest.right)
    dest.set_right(cut[0])
    current = current.right

  current = cups_by_value[1]
  one = int(current.right)
  two = int(current.right.right)
  print(one, two, one * two)


# solve(DUMMY)
# import cProfile
# cProfile.run('solve(DUMMY, num_rounds=10000000, num_cups=1000001)')
solve(INPUT, num_rounds=10000000, num_cups=1000001)

print('done')

