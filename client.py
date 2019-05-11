# This file contains the code for the client for the chat program
# It contains a small loop for clients to send messages and recieve messages
# The recieve messages loop is put into another thread so that the client can both send and
# recieve messages at any time. 

from socket import *
from threading import Thread
import os
import sys

# This function is a loop for recieving messages from the server
# Parameters: clientSocket - the client socket connection
# No returns: This is a loop until the socket is disconnected and then it exits
def recieveMessage(clientSocket):
	try:
		while 1:
			messageRecieved = clientSocket.recv(1024).decode()
			print(messageRecieved)
	except:
		os._exit(0)

#captures system arguments and makes sure all three are there
if len(sys.argv) < 3:
	print("Please use all the arguments: python script, IP address or hostname, port number")
	os.exit(0)

ip_address_or_hostname = str(sys.argv[1])
serverPort = int(sys.argv[2])

#open socketd 
clientSocket = socket(AF_INET, SOCK_STREAM)
#connect to server
clientSocket.connect((ip_address_or_hostname,serverPort))

#captures the user name of the client and sends it to the server. 
message = input("User name: ")
clientSocket.send(message.encode())

#recieves the server's initial response and prints it to the screen (welcome message)
modifiedMessage = clientSocket.recv(1024).decode()

print('The server responded with: ', modifiedMessage)

t = Thread(target=recieveMessage, args=(clientSocket,))
t.start()

#loop for sending messages to the server
try:
	while 1:
		message = input('')
		clientSocket.send(message.encode())
		#if the use input is "close()" - close the socket (the server will also close it on the other end once it recieves the message)
		if message == "close()":
			clientSocket.close()
			break
except:
	os._exit(0)

