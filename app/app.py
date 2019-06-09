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
#app.config.from_pyfile('config/flask_config.py')
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
        print(app.config["ENGINE_STRING"])
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
        df = assemble_data(player1, player2, surface, app.config["ENGINE_STRING"])
        print(df.head(1))
        p1win = score_model(player1, player2, surface, app.config["ENGINE_STRING"])
        print(p1win)
        result = pctDisplay(p1win)

        p1h2h = int(df['totalPlayed'][0]*df['h2h_win_pct'][0])
        p2h2h = int(df['totalPlayed'][0] - p1h2h)
        p1rank = int(df['Rank_P1'][0])
        p2rank = int(df['Rank_P2'][0])
        winpctp1 = pctDisplay(df['winpct_surface_P1'][0])
        winpctp2 = pctDisplay(df['winpct_surface_P2'][0])
        #db.session.add(track1)
        #db.session.commit()
        #logger.info("New song added: %s by %s", request.form['title'], request.form['artist'])
        #result = "Hooray, {} will play {} on {} now! {} has an expected {} chance to win".format(player1, player2, surface, player1, p1win)
        #return redirect(url_for('index'))
        return render_template('index.html', p1 = player1, p2 = player2, surf = surface, result=result, 
            p1h2h = p1h2h, p2h2h = p2h2h, p1rank = p1rank, p2rank = p2rank, winpctp1 = winpctp1, winpctp2 = winpctp2)
        #return redirect(url_for('index'))
    except:
        logger.warning("Not able to display tracks, error page returned...")
        #return render_template('index.html')
        return render_template('error.html')

def pctDisplay(floatinput):
    return str(round(floatinput*100, 2)) + '%'

if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"], port=app.config["PORT"], host=app.config["HOST"])