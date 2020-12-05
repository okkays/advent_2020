with open('input.txt', 'r') as f:
  tickets = [f.strip() for f in f.readlines()]


def search(steps, start=None, end=None):
  inc = 2**(len(steps) - 1)
  if start is None:
    start = 0
  if end is None:
    end = inc - 1
  if not steps:
    return start
  if steps[0]:
    return search(steps[1:], start + inc, end)
  return search(steps[1:], start, end - inc)


def find_seat(ticket):
  row_steps = [c == 'B' for c in ticket if c in ['B', 'F']]
  col_steps = [c == 'R' for c in ticket if c in ['L', 'R']]
  row = search(row_steps)
  col = search(col_steps)
  sid = (row * (len(row_steps) + 1)) + col
  print(row, col, sid)
  return sid


print()
# print(find_seat('FBFBBFFRLR'))
seats = [find_seat(ticket) for ticket in tickets]
seats.sort()
low = seats[0]
high = seats[-1]
print('part 1', high)

print([a + 1 for a, b in zip(seats[::2], seats[1::2]) if b - 1 != a])
