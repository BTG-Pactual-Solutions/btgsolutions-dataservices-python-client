import btgsolutions_dataservices as btg
from time import sleep
import json
import math

API_KEY = "PUT_YOUR_API_KEY_HERE"

tickers_under_control = []

class WSTradesPool():
  def __init__(self, callback_fn, number_of_connections, api_key, data_type, data_subtype):
    self.api_key = api_key
    self.data_type = data_type
    self.data_subtype = data_subtype
    self.number_of_connections = number_of_connections
    self.callback_fn = callback_fn
    self.ws_connection_map = {} # key: connection id | value: ws object
    self.ws_instrument_map = {} # key: connection id | value: slice of list of desired instruments
    self.__initialize_websockets()

  def __chunks(self, lst, n):
    """ Generate N chunks of equal size from list."""
    size_per_chunk = math.ceil(len(lst)/n)
    for i in range(0, len(lst), size_per_chunk):
        yield lst[i:i + size_per_chunk]

  def __initialize_websockets(self):
    for i in range(self.number_of_connections):
      ws_trades_instance = btg.MarketDataWebSocketClient(
        api_key=API_KEY,
        data_type='trades',
        data_subtype="options",
        instruments=[]
      )
      ws_trades_instance.run(on_message=self.callback_fn)
      self.ws_connection_map[i] = ws_trades_instance
  
  def available_to_subscribe(self,):
    self.ws_connection_map[0].available_to_subscribe()

  def subscribe(self, list_of_instruments):
    for i, instrument_chunk in enumerate(self.__chunks(list_of_instruments, self.number_of_connections)):
      self.ws_connection_map[i].subscribe(instrument_chunk)
      if i in self.ws_instrument_map:
        self.ws_instrument_map[i] += instrument_chunk
      else:
        self.ws_instrument_map[i] = instrument_chunk

  def get_last_event(self, ticker):
    self.get_ws_that_controls_instrument(ticker).get_last_event(ticker)

  def get_last_event_all_tickers(self):
    for ws_id, instrument_chunk in self.ws_instrument_map.items():
      for ticker in instrument_chunk:
        self.ws_connection_map[ws_id].get_last_event(ticker)

  def get_ws_that_controls_instrument(self, ticker):
    for ws_id, instrument_chunk in self.ws_instrument_map.items():
      if ticker in instrument_chunk:
        return self.ws_connection_map[ws_id]

def handle_ws_trades_message(msg):
  parsed_msg = json.loads(msg)
  event_type = parsed_msg["ev"]

  if event_type == "message":
    print(f"""{parsed_msg["status"]}: {parsed_msg["message"]}""")
  elif event_type == "available_to_subscribe":
    tickers_under_control = parsed_msg["message"]
    ws_trades_pool.subscribe(tickers_under_control)
  elif event_type == "trade":
    print(f"Trade event: {parsed_msg}")
  else:
    raise Exception(f"Unhandled event type {event_type} coming from ws_trades.")

def handle_ws_securities_message(msg):
  new_security_symbol = json.loads(msg)["Symbol"]
  tickers_under_control += [new_security_symbol]
  ws_trades_pool.subscribe([new_security_symbol])

# Receive trades
ws_trades_pool = WSTradesPool(
  callback_fn=handle_ws_trades_message,
  number_of_connections=10,
  api_key=API_KEY,
  data_type="trades",
  data_subtype="options"
)

# Receive new intraday created instruments
ws_securities = btg.MarketDataWebSocketClient(
  api_key=API_KEY,
  data_type='securities',
  data_subtype='options'
)
ws_securities.run(on_message=handle_ws_securities_message)

# Wait for connection. The package does not support await yet.
sleep(5)
ws_trades_pool.available_to_subscribe()

while True:
  sleep(1)