import os
from os import path
from pathlib import Path
import typing as t
import flask_frozen

from flask import Flask, render_template, request, url_for
import posixpath
from posixpath import relpath as posix_relpath
from flask_frozen import Freezer


# Monkey patch to use the correct index url
def gh_relative_url_for(endpoint, **values):
    url = url_for(endpoint, **values)

    # absolute URLs in http://... (with subdomains or _external=True)
    if not url.startswith("/"):
        return url

    url, fragment_sep, fragment = url.partition("#")
    url, query_sep, query = url.partition("?")
    # if url.endswith('/'):
    #     url += 'index.html'
    url += query_sep + query + fragment_sep + fragment

    request_path = request.path
    if not request_path.endswith("/"):
        request_path = posixpath.dirname(request_path)

    return posix_relpath(url, request_path)


# Monkey patch to match GitHub Pages format
# E.g. '/page' -> '/page.html'
class GH_Freezer(Freezer):
    def __init__(self, *args, **kwargs):
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
    flask_frozen.relative_url_for = gh_relative_url_for
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
