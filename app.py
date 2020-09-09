import json,config
from flask import Flask, request, jsonify
from binance.client import Client
from binance.enums import * 
#above import is to import binance variables
app = Flask(__name__)

#client object
client = Client(config.API_KEY, config.API_SECRET)

def order(side, quantity, symbol, order_type=ORDER_TYPE_MARKET):
    try:
        print(f"sending order {order_type} - {side} {quantity} {symbol}")
        order = client.create_order(symbol=symbol, side=side, type=order_type, quantity=quantity)
    except Exception as e:
        print("an exception occured - {}".format(e))
        return False
    return order


#we want a route that is a webhook that can execute binance orders
#webhook alerts fire from tradingview it sends a post request
#a get request retrieves information

@app.route('/')
def index():
    return 'tradingview signals bot'

@app.route('/webhook', methods=['POST'])
def webhook():
    #to access the content of the request object ->
    #print(request.data)
    data = json.loads(request.data)
    
    if data['passphrase'] != config.WEBHOOK_PASSPHRASE:
        return {
            "code": "erro",
            "message": "invalid passphrase"
        }

    print(data['ticker'])
    print(data['bar'])

    #tradingview returns the 'side' in lowercase
    #but binance requires uppercase
    side = data['strategy']['order_action'].upper()
    quantity = data['strategy']['order_contracts']

    #[side, number of contracts, symbol]
    order_response = order(side, 3990, "DOGEUSDT")
    print(order_response)
    
    if order_response:
        #json.loads() converte num python dict()
        return {
            "code": "success",
            "message": "order executed"
        }
        #I don't understand why, but data must be
        #a python dictionary or a string of JSON (str(request.data))
    else:
        print("order failed")
        return {
            "code": "error",
            "message": "order failed"
        }