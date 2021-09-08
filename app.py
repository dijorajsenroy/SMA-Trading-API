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
    return '''<h1>Simple Moving Averages Trading API</h1><hr>
<p>You will receive json data of top yahoo stocks to trade, and whether you should buy
or sell them according to SMA Algorithm</p>'''


@app.route('/api/', methods=['GET'])
def api_all(): 
    return jsonify(getActions(stocks=getGainers()))

# Execute app
if __name__ == "__main__":
    app.debug = False
    port = int(os.environ.get('PORT', 33507))
    waitress.serve(app, port=port)
