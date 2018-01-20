class Tree(object):
  def __init__(self, left=None, right=None):
    self._left = left
    self._right = right
  
  @property
  def left(self):
    return self._left

  @property
  def right(self):
    return self._right

  @left.setter
  def left(self, value):
    self._left = value

  @right.setter
  def right(self, value):
    self._right = value


if __name__ == '__main__':
  INS = Tree(1)
  print(INS._left) # 1 (Pylint complains "Access protected member") print(INS._right) # None (Pylint complains "Access protected member") print(INS.left) #1
  print(INS.right) # None
  INS.right = 9
  print(INS.right) # 9