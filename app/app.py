import traceback
from flask import render_template, request, redirect, url_for
import logging.config
# from app.models import Tracks
from flask import Flask
from score_model_db import assemble_data, score_model
#from flask_sqlalchemy import SQLAlchemy

# Initialize the Flask application
app = Flask(__name__)

# Configure flask app from flask_config.py
#app.config.from_pyfile('../config/flask_config.py')
app.config.from_pyfile('../config/flask_config.py')

# Define LOGGING_CONFIG in flask_config.py - path to config file for setting
# up the logger (e.g. config/logging/local.conf)
#logging.config.fileConfig(app.config["LOGGING_CONFIG"])
logger = logging.getLogger("penny-lane")
logger.debug('Test log')

# Initialize the database
#db = SQLAlchemy(app)


@app.route('/')
def index():
    """Main view that lists songs in the database.

    Create view into index page that uses data queried from Track database and
    inserts it into the msiapp/templates/index.html template.

    Returns: rendered html template

    """

    try:
        #tracks = db.session.query(Tracks).limit(app.config["MAX_ROWS_SHOW"]).all()
        logger.debug("Index page accessed")
        #return render_template('index.html', tracks=tracks)
        return render_template('index.html')
    except:
        traceback.print_exc()
        logger.warning("Not able to display tracks, error page returned")
        return render_template('error.html')


@app.route('/add', methods=['POST', 'GET'])
def add_entry():
    """View that process a POST with new song input

    :return: redirect to index page
    """
    #player1 = request.form['player1_name']
    #player2 = request.form['player2_name']

    try:
        #track1 = Tracks(artist=request.form['artist'], album=request.form['album'], title=request.form['title'])
        player1 = request.form['player1_name']
        player2 = request.form['player2_name']
        surface = request.form['surface']
        p1win = score_model(player1, player2, surface)
        #db.session.add(track1)
        #db.session.commit()
        #logger.info("New song added: %s by %s", request.form['title'], request.form['artist'])
        result = "Hooray, {} will play {} on {} now! {} has an expected {} chance to win".format(player1, player2, surface, player1, p1win)
        #return redirect(url_for('index'))
        return render_template('index.html', result=result)
        #return redirect(url_for('index'))
    except:
        logger.warning("Not able to display tracks, error page returned")
        return render_template('index.html')
        #return render_template('error.html')

if __name__ == '__main__':
    app.run(debug=app.config["DEBUG"], port=app.config["PORT"], host=app.config["HOST"])