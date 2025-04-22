from flask import Flask, request
import json

app = Flask(__name__)

@app.route("/", methods=["POST"])
def webhook():
    data = json.loads(request.data)

    # Extract custom fields from TradingView if sent
    signal = data.get("action", "signal")
    strike = data.get("strike", "Unknown")

    print(f"\n\n SIGNAL RECEIVED:")
    print(f"Action : {signal}")
    print(f"Strike : {strike}")
    print(f"Time   : {data.get('time', 'Unknown')}\n\n")

    return "Signal received", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
