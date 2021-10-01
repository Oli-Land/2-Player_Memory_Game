import socket
from os import system
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

play = True
while play:
        
    game = Game()

    json_deck = json.dumps(game.board.deck)

    # convert message to bytes, send
    connection.sendall(bytes(json_deck, "utf-8"))


    while not game.is_game_finished():

        game.display_score()
        print("Player 1 turn...")

        current_input_1 = game.turn1()
        connection.sendall(bytes(current_input_1, "utf-8"))
        
        current_input_2 = game.turn2(current_input_1)
        connection.sendall(bytes(current_input_2, "utf-8"))

        game.match('p1', current_input_1, current_input_2)

        game.display_score()
        print("Player 2 turn...")
        Board.display(game.board)

        p2_selection_1_raw = connection.recv(1024)
        p2_selection_1 = p2_selection_1_raw.decode()
        system('clear')
        Board.display(game.board, flipped_cards=[p2_selection_1])

        p2_selection_2_raw = connection.recv(1024)
        p2_selection_2 = p2_selection_2_raw.decode()
        system('clear')
        Board.display(game.board, flipped_cards=[p2_selection_1, p2_selection_2])

        game.match('p2', p2_selection_1, p2_selection_2)

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
            

server_socket.close()