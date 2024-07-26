import websocket
import json
import time
from env_var import *

def connect_to_websocket(ws_url):
    ws = websocket.WebSocket()
    try:
        ws.connect(ws_url)
        print("Connessione completata")
    except Exception as e:
        print(f"Connessione al web socket fallita :( {e}")
        return None
    return ws

def register_player(ws, player_id, player_name):
    try:
        if ws and ws.connected:
            ws.send(json.dumps({"action": "register", "playerId": player_id, "playerName": player_name}))
        else:
            print("La connessione non è aperta")
    except websocket.WebSocketConnectionClosedException as e:
        print("La connessione è stata interrotta")
        ws = reconnect(ws)
        if ws and ws.connected:
            ws.send(json.dumps({"action": "register", "playerId": player_id, "playerName": player_name}))

def send_message(ws, message):
    try:
        if ws and ws.connected:
            ws.send(json.dumps({"action": "sendmessage", "data": message}))
        else:
            print("La connessione non è aperta")
    except websocket.WebSocketConnectionClosedException as e:
        print("La connessione è stata interrotta")
        ws = reconnect(ws)
        if ws and ws.connected:
            ws.send(json.dumps({"action": "sendmessage", "data": message}))

def reconnect(ws):
    ws_url = ws.url  
    ws.close()
    new_ws = connect_to_websocket(ws_url)
    return new_ws
