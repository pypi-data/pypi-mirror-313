# ruff: noqa: E402

import logging
import os

# setup logging to stdout

LOG_LEVEL = os.environ.get("LOG_LEVEL") or "INFO"
FORMAT    = "[%(name)s] [%(levelname)s] %(message)s"
DATEFMT   = "%Y-%m-%d %H:%M:%S %z"

logging.basicConfig(level=LOG_LEVEL, format=FORMAT, datefmt=DATEFMT)
formatter = logging.Formatter(FORMAT, DATEFMT)
logging.getLogger().handlers[0].setFormatter(formatter)

logger = logging.getLogger(__name__)

from hosted_flasks.loader import get_apps

def cli():
  for app in get_apps():
    print(f"{app.name} is hosted on")
    if app.path:
      print(f" - from path {app.path}")
    if app.hostname:
      print(f" - from hostname {app.hostname}")

if __name__ == "__main__":
  cli()
