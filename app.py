import os
from os import path
from pathlib import Path

from flask import Flask, render_template
from flask_frozen import Freezer

# Transforms routes to match GitHub Pages format
# E.g. '/page' -> '/page/index.html' 
class GH_Freezer(Freezer):
    def urlpath_to_filepath(self, path):
        if (not '.' in path.split('/')[-1]) and (not path.split('/')[0].endswith('.html')):
            path += '.html'
        # Remove the initial slash that should always be there
        assert path.startswith('/')
        return path[1:]

template_folder = path.abspath('./wiki')

app = Flask(__name__, template_folder=template_folder)
#app.config['FREEZER_BASE_URL'] = environ.get('CI_PAGES_URL')
app.config['FREEZER_DESTINATION'] = 'public'
app.config['FREEZER_RELATIVE_URLS'] = True
app.config['FREEZER_IGNORE_MIMETYPE_WARNINGS'] = True
app.config['FREEZER_DEFAULT_MIMETYPE'] = 'text/html'
if 'GITHUB_WORKFLOW' in os.environ:
    freezer = GH_Freezer(app)
else:
    freezer = Freezer(app)

@app.cli.command()
def freeze():
    freezer.freeze()

@app.cli.command()
def serve():
    freezer.run()

@app.route('/')
def home():
    return render_template('pages/home.html')

@app.route('/<page>')
def pages(page):
    return render_template(str(Path('pages')) + '/' + page.lower() + '.html')

# Main Function, Runs at http://0.0.0.0:8080
if __name__ == "__main__":
    app.run(port=8080)
