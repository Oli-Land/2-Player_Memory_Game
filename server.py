from os import system
import json
from classes import Board, MyServer, Game



server = MyServer()

# Play again loop
play = True
while play:

    # Instantiate new game, send card deck to client as JSON
    # (Both players track their own identical instance of the game)
    game = Game()
    json_deck = json.dumps(game.board.deck)
    server.connection.sendall(bytes(json_deck, "utf-8"))

    # Main turn loop cycles until win condition is met
    while not game.is_game_finished():

        # ----------------------Player 1 Turn---------------------- #
        # Take turn while player 2 waits.

        game.display_score()
        print("Player 1 turn...")
        
        # Send moves over network to also be displayed for player 2
        current_input_1 = game.turn1()
        server.connection.sendall(bytes(current_input_1, "utf-8"))
        
        current_input_2 = game.turn2(current_input_1)
        server.connection.sendall(bytes(current_input_2, "utf-8"))

        # Check for match and attribute any point to player 1
        game.match('p1', current_input_1, current_input_2)

        # ----------------------Player 2 Turn---------------------- #
        # Wait while player 2 takes their turn.

        game.display_score()
        Board.display(game.board)
        print("Player 2 turn...")

        # Receive player 2's moves over network.
        p2_selection_1_raw = server.connection.recv(1024)
        p2_selection_1 = p2_selection_1_raw.decode()
        
        # Display local board instance with player 2's moves
        system('clear') 
        Board.display(game.board, flipped_cards=[p2_selection_1])
        print("Player 2 turn...")

        p2_selection_2_raw = server.connection.recv(1024)
        p2_selection_2 = p2_selection_2_raw.decode()
        system('clear')
        Board.display(game.board, flipped_cards=[p2_selection_1, p2_selection_2])

        # Check for match and attribute any point to player 2
        game.match('p2', p2_selection_1, p2_selection_2)

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
            

server.connection.close()