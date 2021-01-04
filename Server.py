import chess
import select
import socket
from _thread import *
import utility
import time

# Function: connection_update prints the informations about the connections currently managed in an intuitive manner
def connection_update(connections):
	clock = time.localtime()
	date = f'{clock[2]}/{clock[1]}/{clock[0]}'
	Ttime = f'{clock[3]}:{clock[4]}:{clock[5]}'
	if connections == {}:
		print('-'*5, "Update on Connections Date:",date," Time:", Ttime,'-'*5)
		print('NO CLIENT CONNECTED')
	else:
		print('-'*5, "Update on Connections Date:",date,"Time:", Ttime,'-'*5)
		print('FROM',' '*7,'TO')
		for i in connections:
			print(connections[i][0],' '*5,connections[i][1])




SIZE = 15
IP = '127.0.0.1'
PORT = 1234

# Making our server socket instance
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Reseting the port so that we can reuse it again (if the server has exited once)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# making the server instance ready by binding it
server_socket.bind((IP, PORT))
# listening for connections
server_socket.listen()

sockets_list = [server_socket]
connections = {}

print('#'*7,'CHESSARANK SERVER v1.2','#'*7,'\n')

while True:
	# read_socket manages the list of all the connected sockets in real-time
	read_socket, _, exception_socket = select.select(sockets_list, [], sockets_list)


	for notified_socket in read_socket:
		if(notified_socket==server_socket):
			client_socket, client_addr = server_socket.accept()

			# Receive client ID and 'Want to connect' client ID
			msg = client_socket.recv(SIZE).decode('utf-8')

			# Keeping track of the connections as new connections are made
			sockets_list.append(client_socket)
			connections[client_socket] = [msg[:6], msg[6:]]

		else:
			try:
				# Removing the clients from the tracking list as they have exited
				sockets_list.remove(notified_socket)
				del connections[notified_socket]
			except:
				pass

	# Calling the Function: Connection Update
	connection_update(connections)
	
	for connection in connections:
		# checking for clients present for a successful connection link between two clients
		if connections[connection][1] == msg[:6]:
			# Both the clients are notified about whether they are the first(White) to connect or second(Black)
			connection.send(bytes('1','utf-8'))
			client_socket.send(bytes('2','utf-8'))

			# Start the game (thread it for returning to listening to connections)
			start_new_thread(game.start_game, (connection, client_socket,))

			# remove the both clients from the tracking list
			sockets_list.remove(connection)
			sockets_list.remove(client_socket)
			del connections[connection]
			del connections[client_socket]
			break



