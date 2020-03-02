#!/usr/bin/env python3

import socket
import json
import struct

def send_message(socket, msg):
    msg_bytes = str.encode(json.dumps(msg))
    header = struct.pack("!H", len(msg_bytes))
    socket.sendall(header + msg_bytes)

def recieve_message(socket):
    msg_size_bytes = socket.recv(2)
    (msg_size,) = struct.unpack("!H", msg_size_bytes)
    message = socket.recv(msg_size)
    return message

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect(('localhost', 4001))

send_message(socket, {'token': '2goiwcgmljrkuafvgml2klmtqymfebso', 'lobby': 'foo'})
msg = recieve_message(socket)
connection_message = json.loads(msg)
print("bot_id:", connection_message["bot_id"])
print("connection_id:", connection_message["connection_id"])

send_message(socket, {'action': 'start_match_making'})
msg = recieve_message(socket)
status = json.loads(msg)
print("status:", status["status"])

msg = recieve_message(socket)
decoded = json.loads(msg)
print("Recieved Request:", decoded["request_type"])
print("game_id:", decoded["game_info"]["game_id"])
print("player:", decoded["game_info"]["player"])

send_message(socket, {"action": "accept_game", "game_id": decoded["game_info"]["game_id"]})

for i in range(0, 100):
    msg = recieve_message(socket)
    decoded = json.loads(msg)
    print(i, ": Recieved Request:", decoded["request_type"], "moves_request_id", decoded["moves_request"]["request_id"])
    send_message(socket, {"action": "send_moves", "request_id": decoded["moves_request"]["request_id"], "moves": []})

msg = recieve_message(socket)
decoded = json.loads(msg)
print("Game Over:", decoded["info"])
print("Result: ", decoded["result"]["score"])

