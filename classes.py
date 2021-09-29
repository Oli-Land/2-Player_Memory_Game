import random
from os import system
import time
import socket
import json
import sys




class Board:
    def __init__(self):
        self.deck = {}
        symb_lib = ["@", "#", "$", "%", "<", "&", ">", "?"]
        symbs = symb_lib * 2
        random.shuffle(symbs)
        # iterative card generator
        for letter in ['a', 'b', 'c', 'd']:
            for number in ['1', '2', '3', '4']:
                # each card is a nested dictionary named after a board coordinate
                self.deck[letter + number] = {}
                # a symbol value
                self.deck[letter + number]['Value'] = symbs.pop()
                # a boolean for its matched status
                self.deck[letter + number]['Matched'] = False



    def display(self, flipped_cards=[]):
        """ Prints a 4x4 grid of cards from the board dictionary.
        Each 'card' shows up blank by default.
        Prints a card's value when the function is handed a card's name as an argument,
        or when the card's matched status equals True
        
        Inputs: 2 digit board coordinate eg b3
        """
        print(f"Selected: {flipped_cards}")
        print("    1   2   3   4")
        print("  -----------------")
        for letter in ['a', 'b', 'c', 'd']:
            print(letter + ' | ', end="")
            for number in ['1', '2', '3', '4']:
                if (letter + number) in flipped_cards:
                    print(self.deck[letter + number]['Value'] + " | ", end="")
                elif self.deck[letter + number]['Matched'] == True:
                    print(self.deck[letter + number]['Value'] + " | ", end="")
                else:
                    print(" " + " | ", end="")
            print("")
            print("  -----------------")


    def is_game_finished(self):
        """ Checks for the game win condition.
        
        Returns: True when all cards have Matched == True
        """

        for letter in ['a', 'b', 'c', 'd']:
            for number in ['1', '2', '3', '4']:
                if self.deck[letter + number]['Matched'] == False:
                    return False
        return True


class Game:

    def __init__(self):

        self.board = Board()

        self.p1_score = 0
        self.p2_score = 0

    def is_game_finished(self):
        """ Checks for the game win condition.
        
        Returns: True when all cards have Matched == True
        """

        for letter in ['a', 'b', 'c', 'd']:
            for number in ['1', '2', '3', '4']:
                if self.board.deck[letter + number]['Matched'] == False:
                    return False
        return True

    def is_invalid_input(input, previous_input = ""):
        """ Error checking function: checks input for each turn is valid.
        Returns: False on valid input to break loop
        """

        # default string to enter loop. 
        if input == "catch":
            return True

        # exit game if player inputs "exit"    
        if input == "exit":
            return False

        # check for valid input
        if len(input) != 2:
            print("Please enter coordinates as 2 digits (letter,number)")
            return True
        elif input[0] not in ['a', 'b', 'c', 'd']:
            print("Please enter a valid row (a, b, c or d)")
            return True
        elif input[1] not in ['1', '2', '3', '4']:
            print("Please enter a valid column (1, 2, 3 or 4)")
            return True

        # check that input 2 doesn't equal input 1
        if input == previous_input:
            print("Please select a different card for Turn 2")
            return True
            
        return False

    def turn(self):
        
        system('clear')
        Board.display(self.board)
        # -- Turn 1 --
        current_input_1 = "catch"
        # input stage loops until valid input entered. Hands input to error checking function
        while Game.is_invalid_input(current_input_1):
            current_input_1 = input("Enter coordinates of first selection (a-d)(1-4): ")
        if current_input_1 == "exit":
            print("Exited game")
            sys.exit(0)

        system('clear')
        Board.display(self.board, flipped_cards=[current_input_1])

    
        current_input_2 = "catch"
        while Game.is_invalid_input(current_input_2, current_input_1):
            current_input_2 = input("Enter coordinates of second selection (a-d)(1-4): ")
        if current_input_1 == "exit":
            print("Exited game")
            sys.exit(0)

        system('clear')
        # second Turn print board shows both selected cards revealed
        Board.display(self.board, flipped_cards=[current_input_1, current_input_2])

        # conditional structure tests for matched pairs and sets their Matched boolean to True
        if self.board.deck[current_input_1]['Value'] == self.board.deck[current_input_2]['Value']:
            self.board.deck[current_input_1]['Matched'] = True
            self.board.deck[current_input_2]['Matched'] = True
            print("Correct match!")
            self.p1_score += 1
        else:
            print("No match, please try again")

        time.sleep(2)












    





class ServerSocket:
    def __init__(self, ip = "127.0.0.1" , port = 65432):

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        sock.bind((ip, port))

        sock.listen()

    def accept():
        """ accept() -> (socket object, address info)

        Wait for an incoming connection. Return a new socket representing the connection, and the address of the client. For IP sockets, the address info is a pair (hostaddr, port). """
        socket.socket.accept()