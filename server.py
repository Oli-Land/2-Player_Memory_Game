from os import system
import json
from classes import Board, MyServer, Game



server = MyServer()

play = True
while play:
        
    game = Game()

    json_deck = json.dumps(game.board.deck)
    server.connection.sendall(bytes(json_deck, "utf-8"))


    while not game.is_game_finished():

        game.display_score()
        print("Player 1 turn...")

        current_input_1 = game.turn1()
        server.connection.sendall(bytes(current_input_1, "utf-8"))
        
        current_input_2 = game.turn2(current_input_1)
        server.connection.sendall(bytes(current_input_2, "utf-8"))

        game.match('p1', current_input_1, current_input_2)

        game.display_score()
        Board.display(game.board)
        print("Player 2 turn...")

        p2_selection_1_raw = server.connection.recv(1024)
        p2_selection_1 = p2_selection_1_raw.decode()
        system('clear')
        Board.display(game.board, flipped_cards=[p2_selection_1])
        print("Player 2 turn...")

        p2_selection_2_raw = server.connection.recv(1024)
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
            

server.sock.close()