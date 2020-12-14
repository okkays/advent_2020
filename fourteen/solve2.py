import types
print()


class Mask:
  def __init__(self, mask):
    self.mask = mask

  def apply(self, value):
    binary = format(value, '036b')
    base_parts = []
    for i, pair in enumerate(zip(reversed(self.mask), reversed(binary))):
      m, b = pair
      if m == '0':
        base_parts.append(b)
        continue
      base_parts.append(m)

    base = ''.join(base_parts)
    num_floats = sum(1 for b in base if b == 'X')
    results = [list(base) for _ in range(2**num_floats)]
    submasks = [format(i, f'0{num_floats}b') for i in range(2**num_floats)]
    for submask, result in zip(submasks, results):
      x_num = 0
      for i, b in enumerate(result):
        if b != 'X':
          continue
        result[i] = submask[x_num]
        x_num += 1
    return [''.join(reversed(r)) for r in results]


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
      addrs = self.mask.apply(addr)
      for a in addrs:
        self.mem[a] = int(value)
      # print(f'Set {addr} to {self.mem[addr]}')

  def sum_mem(self):
    return sum(self.mem.values())

  def run(self):
    while True:
      try:
        self.step()
      except StopIteration:
        return


with Parser('input.txt') as p:
  p.run()


print(p.sum_mem())
