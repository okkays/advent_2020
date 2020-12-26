INPUT = {
  'door': 8184785,
  'card': 5293040,
}

DUMMY = {
  'door': 5764801,
  'card': 17807724,
}

def transform_given_public(subject, public_key):
  value = 1
  loop_size = 0
  while value != public_key:
    loop_size += 1
    value *= subject
    value %= 20201227
  return loop_size

def transform_given_loop(subject, loop_size):
  value = 1
  for i in range(loop_size):
    value *= subject
    value %= 20201227
  return value

def handshake(card_public, door_public):
  card_loop = transform_given_public(7, card_public)
  door_loop = transform_given_public(7, door_public)
  card_encryption_key = transform_given_loop(door_public, card_loop)
  door_encryption_key = transform_given_loop(card_public, door_loop)
  assert card_encryption_key == door_encryption_key
  print(f'card loop: {card_loop}')
  print(f'door loop: {door_loop}')
  return card_encryption_key

def solve():
  target = INPUT
  encryption_key = handshake(target['card'], target['door'])
  print(encryption_key)

solve()
