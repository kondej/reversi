from flask import Flask, render_template
from flask_cors import CORS

from engine.ai import AI
from engine.core import Core

game = Core()
ai = AI()

app = Flask(__name__, template_folder='../ui/templates', static_folder='../ui/static')
CORS(app)

def run():
    app.run(debug=True, host='0.0.0.0')

@app.route('/')
def index():
    return render_template('index.html')