with open('input.txt', 'r') as f:
  raw_content = f.read()

raw_groups = raw_content.split('\n\n')
groups = [
    [set(member) for member in raw_group.split('\n') if member]
    for raw_group in raw_groups
]

reduced_groups_1 = [set.union(*group) for group in groups]
reduced_groups_2 = [set.intersection(*group) for group in groups]

print(sum([len(group) for group in reduced_groups_1]))
print(sum([len(group) for group in reduced_groups_2]))
