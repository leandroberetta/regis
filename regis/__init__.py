from flask import Flask, render_template
from configparser import ConfigParser
from regis.services import services

# Configuration
config = ConfigParser()
config.read('../regis.cfg')

app = Flask(__name__)

# Blueprints
app.register_blueprint(services, url_prefix='/services')


@app.route('/')
def index():
    return render_template('index.html')

