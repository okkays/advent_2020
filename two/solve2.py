passwords = []
with open('input', 'r') as f:
  for line in f.readlines():
    try:
      passwords.append(line.strip())
    except:
      continue


def is_valid(password):
  rule, value = password.split(': ')
  count, letter = rule.split()
  positions = [int(p) - 1 for p in count.split('-')]
  num_chars = len([pos for pos in positions if value[pos] == letter])
  return num_chars == 1


valid = [password for password in passwords if is_valid(password)]
print('\n'.join(valid))
print(f'answer: {len(valid)} / {len(passwords)}')
