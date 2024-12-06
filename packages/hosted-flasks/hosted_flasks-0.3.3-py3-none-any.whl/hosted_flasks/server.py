import logging

from werkzeug.middleware.dispatcher import DispatcherMiddleware

from hosted_flasks import frontpage
from hosted_flasks.loader import get_apps

# setup logging to stdout

import os

LOG_LEVEL = os.environ.get("LOG_LEVEL") or "INFO"
FORMAT    = "[%(asctime)s] [%(process)d] [%(levelname)s] [%(name)s] %(message)s"
DATEFMT   = "%Y-%m-%d %H:%M:%S %z"

logging.basicConfig(level=LOG_LEVEL, format=FORMAT, datefmt=DATEFMT)
formatter = logging.Formatter(FORMAT, DATEFMT)
logging.getLogger().handlers[0].setFormatter(formatter)

logger = logging.getLogger(__name__)

# dispatch apps based on path and/or hostname

class Dispatcher:
  def __init__(self, frontpage, hosts=None, paths=None):
    self.hosts     = hosts
    self.paths     = DispatcherMiddleware(frontpage, paths)

  def __call__(self, environ, start_response):
    # first check if we have a hostname mapping
    hostname = environ["HTTP_HOST"]
    handler = self.hosts.get(hostname, None)
    if handler:
      logger.debug(f"🧭 dispatching {hostname} to {handler}")
    else:
      logger.debug(f"🧭 dispatching locally (no mapping for {hostname})")
      handler = self.paths
    return handler(environ, start_response)

# combine the apps with the frontpage

hosts = { app.hostname : app.handler for app in get_apps() if app.hostname }
paths = { app.path     : app.handler for app in get_apps() if app.path     }

logger.info("🧭 dispatching domains:")
for host, handler in hosts.items():
  logger.info(f"  - {host} : {handler}")

logger.info("🧭 dispatching paths:")
for host, handler in paths.items():
  logger.info(f"  - {host} : {handler}")

app = Dispatcher(frontpage.app, hosts=hosts, paths=paths)

logger.info(f"✅ {len(get_apps())} hosted flasks up & running...")
