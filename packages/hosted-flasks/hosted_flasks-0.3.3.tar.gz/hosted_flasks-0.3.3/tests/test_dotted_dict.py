from hosted_flasks.utils import DottedDict

def test_succesfull_access():
  d = { "a" : 1, "b" : { "b1" : 1, "b2" : 2 }}
  dd = DottedDict(d)
  
  assert dd["a"] == 1
  assert dd["b.b2"] == 2

def test_unsuccesfull_access():
  d = { "a" : 1, "b" : { "b1" : 1, "b2" : 2 }}
  dd = DottedDict(d)
  
  try:
    dd["c"]
    assert False, "expected KeyError"
  except KeyError:
    pass
