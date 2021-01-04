import chess

SIZE = 1024	

# Class that manages the chess board and game
class Game:
	def __init__(self):
		self.board = chess.Board()
		self.valid_moves = self.board.legal_moves
	def move(self, move):
		self.board.push_san(move)

	def game_over(self):
		return (self.board.is_game_over())


def start_game(player1, player2):
	plr1_move = True
	while True:
		if plr1_move:
			msg = player1.recv(SIZE)
			if msg.decode('utf-8')!='':
				player2.send(msg)
				plr1_move = False
			else:
				player2.send(bytes('Connection closed by Player 1(white)','utf-8'))
				return
		else:
			msg = player2.recv(SIZE)
			if msg.decode('utf-8')!='':
				player1.send(msg)
				plr1_move = True
			else:
				player1.send(bytes('Connection closed by Player 2(Black)','utf-8'))
				return
