# ~/VSCode/testing/T2A3/network


# those two handy commands for dealing with locked-up sockets:

# ps -ef|grep python
# kill -9 <process_id_goes_here>




board = board()

while play:

    p1_turn1()
    board.send()

    p1_turn2()
    board.send()

    board.match()
    board.send()

    p2_turn1()
    board.send()

    p2_turn2()
    board.send()

    board.match()
    board.send()



