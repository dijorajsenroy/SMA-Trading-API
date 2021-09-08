from flask import request, jsonify
import flask
from bs4 import BeautifulSoup
import os
import json
import requests
import time
import waitress

# writing results to an external json
# with open("results.json", "w") as f:
    # json.dump(a, f, indent = 4)

app = flask.Flask(__name__)
#app.config["DEBUG"] = True

# Building a scraper for top gainers from Yahoo finance
def getGainers():
    url = "https://finance.yahoo.com/gainers?offset=0&count=100"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    stocks = []
    for link in soup.findAll('a'):
        l = link.get('href').split('/')
        if l[1] == 'quote':
            x = l[-1].split('?')[0]
            if '%' in x:
                pass
            else:
                stocks.append(x)
    return stocks

# Function to check if the stock should be bought using Simple Moving Averages
def shouldBuy(data):
    avg200 = 0
    avg50 = 0
    count = 0
    for d in data["Time Series (Daily)"]:
        avg200 += float(data["Time Series (Daily)"][d]["2. high"])
        count += 1
    avg200 = avg200/count
    count = 0
    for d in data["Time Series (Daily)"]:
        avg50 += float(data["Time Series (Daily)"][d]["2. high"])
        if count == 50:
            break
        else:
            count += 1
    avg50 = avg50/count
    if avg50 >= avg200:
        return True
    else:
        return False


# Obtaining stock market info using the Alpha Vantage API in Python
def getActions(stocks):
    actions = dict()
    key = "6U4PE7MUGBZLVMM3"  # av api-key
    for sym in stocks:
        print("Obtaining data for symbol:", sym)
        url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={0}&interval=5min&apikey={1}'.format(
            sym, key)
        r = requests.get(url)
        data = r.json()
        if 'Error Message' in data.keys():
            print('failure')
            stocks.remove(sym)
        else:
            print('success')
            for d in data["Time Series (Daily)"]:
                currPrice = data["Time Series (Daily)"][d]["2. high"]
                break
            if shouldBuy(data):
                actions[sym] = ["Buy", currPrice]
            else:
                actions[sym] = ["Sell", currPrice]
            time.sleep(20)  # need to add delay for free API use
    return actions

# Route to The API Page
@app.route('/', methods=['GET'])
def home():
    return '''<h1>Simple Moving Averages Trading API</h1><hr>
<p>You will receive json data of top yahoo stocks to trade, and whether you should buy
or sell them according to SMA Algorithm</p>'''

@app.route('/api', methods=['GET'])
def api_all():
    actions = getActions(stocks=getGainers())
    return jsonify(actions)


if __name__ == "__main__":
    app.debug = False
    port = int(os.environ.get('PORT', 33507))
    waitress.serve(app, port=port)