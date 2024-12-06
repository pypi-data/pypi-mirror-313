from hosted_flasks.statistics import Exclusions

def test_positive_exclusions():
  exclusions = Exclusions({
    "user_agent.user_agent.family" : "HeadlessChrome",
    "user_agent.string" : "researchscan"
  })
  assert exclusions.matches({
    "user_agent" : {
      "string" : "Mozilla/5.0 researchscan.comsys.rwth-aachen.de",
      "user_agent" : {
        "family" : "Other"
      }
    }
  })
  assert exclusions.matches({
    "user_agent" : {
      "string" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/125.0.0.0 Safari/537.36",
      "user_agent" : {
        "family" : "HeadlessChrome"
      }
    }
  })
      

def test_negative_exclusions():
  exclusions = Exclusions({
    "user_agent.user_agent.family" : "HeadlessChrome",
    "user_agent.string" : "researchscan"
  })
  assert not exclusions.matches({
    "user_agent" : {
      "string" : "Dalvik/2.1.0 (Linux; U; Android 9.0; ZTE BA520 Build/MRA58K)",
      "user_agent" : {
        "family" : "Android"
      }
    }
  })

def test_incorrect_exclusions_configuration():
  try:
    Exclusions([1, 2, 3])
    assert False, "expected a ValueError"
  except ValueError:
    pass
