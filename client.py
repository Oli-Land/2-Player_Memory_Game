import socket
import random
from os import system
import time
import json
from classes import Board
from classes import Game



client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("127.0.0.1", 65432))

game = Game()

while True:
    
        
    json_deck = client_socket.recv(1024)
    
    game.board.deck = json.loads(json_deck)
    print(game.board.deck)

    input("continue")

""" while not Game.is_game_finished(game):
    print("Player 1 turn")
    p1_selection_1 = client_socket.recv(1024)
    Board.display(game.board, flipped_cards=[p1_selection_1])
    p1_selection_2 = client_socket.recv(1024)
    Board.display(game.board, flipped_cards=[p1_selection_1, p1_selection_2])
    print("Player 2 turn")
    game.turn()
     """
    
