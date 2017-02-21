from flask import Flask, render_template
from services import services

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.register_blueprint(services, url_prefix='/services')
    app.run(port=4000)
