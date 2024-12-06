class DottedDict:
  """
  wrapper around a normal dict, allowing dotted key access
  >>> d = { "a" : 1, "b" : { "b1" : 1, "b2" : 2 }}
  >>> dd = DottedDict(d)
  >>> dd["b.b2"]
  2
  """
  def __init__(self, wrapped_dict):
    self.wrapped_dict = wrapped_dict
    
  def __getitem__(self, path):
    value = self.wrapped_dict
    for step in path.split("."):
      value = value[step]
    return value
