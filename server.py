import socket
import random
from os import system
import time
import json
from classes import Board
from classes import Game


# instantiate socket class object with two arguments
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# associate socket with ip and port
server_socket.bind(("127.0.0.1", 65432))

# tell the socket what to do is listen
server_socket.listen()
print("Listening for incoming connection on port 65432")

# when a connection comes through,
# output a representation of connection and the address it has come from
connection, address = server_socket.accept()
print(f"Connected by {address}")





game = Game()

json_deck = json.dumps(game.board.deck)

# convert message to bytes, send
connection.sendall(bytes(json_deck, "utf-8"))


while not game.is_game_finished():

    print("Player 1 turn")
    current_input_1 = game.turn1()
    connection.sendall(bytes(current_input_1, "utf-8"))
    current_input_2 = game.turn2(current_input_1)
    connection.sendall(bytes(current_input_2, "utf-8"))
    game.match(current_input_1, current_input_2)

    print("Player 2 turn")
    p2_selection_1_raw = connection.recv(1024)
    p2_selection_1 = p2_selection_1_raw.decode()
    Board.display(game.board, flipped_cards=[p2_selection_1])

    p2_selection_2_raw = connection.recv(1024)
    p2_selection_2 = p2_selection_2_raw.decode()
    Board.display(game.board, flipped_cards=[p2_selection_1, p2_selection_2])

 
# print(f"Game over, {} wins! Final score is {}{}")




# server_socket.close()