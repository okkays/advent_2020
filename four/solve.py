with open('input.txt', 'r') as f:
  corpus = f.read()


def clean_passport(raw_passport):
  passport = {}
  for field in raw_passport.split():
    key, value = field.split(':')
    passport[key] = value
  return passport


raw_passports = corpus.split('\n\n')
passports = [clean_passport(raw) for raw in raw_passports]

required_fields = {
    'byr': lambda value: 1920 <= int(value) <= 2002,
    'iyr': lambda value: 2010 <= int(value) <= 2020,
    'eyr': lambda value: 2020 <= int(value) <= 2030,
    'hgt': lambda value: (value.endswith('cm') and 150 <= int(value[:-2]) <= 193) or (value.endswith('in') and 59 <= int(value[:-2]) <= 76),
    'hcl': lambda value: value.startswith('#') and int(value[1:], 16) > -1,
    'ecl': lambda value: value in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'],
    'pid': lambda value: len(value) == 9 and int(value) > -1,
}


def is_valid(passport):
  for field, value in passport.items():
    try:
      if not required_fields[field](value):
        print(f'invalid value for {field}: {repr(value)}')
        return False
    except KeyError as key:
      if 'cid' in str(key):
        continue
      print(f'unexpected key: {key}')
      continue
    except ValueError:
      print(f'bad value for {field}: {repr(value)}')
      return False
  return not required_fields.keys() - passport.keys()


valid_passports = [p for p in passports if is_valid(p)]
print(len(valid_passports))
