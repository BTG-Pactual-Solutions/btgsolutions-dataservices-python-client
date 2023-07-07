import json 

def _on_message(message):
    print(json.loads(message))

def _on_error(error):
    print(f'### Error: {error} ###')

def _on_close(close_status_code, close_msg):
    print("### Closed Connection ###")

def _on_open():
    print("### Open Connection ###")
