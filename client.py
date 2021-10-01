import socket
from os import system
import json
from classes import Board
from classes import Game



client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("127.0.0.1", 65432))

play = True
while play:
        
    game = Game()

    json_deck = client_socket.recv(1024)

    game.board.deck = json.loads(json_deck)

    while not game.is_game_finished():

        game.display_score()
        print("Player 1 turn...")
        Board.display(game.board)

        p1_selection_1_raw = client_socket.recv(1024)  
        p1_selection_1 = p1_selection_1_raw.decode()
        system('clear')
        Board.display(game.board, flipped_cards=[p1_selection_1])

        p1_selection_2_raw = client_socket.recv(1024)
        p1_selection_2 = p1_selection_2_raw.decode()
        system('clear')
        Board.display(game.board, flipped_cards=[p1_selection_1, p1_selection_2])
        game.match('p1', p1_selection_1, p1_selection_2)

        game.display_score()
        print("Player 2 turn...")

        current_input_1 = game.turn1()
        client_socket.sendall(bytes(current_input_1, "utf-8"))

        current_input_2 = game.turn2(current_input_1)
        client_socket.sendall(bytes(current_input_2, "utf-8"))

        game.match('p2', current_input_1, current_input_2)

    game.game_over()
        
    # play again loop
    again = True
    while again:

        again_prompt = input("Do you want to play again? Y/n: ")
        
        if again_prompt == "y":
            again = False
        elif again_prompt == "n":
            play = False
            again = False
            

client_socket.close()
