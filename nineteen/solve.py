import itertools
import re

def solve(filename):
  with open(filename, 'r') as f:
    raw = f.read()
  raw_rules, raw_messages = raw.replace('"', '').split('\n\n')
  rules = dict([(f'{rule} ').split(':') for rule in raw_rules.strip().split('\n')])
  messages = raw_messages.strip().split('\n')
  rule_zero = re.compile(reduce_rules(rules).replace(' ', ''))
  print(rule_zero)
  matches = [m for m in messages if rule_zero.fullmatch(m)]
  print(matches)
  print(len(matches))

def reduce_rules(rules):
  rules = list(rules.items())
  finalized = []
  new_rules = []
  for key, value in rules:
    if all(not char.isdigit() for char in value):
      finalized.append((key, value))
    else:
      new_rules.append((key, value))
  rules = dict(new_rules)
  last_rules = {}

  while rules != last_rules:
    last_rules = dict(rules)
    for final_key, final_value in finalized:
      for key, value in rules.items():
        rules[key] = value.replace(f' {final_key} ', f' ( {final_value} ) ')

    new_rules = {}
    for key, value in rules.items():
      if all(not char.isdigit() for char in value):
        finalized.append((key, value))
      else:
        new_rules[key] = value
    rules = new_rules

  red = re.compile('\d+')
  rule_zero = rules.pop('0')
  for i in range(100):
    for key, value in rules.items():
      rule_zero = rule_zero.replace(f' {key} ', f' ( {value} ) ')
  red.sub('', rule_zero)
  return rule_zero

solve('inputmean.txt')
