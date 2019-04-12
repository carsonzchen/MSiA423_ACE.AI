from flask import Flask
from flask_sqlalchemy import SQLAlchemy


# Initialize the Flask application
app = Flask(__name__)

# Configure flask app from config.py
app.config.from_object('config')

# Initialize the database
db = SQLAlchemy(app)