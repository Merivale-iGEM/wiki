import os
from os import path
from pathlib import Path
import typing as t

from flask import Flask, render_template
from flask_frozen import Freezer


# Cheap hack to match GitHub Pages format
# E.g. '/page' -> '/page.html'
class GH_Freezer(Freezer):
    def __init__(self, *args, **kwargs):
        self.repo_name = os.environ["GITHUB_REPOSITORY"].split("/")[1]
        super().__init__(*args, **kwargs)

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

    # def _build_one(self, url, last_modified=None):
    #     if url[1 : len(self.repo_name) + 1] == self.repo_name:
    #         url = url[len(self.repo_name) + 1 :]
    #         print(url)
    #     return super()._build_one(url, last_modified)


# Cheap hack to make static files work on GitHub Pages
# Prefixes all static file URLs with the repo name
class GH_Flask(Flask):
    def __init__(self, *args, **kwargs):
        self.repo_name = os.environ["GITHUB_REPOSITORY"].split("/")[1]
        super().__init__(*args, **kwargs)

    def url_for(
        self,
        endpoint: str,
        **values: t.Any,
    ) -> str:
        url = super().url_for(endpoint, **values)
        # if endpoint == "static":
        #    url = "/" + self.repo_name + url
        return url


template_folder = path.abspath("./wiki")
static_folder = path.abspath("./static")
app = None
if "GITHUB_WORKFLOW" in os.environ:
    app = GH_Flask(
        __name__, template_folder=template_folder, static_folder=static_folder
    )
else:
    app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)

# app.config['FREEZER_BASE_URL'] = environ.get('CI_PAGES_URL')
app.config["FREEZER_DESTINATION"] = "build"
app.config["FREEZER_RELATIVE_URLS"] = True
app.config["FREEZER_IGNORE_MIMETYPE_WARNINGS"] = True
app.config["FREEZER_DEFAULT_MIMETYPE"] = "text/html"
app.config["TEMPLATES_AUTO_RELOAD"] = True
if "GITHUB_WORKFLOW" in os.environ:
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
