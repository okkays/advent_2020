with open('input.txt', 'r') as f:
  all_adapters = sorted(int(a) for a in f.readlines())

def get_counts(adapters):
  counts = {c: 0 for c in [1,2,3]}
  prev_adapter = 0
  for adapter in adapters:
    counts[adapter - prev_adapter] += 1
    prev_adapter = adapter
  counts[3] += 1
  return counts

counts = get_counts(all_adapters)

class Node:
  def __init__(self, value):
    self.value = value
    self.children = []
    self.answer = None

  def __repr__(self):
    return f'<{self.value}>'

  def count(self):
    if self.answer is not None:
      return self.answer
    if not self.children:
      return 1
    self.answer = sum(c.count() for c in self.children)
    return self.answer

nodes = {
  adapter: Node(adapter)
  for adapter in [0, *all_adapters, all_adapters[-1] + 3]
}
for node in nodes.values():
  for i in [1,2,3]:
    if node.value + i in nodes:
      node.children.append(nodes[node.value + i])

print(nodes[0].count())
