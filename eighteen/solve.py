import string


class Program:
  def __init__(self, program):
    self.lstack = []
    self.rstack = program
    self.register = None

  def run(self):
    while self.rstack:
      char = self.rstack.pop()
      try:
        num = int(char)
      except ValueError:
        num = None
      if num is not None:
        if self.lstack and self.lstack[-1] == '+':
          self.lstack.pop()
          self.lstack.append(num + self.lstack.pop())
        else:
          self.lstack.append(num)
      elif char in '*+':
        self.lstack.append(char)
      elif char == '(':
        self.rstack.append(Program(self.rstack).run())
      elif char == ')':
        break
    if self.register is None:
      self.register = 1
    while self.lstack:
      char = self.lstack.pop()
      if char == '*':
        continue
      self.register *= int(char)
    return self.register


def solve(filename):
  with open(filename, 'r') as f:
    programs = [l.strip() for l in f.readlines()]

  result = 0
  for program in programs:
    program_result = Program(list(reversed(program.replace(' ', '')))).run()
    result += program_result
    print(program_result)

  return result


print(solve('input.txt'))
