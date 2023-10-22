import os
from os import path
from pathlib import Path
from turtle import st

from flask import Flask, render_template
from flask_frozen import Freezer


# Transforms routes to match GitHub Pages format
# E.g. '/page' -> '/page.html'
class GH_Freezer(Freezer):
    def urlpath_to_filepath(self, path):
        if (not "." in path.split("/")[-1]) and (
            not path.split("/")[0].endswith(".html") and (path != "/")
        ):
            path += ".html"
        elif path == "/":
            path += "index.html"
        # Remove the initial slash that should always be there
        assert path.startswith("/")
        return path[1:]


template_folder = path.abspath("./wiki")
static_folder = path.abspath("./static")
app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
# app.config['FREEZER_BASE_URL'] = environ.get('CI_PAGES_URL')
app.config["FREEZER_DESTINATION"] = "build"
app.config["FREEZER_RELATIVE_URLS"] = True
app.config["FREEZER_IGNORE_MIMETYPE_WARNINGS"] = True
app.config["FREEZER_DEFAULT_MIMETYPE"] = "text/html"
app.config["TEMPLATES_AUTO_RELOAD"] = True
if "GITHUB_WORKFLOW" in os.environ:
    static_url_path = "/" + os.environ["GITHUB_REPOSITORY"].split("/")[1] + "/static"
    app.static_url_path = static_url_path

    for rule in app.url_map.iter_rules("static"):
        app.url_map._rules.remove(rule)

    app.url_map._rules_by_endpoint["static"] = []
    app.view_functions["static"] = None

    app.add_url_rule(
        f"{static_url_path}/<path:filename>",
        endpoint="static",
        view_func=app.send_static_file,
    )

    freezer = GH_Freezer(app)
else:
    freezer = Freezer(app)


@app.cli.command()
def freeze():
    freezer.freeze()


@app.cli.command()
def serve():
    freezer.run()


@app.route("/")
def home():
    return render_template("pages/home.html", show_header=False)


@app.route("/<page>")
def pages(page):
    return render_template(
        str(Path("pages")) + "/" + page.lower() + ".html", show_header=True
    )


# Main Function, Runs at http://0.0.0.0:8080
if __name__ == "__main__":
    app.run(port=8080, debug=True)
