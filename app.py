from flask import request, jsonify, render_template
import os
import flask
import waitress
from main import getActions, getGainers

app = flask.Flask(__name__)
#app.config["DEBUG"] = True

# Route to The API Page
@app.route('/', methods=['GET'])
def home():
    render_template('display.html')
    return jsonify(getActions(stocks=getGainers()))

# Execute app
if __name__ == "__main__":
    app.debug = False
    port = int(os.environ.get('PORT', 33507))
    waitress.serve(app, port=port)
