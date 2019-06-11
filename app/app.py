import traceback
from flask import render_template, request, redirect, url_for
import logging.config
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
logging.config.fileConfig(app.config["LOGGING_CONFIG"])
logger = logging.getLogger("aceai")
logger.debug('Test log')
# Initialize the database
#db = SQLAlchemy(app)


@app.route('/')
def index():
    """Main view that list players and predictions

    Create view into index page that uses data queried from databases and
    display it into the msiapp/templates/index.html template.

    Returns: rendered html template

    """

    try:
        logger.info("Index page accessed")
        return render_template('index.html')
    except:
        traceback.print_exc()
        logger.warning("Not able to display tracks, error page returned")
        return render_template('error.html')

@app.route('/about')
def about():
    """View that process a click on the about page

    Returns: redirect to about page
    """
    logger.info("About page accessed")
    return render_template('about.html')

@app.route('/add', methods=['POST', 'GET'])
def add_entry():
    """View that process a POST and GET with new player and court input

    :return: redirect to index page
    """

    try:
        player1 = request.form['player1_name']
        player2 = request.form['player2_name']
        surface = request.form['surface']
        df = assemble_data(player1, player2, surface, app.config["ENGINE_STRING"])
        p1win = score_model(df)
        result = pctDisplay(p1win)

        p1h2h = int(df['totalPlayed'][0]*df['h2h_win_pct'][0])
        p2h2h = int(df['totalPlayed'][0] - p1h2h)
        p1rank = int(df['Rank_P1'][0])
        p2rank = int(df['Rank_P2'][0])
        winpctp1 = pctDisplay(df['winpct_surface_P1'][0])
        winpctp2 = pctDisplay(df['winpct_surface_P2'][0])

        return render_template('index.html', p1 = player1, p2 = player2, surf = surface, result=result, 
            p1h2h = p1h2h, p2h2h = p2h2h, p1rank = p1rank, p2rank = p2rank, winpctp1 = winpctp1, winpctp2 = winpctp2)
    except:
        logger.warning("Not able to display tracks, error page returned...")
        return render_template('error.html')

def pctDisplay(floatinput):
    """Display a float input as a percentage value with 2 decimal points and % sign
    Param: (float) float value to be formatted
    Returns: (str) percentage value with the correct format
    """
    return str(round(floatinput*100, 2)) + '%'

if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"], port=app.config["PORT"], host=app.config["HOST"])