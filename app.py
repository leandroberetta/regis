from flask import Flask, render_template
from regis.service import services

app = Flask(__name__, static_folder='regis/static', template_folder='regis/templates')

# Blueprints
app.register_blueprint(services, url_prefix='/services')


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(port=4000, debug=True)