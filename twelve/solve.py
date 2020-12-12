import math

with open('dummy.txt', 'r') as f:
  raw_instructions = [f.strip() for f in f.readlines()]

problem_instructions = [(r[0], int(r[1:])) for r in raw_instructions]


# N means to move north by the given value.
# S means to move south by the given value.
# E means to move east by the given value.
# W means to move west by the given value.
# L means to turn left the given number of degrees.
# R means to turn right the given number of degrees.
# F means to move forward by the given value in the direction the ship is currently facing.

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
    return Point(self.x * other.x, self.y * other.y)

  def __repr__(self):
    return f'({self.x}, {self.y})'

  def __eq__(self, other):
    return self.x == other.x and self.y == other.y

assert Point(1, 2) + Point(3, 4) == Point(4, 6)
assert Point(1, 2) - Point(3, 4) == Point(-2, -2)
assert Point(6, 2) * Point(3, 4) == Point(18, 8)
assert Point(-6, 2).manhattan == 8

class Ship:
  def __init__(self):
    self.position = Point(0, 0)
    self.heading = 90

  def bulk_move(self, instructions):
    for instruction in instructions:
      self.move(instruction)

  def move(self, instruction):
    direction, amount = instruction
    if direction == 'N':
      self.position += Point(amount, 0)
    elif direction == 'S':
      self.position -= Point(amount, 0)
    elif direction == 'E':
      self.position += Point(0, amount)
    elif direction == 'W':
      self.position -= Point(0, amount)
    elif direction == 'L':
      self.heading -= amount
    elif direction == 'R':
      self.heading += amount
    elif direction == 'F':
      heading_x = math.cos(math.radians(self.heading))
      heading_y = math.sin(math.radians(self.heading))
      heading_points = Point(heading_x, heading_y)
      self.position += Point(amount, amount) * heading_points
    else:
      raise ValueError('bad direction')

ship = Ship()
ship.bulk_move(problem_instructions)
print(round(ship.position.manhattan))
