from flask import render_template, request, redirect, url_for
import logging.config
from app import db, app
from app.models import Track

# Define LOGGING_CONFIG in config.py - path to config file for setting up the logger (e.g. config/logging/local.conf)
logging.config.fileConfig(app.config["LOGGING_CONFIG"])
logger = logging.getLogger("penny-lane")
logger.debug('Test log')


@app.route('/')
def index():
    """Main view that lists songs in the database.

    Create view into index page that uses data queried from Track database and
    inserts it into the msiapp/templates/index.html template.

    Returns: rendered html template

    """

    try:
        tracks = Track.query.all()
        logger.debug("Index page accessed")
        return render_template('index.html', tracks=tracks)
    except:
        logger.warning("Not able to display tracks, error page returned")
        return render_template('error.html')


@app.route('/add', methods=['POST'])
def add_entry():
    """View that process a POST with new song input

    :return: redirect to index page
    """

    try:
        track1 = Track(artist=request.form['artist'], album=request.form['album'], title=request.form['title'])
        db.session.add(track1)
        db.session.commit()
        logger.info("New song added: %s by %s", request.form['title'], request.form['artist'])
        return redirect(url_for('index'))
    except:
        logger.warning("Not able to display tracks, error page returned")
        return render_template('error.html')


if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"], port=app.config["PORT"], host=app.config["HOST"])
