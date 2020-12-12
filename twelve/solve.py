import math

print()

with open('input.txt', 'r') as f:
  raw_instructions = [f.strip() for f in f.readlines()]

problem_instructions = [(r[0], int(r[1:])) for r in raw_instructions]

class Point:
  def __init__(self, x, y):
    self.x = x
    self.y = y

  @property
  def manhattan(self):
    return abs(self.x) + abs(self.y)

  def __add__(self, other):
    return Point(self.x + other.x, self.y + other.y)

  def __sub__(self, other):
    return Point(self.x - other.x, self.y - other.y)

  def __mul__(self, other):
    if isinstance(other, Point):
      return Point(self.x * other.x, self.y * other.y)
    return Point(self.x * other, self.y * other)

  def __repr__(self):
    return f'({self.x}, {self.y})'

  def __eq__(self, other):
    return self.x == other.x and self.y == other.y

assert Point(1, 2) + Point(3, 4) == Point(4, 6)
assert Point(1, 2) - Point(3, 4) == Point(-2, -2)
assert Point(6, 2) * Point(3, 4) == Point(18, 8)
assert Point(-6, 2).manhattan == 8

class Ship:
  def __init__(self, waypoint):
    self.waypoint = waypoint
    self.position = Point(0, 0)

  def bulk_move(self, instructions):
    for instruction in instructions:
      self.move(instruction)

  def rotate_waypoint(self, degrees):
    cos_t = math.cos(math.radians(-degrees))
    sin_t = math.sin(math.radians(-degrees))

    new_x = cos_t * self.waypoint.x - sin_t * self.waypoint.y
    new_y = sin_t * self.waypoint.x + cos_t * self.waypoint.y

    new_waypoint = Point(round(new_x), round(new_y))
    print(self.waypoint, new_waypoint)
    self.waypoint = new_waypoint

  def move(self, instruction):
    print(instruction, self.position, self.waypoint, self.position.manhattan)
    direction, amount = instruction
    if direction == 'N':
      self.waypoint += Point(0, amount)
    elif direction == 'S':
      self.waypoint -= Point(0, amount)
    elif direction == 'E':
      self.waypoint += Point(amount, 0)
    elif direction == 'W':
      self.waypoint -= Point(amount, 0)
    elif direction == 'L':
      self.rotate_waypoint(-amount)
    elif direction == 'R':
      self.rotate_waypoint(amount)
    elif direction == 'F':
      self.position += self.waypoint * amount
    else:
      raise ValueError('bad direction')

test_ship = Ship(Point(4, 10))
test_ship.move(('R', 90))
assert test_ship.waypoint == Point(10, -4)
test_ship.move(('R', 90))
assert test_ship.waypoint == Point(-4, -10)
test_ship.move(('R', 90))
assert test_ship.waypoint == Point(-10, 4)
test_ship.move(('R', 90))
assert test_ship.waypoint == Point(4, 10)

ship = Ship(Point(10, 1))
ship.bulk_move(problem_instructions)
print(round(ship.position.manhattan))
