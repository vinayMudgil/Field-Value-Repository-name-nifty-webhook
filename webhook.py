from flask import Flask, request
import requests
import math

app = Flask(__name__)

INDEX = "NIFTY"
ROUND_TO = 50
EXPIRY = "25APR2024"
NSE_OPTION_CHAIN_URL = f"https://www.nseindia.com/api/option-chain-indices?symbol={INDEX}"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def get_option_chain():
    session = requests.Session()
    session.headers.update(HEADERS)
    response = session.get(NSE_OPTION_CHAIN_URL)
    return response.json()

def get_atm_strike(price):
    return round(price / ROUND_TO) * ROUND_TO

def fetch_option_price(strike, option_type):
    chain = get_option_chain()
    for data in chain['records']['data']:
        if data['strikePrice'] == strike:
            if option_type == "CE":
                return data['CE']['lastPrice']
            elif option_type == "PE":
                return data['PE']['lastPrice']
    return None

@app.route('/', methods=['POST'])
def webhook():
    data = request.json
    signal = data.get("message")
    price = float(data.get("price", 0))
    atm = get_atm_strike(price)
    option_type = "CE" if signal == "buy_call" else "PE"
    option_price = fetch_option_price(atm, option_type)
    response_text = f"Received {signal.upper()} → Strike: {atm}{option_type}, Price: ₹{option_price}"
    print(response_text)
    return response_text, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
