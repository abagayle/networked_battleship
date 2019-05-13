# This file is the server code for the chat program.
# It contains an input handler to handle all server input
# as well as a client manager to handle all the client input and broadcasting
# it handles both of these using threading to be able to manage each at the same time 

from socket import *
from threading import Thread
import os
import sys

#Client list - keeps track of clients that are connected
clients = []

#global variables for commands 
welcome_message = "\nWelcome to the chat! Type list() to see who is online! Reference the README for other commands."


def startBattleship(client_initiate, client_receiver)


# server input handler - handles commands given through the server command line. Will be own thread.
# Parameters: serverSocket - the socket connection used for the server itself
# No returns - just prints and changes global variables or closes the server
def serverInputHandler(serverSocket):
	global starwars_bot_flag
	global joke_bot_flag
	while 1:
		# 
		command = input('Enter "list()" to list users, or "close()" to end the server run. Reference the README for other commands\n')
		
		#This command is for listing every client currently connected to teh server. 
		if command == "list()":
			for i in range(0, len(clients)):
				if clients[i][2] == 0:
					print("Name: %s IP: %s Port: %s" %(clients[i][1],clients[i][3],serverPort))		
		#This command changes the welcome message.	
		elif "welcome(" in command:
			new_message = command.split('welcome(')
			new_message = new_message[1].split(')')
			new_message = new_message[0]
			global welcome_message
			welcome_message = new_message
			print("Welcome message successfully changed from default for this server iteration")
		#closes server by first closing all client connections and then breaking out of the while to close the server socket and exiting			
		elif command == "close()":
			for i in range(0, len(clients)):
				if clients[i][2] == 0:
					clients[i][0].close()
			
			break
			
	serverSocket.close()
	os._exit(0)
	
# this method handles the client interactions and broadcasts as well as client commands. Will be separate thread for each client.
# Parameters: connectionSocket - a client connection, client_nume - the client position in the client list
# No returns - just prints and sends over connections or closes a connection
def clientManager(connectionSocket, client_num):
	
	battleships = []
	hits = []

	try:
		#recieves a message (the clients name) from the client and decodes it
		message = connectionSocket.recv(1024).decode()
		
		#stores the client's name in the client list
		clients[client_num][1] = message
		
		#prints the client name on the server and informs client that they are online, as well as giving them the welcome message. 
		identify = "Client %s is online." % (message)
		print(identify)
		identify += "\n"
		identify += welcome_message
		connectionSocket.send(identify.encode())
		
		#loop for handling future client input
		while 1:
			#recieves client message
			message = connectionSocket.recv(1024).decode()
			
			#prints their message to the server
			server_response = "%s: %s" % (clients[client_num][1],message)
			print(clients[client_num][1], " sent: ", message)
			
			#if statements to determine if the client typed a command or is just chatting
			#if name( is used, then the client is requesting to change their name.
			if "name(" in message:
				#find the new name by splitting up the string
				new_name = message.split('name(')
				new_name = new_name[1].split(')')
				new_name = new_name[0]
				name_change = "%s changed to: %s"%(clients[client_num][1],new_name)
				clients[client_num][1] = new_name
				print("New name is: ", new_name)
				for i in range(0, len(clients)):
					if clients[i][2] == 0:
						clients[i][0].send(name_change.encode())
			#client wants list of everyone online		
			elif "list()" in message:
				for i in range(0, len(clients)):
					if clients[i][2] == 0:
						send_list = "Name: %s IP: %s Port: %s"%(clients[i][1],clients[i][3],serverPort)
						clients[client_num][0].send(send_list.encode())	
			elif "battleship(" in message:
				name_of_player = messsge.split('battleship(')
				name_of_player = name_of_player[1].split(')')
				name_of_player = name_of_player[0]
				
				player_num = -1
				
				#find player with that name in client list
				for i in range(0, len(clients)):
					if clients[i][1] == name_of_player:
						player_num = i
			
				if player_num != -1:
					startBattleship(client_num, player_num)
				else:
					no_player = "There is no player online by the name of " + name_of_player
					print(no_player)
					clients[i][0].send(no_player.encode())
			elif "target(" in message:
				coordinates = message.split('target(')
				coordinates = coordinates[1].split(')')
				coordinates = coordinates[0]
				
				if "," in coordinates:	
					num1 = coordinates.split(',')[0]
					num2 = coordinates[1]
				
				else:
					wrong = "Wrong formate for coordinates"
					print(wrong)
					clients[i][0].send(wrong.encode())
				
				
				
				
			else:
				for i in range(0, len(clients)):
					if clients[i][2] == 0 and client_num != i:
						clients[i][0].send(server_response.encode())
				#if they close their connection, then client breaks out of loop and closes connection socket and exits
				if message == "close()":
					clients[client_num][2]=-1
					print(clients[client_num], " has left the chat.")
					break
					
		connectionSocket.close()
	except:
		os._exit(0)
				

#gathers system arguments in command line to use for IP/hostname and port number 
if len(sys.argv) < 3:
	print("Please use all the arguments: python script, IP address or hostname, port number")
	exit()

ip_address_or_hostname = str(sys.argv[1])
serverPort = int(sys.argv[2])

#open server socket	and make reusable
serverSocket = socket(AF_INET, SOCK_STREAM) 
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

#bind the socket to the hostname or ip address and the port
serverSocket.bind((ip_address_or_hostname, serverPort))
serverSocket.listen(1)

print('The server is listening for connection requests.');

#Creating a new thread to handle input on the server side for commands
t = Thread(target=serverInputHandler, args=(serverSocket,))
t.start()
counter = 0

try:
	#loop to handle client connections - opening a new thread for each new client connection
	while 1:
		#accept new client connection
		connectionSocket, addr = serverSocket.accept()
		#Socket, client name, Is connected flag, address
		clients.append([connectionSocket,0,0,addr])
		#open thread for client management (deals with recieving and sending)
		t = Thread(target=clientManager, args=(connectionSocket,counter,))
		t.start()
		#client counter increases by 1
		counter += 1
		
	serverSocket.close()
	
except:
	os._exit(0)
