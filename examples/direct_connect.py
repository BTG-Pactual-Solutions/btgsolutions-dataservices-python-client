import json
import requests
import websocket
import threading
import time

API_KEY = 'YOUR_API_KEY_HERE' # NOTE: change to use your API_KEY

ws_type = 'books'
feed = 'stocks'
target = 'realtime'
instruments = ['PETR4','BBAS3']

def get_new_token(API_KEY):
    url = f"https://dataservices.btgpactualsolutions.com/api/v2/authenticate"
    headersList = {
        "Content-Type": "application/json" 
    }
    payload = json.dumps({
        "api_key": API_KEY,
        "client_id": f"btgsolutions-client-python"
    })
    response = requests.request("POST", url, data=payload,  headers=headersList)
    if response.status_code == 200:
        token =  json.loads(response.text).get('AccessToken')
        if not token:
            raise Exception('Something has gone wrong while authenticating: No token as response.')
    else:
        response = json.loads(response.text)
        raise Exception(f"ERROR HTTP Status {response.status_code}")
     
    return token

token = get_new_token(API_KEY=API_KEY)

print(token)

def on_open(ws):
    print("CONNECTION OPENED SUCCESSFULLY")

def on_message(ws, message):
    print(f"Received message: {message}")

def on_error(ws, error):
    print(f"Error : {error}")

def on_close(ws, close_status_code, close_msg):
    print(f"CONNECTION CLOSED {close_status_code} , {close_msg}")

ws = websocket.WebSocketApp(
    url="wss://dataservices.btgpactualsolutions.com/stream/v2/marketdata/book/stocks",
    on_open=on_open,
    on_message=on_message,
    on_error=on_error,
    on_close=on_close, 
    header={"Sec-WebSocket-Protocol": token}
)

wst = threading.Thread(target=ws.run_forever)
wst.daemon = True
wst.start()

time.sleep(3)

available_instruments_msg = {"action": "available_to_subscribe"}
ws.send(json.dumps(available_instruments_msg))

subscription_msg = {"action":"subscribe", "params": ["PETR4", "VALE3", "WDOZ22"]}
ws.send(json.dumps(subscription_msg))

while True:
    time.sleep(30)
