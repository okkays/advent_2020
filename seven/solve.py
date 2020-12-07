with open('input.txt', 'r') as f:
  rules = f.readlines()

rule_map = {}
for rule in rules:
  rule = rule.replace(' bags', '').replace(' bag', '').replace('.', '')
  key, values = rule.split(' contain ')
  content_map = {}
  for content in values.split(', '):
    if content.startswith('no other'):
      continue
    count, kind = content.strip().split(' ', 1)
    content_map[kind] = int(count)
  rule_map[key] = content_map

def has_child(rule, child):
  contents = rule_map[rule]
  if child in contents:
    return True
  return any(has_child(content, child) for content in contents)

print('part 1')
valid = [rule for rule in rule_map if has_child(rule, 'shiny gold')]
print(len(valid))

def count_children(rule):
  contents = rule_map[rule]
  return sum(value + (value * count_children(content))
             for content, value in contents.items())


print('part 2')
print(count_children('shiny gold'))
