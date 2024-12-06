from hosted_flasks.loader import get_apps

def test_ensure_exception_when_default_config_file_is_not_found():
  try:
    get_apps(force=True)
    assert False, "expected ValueError due to missing config file"
  except ValueError:
    pass

def test_basic_app_loading(tmp_path):
  app_names = [ "app_1", "app_2" ]

  # create 2 miminal apps
  for app_name in app_names:
    folder = tmp_path / app_name
    folder.mkdir()
    init = folder / "__init__.py"
    init.write_text("""
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
  return "Hello World"  
""")

  # create a configuration
  config = tmp_path / "hosted-flasks.yaml"
  content = "apps:\n"
  for app_name in app_names:
    content += f"""
  {app_name}:
    src: {app_name}
    path: /{app_name}
    hostname: {app_name}
"""
  config.write_text(content)

  apps = get_apps(config, force=True)
  assert len(apps) == 2
  assert [ app.name for app in apps ] == [ "app_1", "app_2" ]

def test_apps_need_at_least_a_path_or_a_hostname(tmp_path):
  config = tmp_path / "hosted-flasks.yaml"
  content = """
apps:
  not_served:
    src: not_served
"""
  config.write_text(content)

  apps = get_apps(config, force=True)
  assert len(apps) == 0

def test_app_without_implementation_is_not_loaded(tmp_path):
  config = tmp_path / "hosted-flasks.yaml"
  content = """
apps:
  dummy:
    src: dummy
    path: /dummy
"""
  config.write_text(content)

  apps = get_apps(config, force=True)
  assert len(apps) == 0

def test_app_without_flask_object_is_not_loaded(tmp_path):
  # add dummy implementation, without exposing a Flask object
  dummy = tmp_path / "dummy"
  dummy.mkdir()
  init = dummy / "__init__.py"
  init.write_text("# nothing here")

  config = tmp_path / "hosted-flasks.yaml"
  content = """
apps:
  dummy:
    src: dummy
    path: /dummy
"""
  config.write_text(content)
  
  apps = get_apps(config, force=True)
  assert len(apps) == 0

def test_app_that_throws_exception_is_not_loaded(tmp_path):
  # add dummy implementation, without exposing a Flask object
  dummy = tmp_path / "dummy"
  dummy.mkdir()
  init = dummy / "__init__.py"
  init.write_text("raise KeyError")

  config = tmp_path / "hosted-flasks.yaml"
  content = """
apps:
  dummy:
    src: dummy
    path: /dummy
"""
  config.write_text(content)
  
  apps = get_apps(config, force=True)
  assert len(apps) == 0

def test_app_with_not_default_appname(tmp_path):
  app_name = "custom_app"
  folder = tmp_path / app_name
  folder.mkdir()
  init = folder / "__init__.py"
  init.write_text("""
from flask import Flask

custom_app = Flask(__name__)

@custom_app.route("/")
def hello_world():
  return "Hello World"  
""")

  # create a configuration
  config = tmp_path / "hosted-flasks.yaml"
  content = f"""
apps:
  {app_name}:
    src: {app_name}
    app: {app_name}:custom_app
    path: /{app_name}
    hostname: {app_name}
"""
  config.write_text(content)

  apps = get_apps(config, force=True)
  assert len(apps) == 1
  assert apps[0].name == app_name

def test_app_with_nested_appname(tmp_path):
  app_name = "custom_app"
  folder = tmp_path / app_name
  folder.mkdir()
  init = folder / "__init__.py"
  init.write_text("# nothing at this level")
  sub = folder / "sub"
  sub.mkdir()
  sub_init = sub / "__init__.py"
  sub_init.write_text("""
from flask import Flask

custom_app = Flask(__name__)

@custom_app.route("/")
def hello_world():
  return "Hello World"  
""")

  # create a configuration
  config = tmp_path / "hosted-flasks.yaml"
  content = f"""
apps:
  {app_name}:
    src: {app_name}
    app: {app_name}.sub:custom_app
    path: /{app_name}
    hostname: {app_name}
"""
  config.write_text(content)

  apps = get_apps(config, force=True)
  assert len(apps) == 1
  assert apps[0].name == app_name

def test_app_with_non_init_app_file(tmp_path):
  app_name = "custom_app"
  folder = tmp_path / app_name
  folder.mkdir()
  init = folder / "__init__.py"
  init.write_text("# nothing at this level")
  app = folder / "app.py"
  app.write_text("""
from flask import Flask

server = Flask(__name__)

@server.route("/")
def hello_world():
  return "Hello World"  
""")

  # create a configuration
  config = tmp_path / "hosted-flasks.yaml"
  content = f"""
apps:
  {app_name}:
    src: {app_name}
    app: {app_name}.app:server
    path: /{app_name}
    hostname: {app_name}
"""
  config.write_text(content)

  apps = get_apps(config, force=True)
  assert len(apps) == 1
  assert apps[0].name == app_name

def test_app_with_dot_in_path(tmp_path):
  app_name = "custom.app"
  folder = tmp_path / app_name
  folder.mkdir()
  init = folder / "__init__.py"
  init.write_text("""
from flask import Flask

server = Flask(__name__)

@server.route("/")
def hello_world():
  return "Hello World"  
""")

  # create a configuration
  config = tmp_path / "hosted-flasks.yaml"
  content = f"""
apps:
  {app_name}:
    src: {app_name}
    app: server
    path: /{app_name}
    hostname: {app_name}
"""
  config.write_text(content)

  apps = get_apps(config, force=True)
  assert len(apps) == 1
  assert apps[0].name == app_name
