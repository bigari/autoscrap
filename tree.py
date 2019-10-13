class Node:
  def __init__(self, key, tag, data=None, parent=None):
    self.data = data
    self.parent = parent
    self.key = key
    self.tag = tag
    self.children = []

  def add_child(self, obj):
    self.children.append(obj)

  def add_children(self, children):
    self.children.extend(children)



def distance(node1, node2):

  d1 = {}

  current = node1
  i = 0
  d1[current.key] = i
  while current.parent is not None:
    i+=1
    current = current.parent   
    d1[current.key] = i

  current = node2
  i = 0 
  while current.parent is not None and current.key not in d1:
    i+=1
    current = current.parent   


  return i+ 1 + d1[current.key]+ 1