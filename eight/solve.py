with open('input.txt', 'r') as f:
  raw_program = [f.split() for f in f.readlines()]

input_program = [(cmd, int(arg)) for cmd, arg in raw_program]


def run(program, sub=None):
  reg = 0
  pos = 0
  visited_pos = set()
  while pos < len(program):
    if pos in visited_pos:
      return False, reg
    visited_pos.add(pos)
    cmd, arg = program[pos]
    if sub is not None and sub == pos:
      if cmd == 'jmp':
        cmd = 'nop'
      elif cmd == 'nop':
        cmd = 'jmp'
    if cmd == 'acc':
      reg += arg
    if cmd == 'jmp':
      pos += arg - 1
    # print(f'reg: {reg}, pos: {pos}, cmd: {cmd}')
    pos += 1
  return True, reg


print('----')
print('part 1: ', run(input_program))


sub_indices = (index for index, cmd
               in enumerate(input_program) if cmd[0] in ['jmp', 'nop'])
runs = (run(input_program, sub=index) for index in sub_indices)
valid_runs = (reg for status, reg in runs if status)
print('part 2: ', next(valid_runs))
