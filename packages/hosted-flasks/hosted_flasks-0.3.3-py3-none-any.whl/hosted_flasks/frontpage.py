import logging

import os

from pathlib import Path

from flask import Flask, render_template, send_from_directory, abort, request

from hosted_flasks.loader     import get_apps, get_config
from hosted_flasks.statistics import db

logger = logging.getLogger(__name__)

FRONTPAGE_FOLDER = os.environ.get("HOSTED_FLASKS_FRONTPAGE_FOLDER", None)
if not FRONTPAGE_FOLDER:
  FRONTPAGE_FOLDER = Path(__file__).resolve().parent / "frontpage"
  logger.debug("📰 using default frontpage folder")
else:
  FRONTPAGE_FOLDER = Path(FRONTPAGE_FOLDER).resolve()
  logger.info(f"📰 using custom frontpage folder: {FRONTPAGE_FOLDER.relative_to(Path.cwd())}")

app = Flask(
  "hosted-flasks",
  template_folder=FRONTPAGE_FOLDER,
  static_folder=f"{FRONTPAGE_FOLDER}/static",
  static_url_path=""
)

app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.route("/")
def show_frontpage():
  return render_template(
    "index.html",
    apps=get_apps(),
    title=get_config()["title"],
    description=get_config()["description"]
  )

@app.route("/hosted/<path:filename>")
def send_frontpage_static(filename):
  # static folder from root of app that uses hosted flasks to serve apps
  return send_from_directory("", filename)

# if we have a database connection
if db is not None:
  # get shared secret cookie
  SECRET = os.environ.get("HOSTED_FLASKS_STATS_SECRET", None)
  # if we have such secret cookie, setup an endpoint for retrieving the stats
  if SECRET:
    @app.route("/stats")
    def show_stats():
      # if the browser has a cookie with the secret cookie value, show the stats
      if not request.cookies.get("stats", None) == SECRET:
        abort(404)
      return render_template(
        "stats.html",
        apps=get_apps(),
        title=get_config()["title"],
        description=get_config()["description"],
        stats=list(db.logs.aggregate( [
            {
              "$group": {
                "_id": { 
                   "hosted_flask": "$metadata.hosted_flask",
                   "date": {
                     "$dateToString": {
                       "format": "%Y-%m-%d",
                       "date"  : "$datetime"
                     }
                   },
                 },
                 "visitors": { "$sum": 1 }
              }
           },
           {
             "$sort": {
                "_id": 1
              }  
           },
           {
             "$project" : {
               "_id"          : 0,
               "hosted_flask" : "$_id.hosted_flask",
               "date"         : "$_id.date",
               "visitors"     : "$visitors"
             }
           }
        ]))
      )
