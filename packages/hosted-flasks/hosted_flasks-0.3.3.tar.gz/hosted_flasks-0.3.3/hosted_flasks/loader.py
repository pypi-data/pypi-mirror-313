import logging

import os
import sys

from pathlib import Path
import markdown

import yaml

from importlib.util import spec_from_file_location, module_from_spec

from dataclasses import dataclass, field
from typing import Union, Dict, List

from flask import Flask

from hosted_flasks             import statistics
from hosted_flasks.monkeypatch import Environment

logger = logging.getLogger(__name__)

apps = []

@dataclass
class HostedFlask:
  name         : str
  src          : Union[str, Path]
  path         : str   = None
  hostname     : str   = None
  app          : str   = "app"
  handler      : Flask = field(repr=False, default=None)
  environ      : Dict  = None

  track        : List[str] = field(default_factory=list)
  log          : statistics.LogConfig = field(default_factory=dict)
  exclude      : statistics.Exclusions = field(default_factory=dict)

  title        : str   = None
  description  : str   = None
  image        : str   = None
  github       : str   = None
  docs         : str   = None

  def __post_init__(self):
    if not self.path and not self.hostname:
      logger.fatal(f"⛔️ an app needs at least a path or a hostname: {self.name}")
      return

    self.src = Path(self.src).resolve() # ensure it's a Path

    # we need to add app to apps before loading the handler, because else the
    # monkeypatched os.environ.get won't be able to correct handle calls to it
    # at the time of loading the handler
    apps.append(self)

    # if the handler isn't provided, load it from the source
    if not self.handler:
      self.load_handler()
      
    # without a handler, we remove ourself from the apps
    if not self.handler:
      logger.fatal(f"⛔️ an app needs a handler: {self.src.name}.{self.app}")
      apps.remove(self)
    
    # instantiate log configuration
    self.log = statistics.LogConfig(**self.log)
    
    # instantiate Exclusions
    self.exclude = statistics.Exclusions(self.exclude)
    
    # install a tracker
    if self.track:
      statistics.track(self)
  
  @property
  def appname(self):
    return self.app.split(":", 1)[-1]  # app or name:app or name.sub:app
  
  @property
  def module_path(self):
    """
    self.app can have several forms
    - appname                                 -> name/__init__:appname
    - module_folder:appname                   -> module_folder/__init__:appname
    - module_file_name:appname                -> module_file_name:appname
    - module_folder/module_file_name:appname  -> module_folder/module_file_name:appname
    """

    # determine module_folder
    parts = self.app.split(":", 1)  # app or name:app or name.sub:app
    if len(parts) == 1: # only an app object name
      module_folder = self.src.name  # add module name by default
    else: # explicit module path and app object name
      module_folder = parts[0].replace(".", "/")  # turn dotted name into path

    # check if the last part of the module path points to a file, else add init
    module_path = self.src.parent / module_folder
    if module_path.with_suffix(".py").is_file():
      return module_path.with_suffix(".py")
    return module_path / "__init__.py"
  
  def load_handler(self):
    # create a fresh monkeypatched environment scoped to the app name
    self.environ = Environment.scope(self.name)

    # load the module, creating the handler flask app
    try:
      spec = spec_from_file_location(self.src.name, self.module_path)
      mod = module_from_spec(spec)
      sys.modules[self.src.name] = mod
      spec.loader.exec_module(mod)
      # extract the handler from the mod using the appname
      self.handler = getattr(mod, self.appname)
    except FileNotFoundError:
      logger.warning(f"😞 '{self.module_path}' doesn't exist")
    except AttributeError:
      logger.warning(f"😞 '{self.module_path}' doesn't provide flask object: {self.app}")
    except Exception:
      logger.exception(f"😞 '{self.module_path}' failed to load due to")

def get_config(config=None):
  if not config:
    config = os.environ.get("HOSTED_FLASKS_CONFIG", Path() / "hosted-flasks.yaml")

  try:
    with open(config) as fp:
      return yaml.safe_load(fp)
  except FileNotFoundError:
    raise ValueError(f"💀 I need a config file. Tried: {config}")

def get_apps(config=None, force=False):
  global apps

  if not config:
    config = os.environ.get("HOSTED_FLASKS_CONFIG", Path() / "hosted-flasks.yaml")

  if force:
    apps.clear()

  # lazy load the apps
  if not apps:
    for name, settings in get_config(config)["apps"].items():
      src = config.parent / settings.pop("src")
      settings["description"] = markdown.markdown(settings.pop("description", ""))
      add_app(name, src, **settings)
  return apps

def add_app(name, src, **kwargs):
  app = HostedFlask(name, src, **kwargs)  # adds self to global apps list
  logger.info(f"🌍 loaded app: {app.name}")
