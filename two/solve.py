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
  min_chars_raw, max_chars_raw = count.split('-')
  min_chars = int(min_chars_raw)
  max_chars = int(max_chars_raw)
  num_chars = len([char for char in value if char == letter])
  return min_chars <= num_chars <= max_chars


valid = [password for password in passwords if is_valid(password)]
print('\n'.join(valid))
print(f'answer: {len(valid)} / {len(passwords)}')
