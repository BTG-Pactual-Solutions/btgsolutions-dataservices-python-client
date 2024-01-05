import btgsolutions_dataservices as btg
import json
import traceback
import pandas as pd
from time import sleep

desired_tickers = ['ABEVM138', 'ABEVM141']
last_bid_and_offer_by_ticker = {}

ws = btg.MarketDataWebSocketClient(
    api_key='YOUR_API_KEY_HERE',
    stream_type='throttle',
    exchange='b3',
    data_type='books',
    data_subtype='options',
    instruments=desired_tickers
)


def on_message(ws_msg):
    msg = json.loads(ws_msg)

    try:
        if msg["ev"] == "message":
            return
        elif msg["ev"] == "get_last_event":
            if msg['message'] is None:
                return
            msg = msg["message"]
            msg_ticker = msg["symb"]
            last_bid_and_offer_by_ticker[msg_ticker] = {
                "bid": msg["bid"][0]["px"],
                "ask": msg["offer"][0]["px"]
            }
            df = pd.DataFrame().from_dict(last_bid_and_offer_by_ticker).T
            print(df)
            return
        elif msg["ev"] == "trade":
            msg_ticker = msg["symb"]
            return
        elif msg["ev"] == "book":
            # NOTE: Comment this "book" if clause if you do not want your dictionary to be updated continuously in realtime
            msg_ticker = msg["symb"]
            last_bid_and_offer_by_ticker[msg_ticker] = {
                "bid": msg["bid"][0]["px"],
                "ask": msg["offer"][0]["px"]
            }
            df = pd.DataFrame().from_dict(last_bid_and_offer_by_ticker).T
            print(df)
            return
    except Exception as e:
        print(msg)
        print(e)
        print(traceback.format_exc())


ws.run(on_message=on_message)
sleep(2)

for ticker in desired_tickers:
    ws.get_last_event([ticker])

while True:
    sleep(10)
