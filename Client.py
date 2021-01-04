from utility import *
import socket
import time
import sys

PORT = 1234
IP = '127.0.0.1'
SIZE = 1024

# initializing the board(game class instance)
board = Game()


# Receiving user input for their client id and the one thy want to connect to
client_id = ''
connecting_client_id = ''
while not client_id or len(client_id)!=6:
	client_id = input('Enter your ID: ')
while not connecting_client_id or len(connecting_client_id)!=6:
	connecting_client_id = input("Enter opponent's ID: ")

# Preparing the client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#connecting the client socket to the server
client_socket.connect((IP, PORT))

#sending the id informations to the server
send_data = bytes(client_id+connecting_client_id, 'utf-8')
client_socket.send(send_data)

# Receiving the role of the client (Player type: White[1] or Black[2])
player_num = client_socket.recv(SIZE).decode('utf-8')

# (White) player 1
if player_num == '1':
	while True:
		# TODO: let the user only see the valid moves without the whole structure
		# valid_moves = []
		print(board.board,'\n',board.valid_moves)# TODO: validify moves
		mv = input('Enter your move: ')
		# TODO: checking if the move is valid
		board.move(mv)
		print(board.board,'\n',board.valid_moves)#TODO: validify moves
		client_socket.send(bytes(mv, 'utf-8'))

		player_turn = False

		# opponents turn
		while not player_turn:
			mv = client_socket.recv(SIZE).decode('utf-8')
			if len(mv)<=4 and len(mv)>1:
				board.move(mv)
				player_turn = True
			else:
				print(mv)
				time.sleep(1)
				print('Closing this connection')
				time.sleep(1)
				sys.exit()
		player_turn = False

else:
	# As the player is (black) player 2 he has to wait for the opponent's turn first
	while True:
		player_turn = False
		while not player_turn:
			mv = client_socket.recv(SIZE).decode('utf-8')

			if len(mv)<=4 and len(mv)>1:
				board.move(mv)
				player_turn = True
			else:
				print(mv)
				time.sleep(1)
				print('Closing this connection')
				time.sleep(1)
				sys.exit()
		player_turn = False


		# TODO: let the user only see the valid moves without the whole structure
		# valid_moves = []
		print(board.board,'\n',board.valid_moves)# TODO: validify moves
		mv = input('Enter your move: ')
		board.move(mv)
		print(board.board,'\n', board.valid_moves)# TODO: validify moves
		client_socket.send(bytes(mv, 'utf-8'))
	

		


