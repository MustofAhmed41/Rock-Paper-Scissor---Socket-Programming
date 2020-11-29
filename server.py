import socket
from _thread import *
import pickle
from game import Game

server = "192.168.0.107"
port = 5555

s = socket.socket(socket.AF_INET,
                  socket.SOCK_STREAM)  # AFNET means types of connection, SOCK_STREAM means how information is coming
# in.

try:
    s.bind((server, port))  # port might be busy then it might throw error, so encode in try except block
except socket.error as e:  # connecting server and port
    str(e)

s.listen()  # the parameter implies number of connection allows
print("Waiting for a connection, Server Started")

connected = set()  # store id of connected users
games = {}  # games is dictionary and is going to store games, it will have id as key and store game object as value
idCount = 0


def threaded_client(conn, p, gameId):  # gameId indicates which game in game dictionary
    global idCount  # if someone leaves or disconnects, so we need to keep track of that
    conn.send(str.encode(str(p)))  # connect initially, and sending value player, see network classes connect method
    # know if player 0 or 1

    reply = ""
    while True:  # we are going to send string data to our server from client, we are going send 1 of 3 different
        # options we are going to send set, or reset, or move get means get the game from server(every frame),
        # string get, server gets the game and sends it back reset means both player finished now reset the game on
        # the client side client makes a move, it send this information to server, update the game accordingly and
        # send game back to the client

        try:  # try catch because conn.recv... might cause problem sometimes

            data = conn.recv(4096).decode()  # if pickle data error, increase size 4096*2
            if gameId in games:  # every time we run loop, we check if game is still running by seeing if gameId is
                # still inside dictionary
                # if clients disconnects, we must delete it from games dictionary, or else we might lose game
                game = games[gameId]

                if not data:
                    break
                else:
                    if data == "reset":
                        game.resetWent()
                    elif data != "get":  # must be move
                        game.play(p, data)  # player and its move is passed as parameter

                    reply = game
                    conn.sendall(pickle.dumps(reply))  # sending our game in pickle form
            else:
                break
        except:
            break

    print("Lost connection")
    try:
        del games[gameId]  # if both players leave exactly same time it might cause issue to surround it with try catch
        print("Closing Game", gameId)
    except:
        pass
    idCount -= 1
    conn.close()


while True:  # this will continuously look for connection, continuously try to grab connection
    conn, addr = s.accept()  # this is conn is going to be the connection, addr will  be the ip address
    print("Connected to:", addr)
    idCount += 1  # keep count of how many connections to the server
    p = 0  # stands for current player
    gameId = (idCount - 1) // 2  # keeping track of number of games going on,  "//" means divides and floors the value

    if idCount % 2 == 1:  # if number of player is 3, id count is 3, then we say 2 players are already connected and
        # we need to create a new game
        games[gameId] = Game(gameId)
        print("creating a new game....")
    else:  # if we don't need to create a new game, just connect a user to a existing game
        games[gameId].ready = True  # preparing game
        p = 1  # player value is 1

    start_new_thread(threaded_client, (conn, p, gameId))

# if cannot run the server file then we mainly it might be because port number ex:5050 already being used
# so we need to kill port 5050. To do this
# do this in cmd prompt
# netstat -ano | findstr :5555
# then we will get o/p like this
#  TCP    192.168.0.103:5050     0.0.0.0:0              LISTENING       8680
#  UDP    0.0.0.0:5050           *:*                                    6772
# in output there might be more than 2 rows somethings, just try all number, (Mainly the row which has LISTENING will do the work)
# now try to destroy both 8680 and 6772, i am not sure which one but try to do with both if one dies it server will run again
# taskkill /PID 14444 /F       # if this fails try
# taskkill /PID 6772 /F
# o/p will be now
# SUCCESS: The process with PID 8680 has been terminated.
