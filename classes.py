""" This module contains the classes which 2Oli2Land server.py and client.py depend upon.

    Classes:
    Board
    Game
    MyServer
    MyClient
"""

import random
from os import system
import time
import socket
import sys


class Board:
    """ Contains methods for generating and displaying the game board.

    Methods:
        __init__(): Inits the board's deck
        display(self, flipped_cards=[]): Displays the game board

    Attributes:
            deck: A dictionary of cards named after board coordinates.
                Each card is a nested dictionary containing its symbol value
                and its matched status boolean.

    """

    def __init__(self):
        """ Inits a Board class object with a deck attribute.

        Shuffles the library of symbols and
        iterates over all board coordinates, creating dictionaries
        for each card and pops a symbol to each.

        """

        self.deck = {}
        symb_lib = ["@", "#", "$", "%", "<", "&", ">", "?"]
        symbs = symb_lib * 2
        random.shuffle(symbs)
        for letter in ['a', 'b', 'c', 'd']:
            for number in ['1', '2', '3', '4']:
                self.deck[letter + number] = {}
                self.deck[letter + number]['Value'] = symbs.pop()
                self.deck[letter + number]['Matched'] = False


    def display(self, flipped_cards=[]):
        """ Prints a 4x4 grid containing cards from the board deck.

        Each 'card' shows up blank by default.
        Prints a card's symbol value when the function is handed
        a card's key as an argument, or when the card's 
        Matched boolean is True.

        Args:
            flipped_cards: A list containing one or two strings of
                2-digit board coordinates provided from player input eg [b3, c4]
        """
        print("")
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
        print("")


class Game:
    """ Contains methods for gameplay.

    Attributes:
        board: See Board class
        p1_score: An integer storing player 1 score
        p2_score: An integer storing player 2 score

    Methods:
        __init__: Inits the game
        is_game_finished(self): Checks for game win condition
        is_invalid_input(self, input, previous_input = ""):
            Checks user inputs are valid
        turn1(self): First turn of each round
        turn2(self, current_input_1): Second turn of each round
        match(self, current_player, current_input_1, current_input_2):
            Checks if turn1 and turn2 selections match
        display_score(self): Prints player scores
        game_over(self): Prints end of game message and player scores

    """


    def __init__(self):
        """ Inits the game by creating an instance of the Board class.
        
        Sets scores of players to 0 and prints the game rules

        """

        self.board = Board()
        self.p1_score = 0
        self.p2_score = 0

        print("""\n       
        Welcome to 2Oli2Land!

        This is a 2 player game of memory
        Test your short term memory against a friend or foe
        Server is player 1, Client is player 2

        Choose a card on the board to view its symbol
        Input board coordinates for card choice as (row)(column) eg. b3
        Take turns trying to match pairs of cards
        Each pair matched awards 1 point
        Have fun!
        (Type "exit" to exit game)

        """)
        

    def is_game_finished(self):
        """ Checks the game's card deck for the win condition.

        Returns: True when all cards' Matched booleans are True

        """
        for letter in ['a', 'b', 'c', 'd']:
            for number in ['1', '2', '3', '4']:
                if self.board.deck[letter + number]['Matched'] == False:
                    return False
        return True


    def is_invalid_input(self, input, previous_input = ""):
        """ Checks input for each turn is valid.

        Args:
            input: User input string handed from turn1() and turn2() methods.
            previous_input: Input from turn1(). Compared to input from
                turn2() for prevention of wasting turn 2.

        Returns: False on valid input to break turn's input loop
        """

        # default string to enter loop 
        if input == "catch":
            return True

        # "exit" is valid input
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

        # check that selection hasn't already been matched
        if self.board.deck[input]['Matched'] == True:
            print("Selected card is already matched. Please select a different card")
            return True    

        # check that turn2() input is different to turn1() input
        if input == previous_input:
            print("Please select a different card for Turn 2")
            return True
    
        return False


    def turn1(self):
        """ First of each players' 2 turns.
        
        Takes user input as a string and calls Board.display() 
        with the selected card revealed.

        Returns: User input selection as string to be handed to turn2(),
            match() to check for matching selection,
            and also sent across the network to show the other player
        
        """
        
        Board.display(self.board)

        current_input_1 = "catch"
        while Game.is_invalid_input(self, current_input_1):
            current_input_1 = input("Enter coordinates of first selection (a-d)(1-4): ")
        if current_input_1 == "exit":
            print("Exited game")
            sys.exit(0)

        system('clear')
        Board.display(self.board, flipped_cards=[current_input_1])

        return current_input_1
        
    def turn2(self, current_input_1):
        """ Second of each players' 2 turns.
        
        Takes user input as a string and calls Board.display() 
        with both selected cards revealed.

        Returns: User input selection as string to be handed to
            match() to check for matching selection,
            and also sent across the network to show the other player
        
        """

        current_input_2 = "catch"
        while Game.is_invalid_input(self, current_input_2, current_input_1):
            current_input_2 = input("Enter coordinates of second selection (a-d)(1-4): ")
        if current_input_1 == "exit":
            print("Exited game")
            sys.exit(0)

        system('clear')
        Board.display(self.board, flipped_cards=[current_input_1, current_input_2])
        
        return current_input_2


    def match(self, current_player, current_input_1, current_input_2):
        """ Tests for matched pairs and sets their Matched boolean to True.

        Takes input from turn1() and turn2() and tests equality.
        Upon correct match, accesses the game board's deck and
        changes both cards' Matched boolean to True and
        increments score of current player by 1. Pauses the game for 2 seconds
        to allow both players a limited time viewing revealed cards.

        Args:
            current_player: String tracking current player for scoring purposes.
            current_input_1: User input string from turn1().
            current_input_2: User input string from turn2().

        """

        if self.board.deck[current_input_1]['Value'] == self.board.deck[current_input_2]['Value']:
            self.board.deck[current_input_1]['Matched'] = True
            self.board.deck[current_input_2]['Matched'] = True
            print("Correct match!")

            if current_player == 'p1':
                self.p1_score += 1
            elif current_player == 'p2':
                self.p2_score += 1

            if self.p1_score > self.p2_score:
                print(f"Player 1 is in the lead with {self.p1_score} points!")
            elif self.p2_score > self.p1_score:
                print(f"Player 2 is in the lead with {self.p2_score} points!")
            elif self.p1_score == self.p2_score:
                print(f"Score is tied at {self.p1_score} points!")
        
        else:
            print("No match...")

        time.sleep(2)
        system('clear')


    def display_score(self):

        print(f"\nPlayer 1 Score: {self.p1_score} points")
        print(f"Player 2 Score: {self.p2_score} points\n")


    def game_over(self):
        """ Displays both players' final scores and who is the winner """

        print("Game Over!")
        print(f"Final score for Player 1: {self.p1_score} points")
        print(f"Final score for Player 2: {self.p2_score} points")
        if self.p1_score > self.p2_score:
            print(f"Player 1 wins!")
        elif self.p2_score > self.p1_score:
            print(f"Player 2 wins!")
        elif self.p1_score == self.p2_score:
            print(f"It's a draw!")


class MyServer:
    """ Sets up the server socket for networked play.

    Instantiates the server's socket object using the python standard socket library
    with AddressFamily AF_INET and SocketKind SOCK_STREAM.
    Finds the host IP and associates the socket with the IP and
    the arbitrary port 65444. Tells the socket to listen and
    accept incoming connection from the client.

    Attributes:
        connection: A socket configured to send data to the client.
        address: Tuple representing client address (IP, port)

    """


    def __init__(self):

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)

        port = 65444

        sock.bind((ip, port))

        sock.listen()
        print(f"Server IP is: {ip}")
        print(f"Listening for incoming connection on port {port}")

        self.connection, self.address = sock.accept()
        print(f"Connected by {self.address}")


class MyClient:
    """ Sets up the client socket for network play.

    Instantiates the client socket object using the python standard socket library
    with AddressFamily AF_INET and SocketKind SOCK_STREAM. Accepts user input for
    server IP address (displayed on server's screen when program loads) and sets port to 65444.
    
    Attributes:
        sock: A socket configured to send data to the server

    """

    def __init__(self):

        ip = input("Input server IP: ")
        port = 65444

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((ip, port))
        print(f"Connected to {ip}, {port}")





        

