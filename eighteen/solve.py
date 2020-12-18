import string


class Program:
  def __init__(self, buffer):
    self.buffer = iter(buffer)
    self.register = 0
    self.op = None

  def eval(self, num):
    if self.op == '+':
      self.register += num
    elif self.op == '*':
      self.register *= num
    self.op = None

  def step(self):
    char = next(self.buffer)
    if char == ' ':
      return
    if char in string.digits:
      if self.op is None:
        self.register = int(char)
        return
      self.eval(int(char))
      return
    if char in ['+', '*']:
      self.op = char
      return
    if char == '(':
      sub_program = Program(self.buffer)
      result = sub_program.run()
      if self.op is None:
        self.register = result
        return
      self.eval(result)
      return
    if char == ')':
      raise StopIteration

  def run(self):
    while True:
      try:
        self.step()
      except StopIteration:
        break
    return self.register


def solve(filename):
  with open(filename, 'r') as f:
    programs = [l.strip() for l in f.readlines()]

  result = 0
  for program in programs:
    program_result = Program(program).run()
    result += program_result
    print(program_result)

  return result


print(solve('input.txt'))
