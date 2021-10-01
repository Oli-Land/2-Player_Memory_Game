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

json_deck = client_socket.recv(1024)

game.board.deck = json.loads(json_deck)




while not game.is_game_finished():

    print("Player 1 turn...")

    p1_selection_1_raw = client_socket.recv(1024)  
    p1_selection_1 = p1_selection_1_raw.decode()
    Board.display(game.board, flipped_cards=[p1_selection_1])

    p1_selection_2_raw = client_socket.recv(1024)
    p1_selection_2 = p1_selection_2_raw.decode()
    Board.display(game.board, flipped_cards=[p1_selection_1, p1_selection_2])

    game.match('p1', p1_selection_1, p1_selection_2)


    print("Player 2 turn...")

    current_input_1 = game.turn1()
    client_socket.sendall(bytes(current_input_1, "utf-8"))

    current_input_2 = game.turn2(current_input_1)
    client_socket.sendall(bytes(current_input_2, "utf-8"))

    game.match('p2', current_input_1, current_input_2)

print("Game Over!")
print(f"Final score for Player 1: {game.p1_score} points")
print(f"Final score for Player 2: {game.p2_score} points")
if game.p1_score > game.p2_score:
    print(f"Player 1 wins!")
elif game.p2_score > game.p1_score:
    print(f"Player 2 wins!")
elif game.p1_score == game.p2_score:
    print(f"It's a draw!")
    

