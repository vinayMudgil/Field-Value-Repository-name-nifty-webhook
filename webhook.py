
from flask import Flask, request
import json

app = Flask(__name__)

@app.route("/", methods=["POST"])
def webhook():
    data = json.loads(request.data)
    
    # Extract custom fields from TradingView if sent
    signal = data.get("action", "Signal")
    strike = data.get("strike", "Unknown")
    
    print(f"\n📢 SIGNAL RECEIVED:")
    print(f"Action : {signal}")
    print(f"Strike : {strike}")
    print(f"Time   : {data.get('time', 'Unknown')}\n")

    return "Signal received", 200
