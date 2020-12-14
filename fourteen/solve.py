print()

import types

class Mask:
  def __init__(self, mask):
    self.mask = mask

  def apply(self, value):
    binary = format(value, '036b')
    result = 0
    for i, pair in enumerate(zip(reversed(self.mask), reversed(binary))):
      m, b = pair
      if m == '0':
        continue
      if m == '1' or b == '1':
        result += 2**i
    return result


assert Mask('XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X').apply(11) == 73


class Parser:
  def __init__(self, filename):
    self.filename = filename
    self.mask = None
    self.mem = {}

  def __enter__(self):
    self.file = open(self.filename, 'r')
    return self

  def __exit__(self, *args):
    self.file.close()

  def step(self):
    raw = self.file.readline().strip()
    if raw == '':
      raise StopIteration()
    dest, value = raw.split(' = ')
    if dest == 'mask':
      self.mask = Mask(value)
      return
    if dest.startswith('mem'):
      addr = int(dest[4:-1])
      self.mem[addr] = self.mask.apply(int(value))
      # print(f'Set {addr} to {self.mem[addr]}')

  def sum_mem(self):
    return sum(self.mem.values())

  def run(self):
    while True:
      try:
        self.step()
      except StopIteration:
        return


with Parser('dummy.txt') as p:
  p.run()


print(p.sum_mem())

