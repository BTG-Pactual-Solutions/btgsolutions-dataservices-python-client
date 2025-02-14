API_KEY = 'PUT_YOUR_KEY_HERE'

import pandas as pd
import datetime
import btgsolutions_dataservices as btg
import json
import traceback
from time import sleep
import streamlit as st
from time import sleep
import threading

DATA_SUBTYPE = "stocks" # "stocks", 'derivatives', 'options'
TICKERS_OF_INTEREST = ["BPAC11", "VALE3", "MGLU3", "AMER3", "SHOW3"]

class CustomClient:

    def __init__(self, api_key:str, data_subtype:str, data_type:str='books', ticker_list=None):

        self.ticker_list = ticker_list
        self.reset_internal_states()

        self.ws = btg.MarketDataWebSocketClient(
            api_key=api_key,
            stream_type='realtime',
            exchange='b3',
            data_type=data_type,
            data_subtype=data_subtype
        )

        self.ws.run(
            on_open=self.on_open_connection_callback,
            on_message=self.message_callback,
            reconnect=True,
            default_logs=False
        )

    def reset_internal_states(self,):
        self.last_bid_and_offer_by_ticker = {}
        self.available_to_subscribe = []
        self.blank_last_event_number = 0

    def request_available_tickers_to_subscribe(self,):
        self.ws.available_to_subscribe()

    def internal_dict_state_summary(self):
        up_to_date = len(self.last_bid_and_offer_by_ticker)
        blank_books = self.blank_last_event_number
        total = up_to_date + blank_books
        available_number = len(self.available_to_subscribe)

        return f"up_to_date: {up_to_date} & blank_books: {blank_books} = {total} | available_to_subscribe = {available_number}"
    
    def message_callback(self, ws_msg):
        msg = json.loads(ws_msg)

        try:
            if msg["ev"] == "get_last_event":
                if msg["message"] is None:
                    self.blank_last_event_number += 1
                    return
                msg = msg["message"]
                msg_ticker = msg["symb"]
                if self.last_bid_and_offer_by_ticker.get(msg_ticker):
                    pass
                else:
                    self.last_bid_and_offer_by_ticker[msg_ticker] = self.get_last_bid_and_offer_from_message(msg, source="last_event")
                return
            elif msg["ev"] == "book":
                # NOTE: Comment this "book" if clause if you do not want your dictionary to be updated continuously in realtime
                msg_ticker = msg["symb"]
                self.last_bid_and_offer_by_ticker[msg_ticker] = self.get_last_bid_and_offer_from_message(msg, source="book_event")
                return
            elif msg["ev"] == "available_to_subscribe":
                if msg["message"] is None:
                    print(f"Unexpected behavior: {msg}")
                    return
                else:
                    self.available_to_subscribe = msg["message"]

                    tickers_to_subscribe = set(self.available_to_subscribe) & set(self.ticker_list)
                    not_available_to_subscribe = set(self.ticker_list) - set(self.available_to_subscribe)
                    if len(not_available_to_subscribe) > 0:
                        print(f"The following instruments of interest were not available to subscribe: {not_available_to_subscribe}. Check DataSubtype or ticker validity.")

                    tickers_to_subscribe = list(tickers_to_subscribe)
                    self.fill_last_event(ticker_list=tickers_to_subscribe)
                    self.subscribe(tickers_to_subscribe)
        except Exception as e:
            # print(msg)
            # print(e)
            print(traceback.format_exc())
        
    def get_last_bid_and_offer_from_message(self, msg, source):

        last_bid_offer = {
            "bid": None,
            "bid_vol": None,
            "ask": None,
            "ask_vol": None,
            "source": source,
        }
        last_update = None

        if msg["bid"] and len(msg["bid"]) > 0:
            last_bid_offer["bid"] = msg["bid"][0]["px"]
            last_bid_offer["bid_vol"] = msg["bid"][0]["qty"]
            last_update = msg["bid"][0]["datetime"]
        if msg["offer"] and len(msg["offer"]) > 0:
            last_bid_offer["ask"] = msg["offer"][0]["px"]
            last_bid_offer["ask_vol"] = msg["offer"][0]["qty"]
            last_update = msg["offer"][0]["datetime"]
        
        last_bid_offer["last_update"] = last_update

        return last_bid_offer

    def on_open_connection_callback(self):
        # NOTE: called both in new connections and reconnections
        self.reset_internal_states()
        self.request_available_tickers_to_subscribe()
    
    def subscribe(self, tickers:list):
        self.ws.subscribe(tickers, n=1)

    def fill_last_event(self, ticker_list:list=None):
        if ticker_list:
            for ticker in ticker_list:
                self.ws.get_last_event([ticker])
        else:
            print(f'No ticker was provided, must provide a list of tickers!')

    def get_bid_offer(self):
        df = pd.DataFrame().from_dict(self.last_bid_and_offer_by_ticker).T
        return df

@st.cache_resource
def get_client():
    return CustomClient(API_KEY, data_subtype=DATA_SUBTYPE, ticker_list=TICKERS_OF_INTEREST)
client = get_client()

sleep(1)

with st.empty():
    while True:
        
        df = client.get_bid_offer()
        st.write(df)
        print(f"{datetime.datetime.now()}| Internal state summary : {client.internal_dict_state_summary()}")
        # print(set(client.available_to_subscribe) - set(list(client.last_bid_and_offer_by_ticker.keys())))

        sleep(1)