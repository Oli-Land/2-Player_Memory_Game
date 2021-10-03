import socket
from os import system
import json
from classes import Board, MyClient
from classes import Game



client = MyClient()

play = True
while play:

    # Instantiate new game
    # Receive card deck from server as JSON
    # Overwrite local game deck
    # (Both players track their own identical instance of the game)    
    game = Game()
    json_deck = client.sock.recv(1024)
    game.board.deck = json.loads(json_deck)

    # Main turn loop cycles until win condition is met
    while not game.is_game_finished():

        # ----------------------Player 1 Turn---------------------- #
        # Wait while player 1 takes their turn.

        game.display_score()
        Board.display(game.board)
        print("Player 1 turn...")

        # Receive player 1's moves over network.
        p1_selection_1_raw = client.sock.recv(1024)  
        p1_selection_1 = p1_selection_1_raw.decode()
        
        # Display local board instance with player 1's moves 
        system('clear')
        Board.display(game.board, flipped_cards=[p1_selection_1])
        print("Player 1 turn...")

        p1_selection_2_raw = client.sock.recv(1024)
        p1_selection_2 = p1_selection_2_raw.decode()
        system('clear')
        Board.display(game.board, flipped_cards=[p1_selection_1, p1_selection_2])
        
        # Check for match and attribute any point to player 2
        game.match('p1', p1_selection_1, p1_selection_2)

        # ----------------------Player 2 Turn---------------------- #
        # Take turn while player 1 waits.

        game.display_score()
        print("Player 2 turn...")

        # Send moves over network to also be displayed for player 2
        current_input_1 = game.turn1()
        client.sock.sendall(bytes(current_input_1, "utf-8"))

        current_input_2 = game.turn2(current_input_1)
        client.sock.sendall(bytes(current_input_2, "utf-8"))
        
        # Check for match and attribute any point to player 2
        game.match('p2', current_input_1, current_input_2)

    game.game_over()
        
    # play again prompt loop
    again = True
    while again:

        again_prompt = input("Do you want to play again? y/n: ")
        
        if again_prompt == "y":
            again = False
        elif again_prompt == "n":
            play = False
            again = False
            

client.sock.close()
