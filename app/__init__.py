from flask import Flask

# Initialize the Flask application
app = Flask(__name__)

# Configure flask app from config.py
app.config.from_object('config')