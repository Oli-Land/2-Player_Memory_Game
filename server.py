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

print(connection)

game = Game()

while True:
    

    json_deck = json.dumps(game.board.deck)
    
    # convert message to bytes, send
    connection.sendall(bytes(json_deck, "utf-8"))


""" while not Game.is_game_finished(game):
    print("Player 1 turn")
    game.turn()
    print("Player 2 turn")
    p2_selection_1 = connection.recv(1024)
    Board.display(game.board, flipped_cards=[p2_selection_1])
    p2_selection_2 = connection.recv(1024)
    Board.display(game.board, flipped_cards=[p2_selection_1, p2_selection_2])
 """
# print(f"Game over, {} wins! Final score is {}{}")




# server_socket.close()