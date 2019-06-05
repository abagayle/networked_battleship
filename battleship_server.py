import socket
from _thread import *
import sys

#server setup with sockets and such
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server = ''
port = 43500

server_ip = socket.gethostbyname(server)

try:
    s.bind((server, port))

except socket.error as e:
    print(str(e))

s.listen(2)
print("Waiting for a connection")

currentId = "0"

#tracks the player hits
player1Hits = 0
player2Hits = 0

#defines the player ships
player1Ships = 0
player2Ships = 0

#defines the ship objects that hold the data. So each grid is a ship
player1_ships = []
player2_ships = []

#For loops below define the grids to define size of it
for row in range(10):
    player1_ships.append([])
    for column in range(10):
        player1_ships[row].append(0)
                
for row in range(10):
    player2_ships.append([])
    for column in range(10):
        player2_ships[row].append(0)


#defines and tracks the hits
player1_hits = []
player2_hits = []

#defines the hit grid tracking
for row in range(10):
    player1_hits.append([])
    for column in range(10):
        player1_hits[row].append(0)
                
for row in range(10):
    player2_hits.append([])
    for column in range(10):
        player2_hits[row].append(0)

#creates the threades via a connection 
def threaded_client(conn):
    global currentId, player1Hits, player2Hits, player1_hits, player2_hits, player1_ships, player2_ships, player1Ships, player2Ships
    conn.send(str.encode(currentId))
    currentId = "1"
    reply = ''
    
    #main while loop to run the server, is True to keep it running
    while True:
        try:
        
            #Receive data
            data = conn.recv(2048)
            reply = data.decode('utf-8')
            if not data:
                conn.send(str.encode("Goodbye"))
                break
            else:
            
                #we ack that we got the data and then split it up as needed
                print("Recieved: " + reply)
                reply = reply.split("|")               
                if reply[0] == "SET":
                    arr = reply[1].split(":")                        
                    id = int(arr[0])
                    arr = arr[1].split(",")
                    row = int(arr[0])
                    col = int(arr[1])
                    
                   #Checks for ids of the player and updates accordingly
                    if id == 0:
                        player1_ships[row][col] = 1
                        player1Ships = player1Ships + 1
                    else:
                        player2_ships[row][col] = 1
                        player2Ships = player2Ships + 1
                        
                    #Ships are set, and it sends an ack    
                    if(player1Ships == 10 or player2Ships == 10):
                        if player1Ships == 10:
                            message = "ALL SHIPS SET"
                        elif player2Ships == 10:
                            message = "ALL SHIPS SET"
                            
                        if player1Ships == 10 and player2Ships == 10:
                            message = "BOTH SIDES READY"
                    else:
                        message = "SET 1 SHIP"
                           
                elif(reply[0] == "HIT"):
                   
                    #More splitting
                    arr = reply[1].split(":")                        
                    id = int(arr[0])
                    arr = arr[1].split(",")
                    row = int(arr[0])
                    col = int(arr[1])
                    
                    print(str(id))
                    
                    #updates player with id 0
                    if id == 0:
                        if player2_ships[row][col] == 1:
                            player1_hits[row][col] = 2
                            message = "Success"
                            global player1Hits
                            player1Hits = player1Hits + 1
                        else:
                            player1_hits[row][col] = 3
                            message = "Fail"
                    else:
                        if player1_ships[row][col] == 1:
                            player2_hits[row][col] = 2
                            message = "Success"
                            global player2Hits
                            player2Hits = player2Hits + 1
                        else:
                            player2_hits[row][col] = 3
                            message = "Fail"
                elif(reply[0] == "ASK"):
                    if player1Ships == 10 and player2Ships == 10:
                            message = "BOTH SIDES READY"
                    else:
                        message = "WAIT"
                else:
                    message = "UNKNOWN"
                
                #We get 10 hits, we get a win
                if(player1Hits == 10):
                    message = "1 WON"
                elif(player2Hits == 10):
                    message = "2 WON"
                    
                
                if id == 0: nid = 1
                if id == 1: nid = 0
                
                reply = str(nid) + ": " + message

                print("Sending: " + reply)

            conn.sendall(str.encode(reply))
        except ValueError:
            print("except " + ValueError)
            break

    print("Connection Closed")
    conn.close()
    player1_hits = []
    player2_hits = []
    
    player1_ships = []
    player2_ships = []
    
    player1Hits = 0
    player2Hits = 0

    player1Ships = 0
    player2Ships = 0

#runs threads and establishes connections     
while True:
    conn, addr = s.accept()
    print("Connected to: ", addr)

    start_new_thread(threaded_client, (conn,))