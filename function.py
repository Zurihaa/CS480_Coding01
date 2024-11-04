import sys

class TicTacToe:
	def __init__(self, first_player):
		self.state = [' '] * 9
		self.player = first_player

	def to_move(self, state):
		if self.player == 'x':
			return 'o' if state.count(' ') % 2 == 0 else 'x'
		else:
			return 'x' if state.count(' ') % 2 == 0 else 'o'

	def is_terminal(self, state):
		win = self.check_win(state, self.player)
		return win is not None or ' ' not in state

	def check_win(self, state, player):

		for row in [[0, 1, 2], [3, 4, 5], [6, 7, 8]]:
			if state[row[0]] == state[row[1]] == state[row[2]] and state[row[0]] != " ":
				return 1 if not_player(self.player) == state[row[0]] else -1

		for col in [[0, 3, 6], [1, 4, 7], [2, 5, 8]]:
			if state[col[0]] == state[col[1]] == state[col[2]] and state[col[0]] != " ":
				return 1 if not_player(self.player) == state[col[0]] else -1

		for diag in [[0, 4, 8], [2, 4, 6]]:
			if state[diag[0]] == state[diag[1]] == state[diag[2]] and state[diag[0]] != " ":
				return 1 if not_player(self.player) == state[diag[0]] else -1

		if ' ' not in state:
			return 0
		return None

	def actions(self, state):
		return [i + 1 for i in range(9) if state[i] == ' ']

	def result(self, state, action):
		new_state = state.copy()
		new_state[action - 1] = self.to_move(state)
		return new_state
	
def not_player(player):
	return "x" if player == "o" else "o"	

def print_board(state):
	for i in range(0, 9, 3):
		print(" | ".join(state[i:i+3]))
		if i < 6:
			print("--+--+--")

def minimax(game, state, counter):
	value, move, counter = max_value(game, state, counter)
	return move, counter

def max_value(game, state, counter):
	counter += 1
	
	if game.is_terminal(state):
		return game.check_win(state, game.to_move(state)), None, counter

	v = float("-inf")

	for a in game.actions(state):
		v2, a2, counter = min_value(game, game.result(state, a), counter)
		if v2 > v:
			v, move = v2, a
	return v, move, counter

def min_value(game, state, counter):
	counter += 1

	if game.is_terminal(state):
		return game.check_win(state, game.to_move(state)), None, counter
	
	v = float("inf")

	for a in game.actions(state):
		v2, a2, counter = max_value(game, game.result(state, a), counter)
		if v2 < v:
			v, move = v2, a

	return v, move, counter

def alpha_beta(game, state, counter):
	value, move, counter = max_alpha_beta(game, state, float("-inf"), float("inf"), counter)
	return move, counter

def max_alpha_beta(game, state, alpha, beta, counter):
	counter += 1

	if game.is_terminal(state):
		return game.check_win(state, game.to_move(state)), None, counter

	v = float("-inf")

	for a in game.actions(state):
		v2, a2, counter = min_alpha_beta(game, game.result(state, a), alpha, beta, counter)
		if v2 > v:
			v, move = v2, a
		alpha = max(alpha, v)
		if v >= beta:
			return v, move, counter
		
	return v, move, counter

def min_alpha_beta(game, state, alpha, beta, counter):
	counter += 1

	if game.is_terminal(state):
		return game.check_win(state, game.to_move(state)), None, counter

	v = float("inf")

	for a in game.actions(state):
		v2, a2, counter = max_alpha_beta(game, game.result(state, a), alpha, beta, counter)
		if v2 < v:
			v, move = v2, a
		beta = min(beta, v)
		if v <= alpha:
			return v, move, counter

	return v, move, counter

def argument_check(args):
	if len(args) != 4:
		print("ERROR: Not enough/too many/illegal input arguments. ")
		sys.exit(1)

	algo = args[1]
	if algo not in ['1', '2']:
		print("ERROR: Not enough/too many/illegal input arguments. ")
		sys.exit(1)
		
	first = args[2]
	if first not in ['x', 'o']:
		print("ERROR: Not enough/too many/illegal input arguments. ")
		sys.exit(1)

	mode = args[3]
	if mode not in ['1', '2']:
		print("ERROR: Not enough/too many/illegal input arguments. ")
		sys.exit(1)

	return algo, first, mode

def main():
	algo, first, mode = argument_check(sys.argv)

	if algo == "1":
		algo_name = "MiniMax"
	elif algo == "2":
		algo_name = "MiniMax with alpha-beta pruning"

	if mode == "1":
		mode_name = "Human Versus Computer"
	elif mode == "2":
		mode_name = "Computer Versus Computer"

	print("Thien Le A20484898 Solution:")
	print("Algorithm: " + algo_name)
	print("First: " + first)
	print("Mode: " + mode_name)

	counter = 0

	tic_tac_toe = TicTacToe(first)
    
    

	while not tic_tac_toe.is_terminal(tic_tac_toe.state):
		if mode == "1":
			if tic_tac_toe.to_move(tic_tac_toe.state) == first:
				moves = tic_tac_toe.actions(tic_tac_toe.state)
				print(first + "'s move. What is your move (possible moves at the moment are: " + str(moves) + " | enter 0 to exit the game)")
				user_move = int(input())
				if user_move == 0:
					sys.exit(1)

				bool = False
				while not bool:
					if user_move not in moves:
						print("Try Again")
						user_move = int(input())
					else:
						bool = True

				tic_tac_toe.state = tic_tac_toe.result(tic_tac_toe.state, user_move)

				print_board(tic_tac_toe.state)
			else:
				print("Computer's move")
				if algo == "1":
					computer_move, counter = minimax(tic_tac_toe, tic_tac_toe.state, counter)
					print(tic_tac_toe.player +"'s selected move: " + str(computer_move) + ". Number of search tree nodes generated: " + str(counter))
				else:
					computer_move, counter = alpha_beta(tic_tac_toe, tic_tac_toe.state, counter)
					print(tic_tac_toe.player +"'s selected move: " + str(computer_move) + ". Number of search tree nodes generated: " + str(counter))

				tic_tac_toe.state = tic_tac_toe.result(tic_tac_toe.state, computer_move)

				print_board(tic_tac_toe.state)
		elif mode == "2":
			print(f"{first}'s move:")
			if algo == "1":
				computer_move, counter = minimax(tic_tac_toe, tic_tac_toe.state, counter)
				print(tic_tac_toe.player +"'s selected move: " + str(computer_move) + ". Number of search tree nodes generated: " + str(counter))
			else:
				computer_move, counter = alpha_beta(tic_tac_toe, tic_tac_toe.state, counter)
				print(tic_tac_toe.player +"'s selected move: " + str(computer_move) + ". Number of search tree nodes generated: " + str(counter))
				
			tic_tac_toe.state = tic_tac_toe.result(tic_tac_toe.state, computer_move)

			print_board(tic_tac_toe.state)
	
	if tic_tac_toe.check_win(tic_tac_toe.state, first) == 1:
		print(first + " lost")
	elif tic_tac_toe.check_win(tic_tac_toe.state, first) == -1:
		print(first + " win")
	else:
		print("tie")

if __name__ == "__main__":
	main()