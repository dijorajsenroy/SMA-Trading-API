from bs4 import BeautifulSoup
import json
import requests
import time

# Building a scraper for top gainers from Yahoo finance
def getGainers():
    url = "https://finance.yahoo.com/gainers?offset=0&count=100"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    stocks = []
    for link in soup.findAll('a'):
        l = str(link.get('href'))
        if '/quote/' in l and '%' not in l:
            stocks.append(l.split('?p=')[1])
    return stocks[:10]

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

# writing results to an external json
# with open("results.json", "w") as f:
    # json.dump(a, f, indent = 4)
