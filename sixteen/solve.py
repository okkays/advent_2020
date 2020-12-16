import functools
print()
with open('input.txt', 'r') as notes:
  raw_ranges, raw_my_ticket, raw_other_tickets = notes.read().split('\n\n')

ranges = {}
for raw_range in raw_ranges.split('\n'):
  field, value = raw_range.strip().split(': ')
  raw_low, raw_high = value.split(' or ')
  low = tuple([int(v) for v in raw_low.split('-')])
  high = tuple([int(v) for v in raw_high.split('-')])
  ranges[field] = (low, high)

my_ticket = [int(t) for t in raw_my_ticket.split('\n')[1].strip().split(',')]

raw_other_tickets = raw_other_tickets.strip().split('\n')[1:]
tickets = [[int(i) for i in ticket.split(',')] for ticket in raw_other_tickets]

print(ranges, my_ticket, tickets)


def get_field_names(value):
  for field, r in ranges.items():
    low, high = r
    if (low[0] <= value <= low[1]) or (high[0] <= value <= high[1]):
      yield field


def get_invalid_values(ticket):
  return [value for value in ticket if not list(get_field_names(value))]


def p1():
  return sum([sum(get_invalid_values(ticket)) for ticket in tickets])


def pivot(list_of_lists):
  return list(zip(*list_of_lists))


def get_possible_fieldnames(valid_tickets):
  fields = pivot(valid_tickets)
  return [set.intersection(*[set(get_field_names(f)) for f in field])
          for field in fields]


def p2():
  valid_tickets = [t for t in tickets if not get_invalid_values(t)]
  fields = get_possible_fieldnames(valid_tickets)
  found = set()
  while any(len(f) > 1 for f in fields):
    for index, field in enumerate(fields):
      if len(field) == 1 and next(iter(field)) not in found:
        break
    found.add(next(iter(field)))
    fields = [other_field - field if index != other_index else field
              for other_index, other_field in enumerate(fields)]

  fields = [next(iter(field)) for field in fields]

  paired_ticket = dict(zip(fields, my_ticket))

  return functools.reduce(lambda a, b: a * b,
                          [value for field, value in paired_ticket.items()
                           if field.startswith('departure')])


print('part1', p1())

print('part2', p2())
