from hosted_flasks.loader import get_apps

def test_app_specific_environment_variable(tmp_path):
  # create app
  app_name = "app_1"
  folder = tmp_path / app_name
  folder.mkdir()
  init = folder / "__init__.py"
  init.write_text("""
from flask import Flask
import os

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

app = Flask(__name__)

NAME = os.environ.get("NAME")

@app.route("/")
def hello_world():
  return f"Hello {NAME}"  
""")

  # create a .env
  env = folder / ".env"
  env.write_text("NAME=AppSpecific")

  # create a configuration
  config = tmp_path / "hosted-flasks.yaml"
  config.write_text(f"""
apps:
  {app_name}:
    src: {app_name}
    path: /{app_name}
    hostname: {app_name}
""")

  apps = get_apps(config, force=True)
  assert len(apps) == 1

  app = apps[0]

  html = app.handler.test_client().get("/")
  assert app.environ.get("NAME") == "AppSpecific"
  assert app.environ.get("APP_1_NAME") == "AppSpecific"
  assert html.data == b"Hello AppSpecific"
