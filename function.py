import sys
from enum import IntEnum

class TerminalStates(IntEnum):
	WIN = 1
	TIE = 0
	LOSE = -1

class TicTacToe:
	# Initialize the player and the board
	def __init__(self, first_player):
		self.state = [' '] * 9
		self.player = first_player
    # Determine whose turn to play
	def to_move(self, state):
		if self.player == 'x':
			return 'o' if state.count(' ') % 2 == 0 else 'x'
		else:
			return 'x' if state.count(' ') % 2 == 0 else 'o'
    #
	def is_terminal(self, state):
		win = self.check_win(state, self.player)
		return win is not None or ' ' not in state

    # Check for win condition
	def check_win(self, state, player):
		# Row for win-con
		for row in [[0, 1, 2], [3, 4, 5], [6, 7, 8]]:
			if state[row[0]] == state[row[1]] == state[row[2]] and state[row[0]] != " ":
				return TerminalStates.WIN if not_player(self.player) == state[row[0]] else TerminalStates.LOSE
        # Coloumn for win-con
		for col in [[0, 3, 6], [1, 4, 7], [2, 5, 8]]:
			if state[col[0]] == state[col[1]] == state[col[2]] and state[col[0]] != " ":
				return TerminalStates.WIN if not_player(self.player) == state[col[0]] else TerminalStates.LOSE
        # Diagonal for win-con
		for diag in [[0, 4, 8], [2, 4, 6]]:
			if state[diag[0]] == state[diag[1]] == state[diag[2]] and state[diag[0]] != " ":
				return TerminalStates.WIN if not_player(self.player) == state[diag[0]] else TerminalStates.LOSE
        # Check if all win con is not true and the board has no empty space
		if ' ' not in state:
			return TerminalStates.TIE
		return None
    #Showing possible moves that can be played
	def actions(self, state):
		return [i + 1 for i in range(9) if state[i] == ' ']
    # Make the move to the board
	def result(self, state, action):
		new_state = state.copy()
		new_state[action - 1] = self.to_move(state)
		return new_state

def not_player(player):
	return "x" if player == "o" else "o"

# Implement Minimax Algorithm based on what provided by the professor
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

# Implement Minimax Alpha Beta Algorithm based on what provided by the professor
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

#Error check for Commandline Argument
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
	print("Algorithm: ", algo_name)
	print("First: ", first)
	print("Mode: ", mode_name)

	counter = 0

	tic_tac_toe = TicTacToe(first)
    # Game Loop
	while not tic_tac_toe.is_terminal(tic_tac_toe.state):
		if mode == "1":
			if tic_tac_toe.to_move(tic_tac_toe.state) == first:
				#List of possible moves
				moves = tic_tac_toe.actions(tic_tac_toe.state)
				print(f"{first}'s move. What is your move (possible moves at the moment are: ) {moves} | enter 0 to exit the game) ")
				user_move = int(input())
				if user_move == 0:
					sys.exit(1)
				#Input check
				bool = False
				while not bool:
					if user_move not in moves:
						print("Try Again")
						user_move = int(input())
					else:
						bool = True
                #Make the move based on user input
				tic_tac_toe.state = tic_tac_toe.result(tic_tac_toe.state, user_move)
                #Print the board
				for i in range(0, 9, 3):
					print(" | ".join(tic_tac_toe.state[i:i+3]))
					if i < 6:
						print("--+---+--")
			else:
				print("Computer's move")
				if algo == "1":
					#Computer doing Minimax Algorithm
					computer_move, counter = minimax(tic_tac_toe, tic_tac_toe.state, counter)
					print(f"{'o' if first == 'x' else 'x'}'s selected move: {computer_move}. Number of search tree nodes generated: {counter}")
				else:
					computer_move, counter = alpha_beta(tic_tac_toe, tic_tac_toe.state, counter)
					print(f"{'o' if first == 'x' else 'x'}'s selected move: {computer_move}. Number of search tree nodes generated: {counter}")
				#Make the computer move after the algorithm
				tic_tac_toe.state = tic_tac_toe.result(tic_tac_toe.state, computer_move)
				#Print the board
				for i in range(0, 9, 3):
					print(" | ".join(tic_tac_toe.state[i:i+3]))
					if i < 6:
						print("--+---+--")
		elif mode == "2":
			print(f"{first}'s move:")
			if algo == "1":
				# Computer doing Minimax Algorithm
				computer_move, counter = minimax(tic_tac_toe, tic_tac_toe.state, counter)
				print(f"{'o' if first == 'x' else 'x'}'s selected move: {computer_move}. Number of search tree nodes generated: {counter}")
			else:
				# Computer doing Minimax Alpha Beta Algorithm
				computer_move, counter = alpha_beta(tic_tac_toe, tic_tac_toe.state, counter)
				print(f"{'o' if first == 'x' else 'x'}'s selected move: {computer_move}. Number of search tree nodes generated: {counter}")
			#Make the computer move after the algorithm
			tic_tac_toe.state = tic_tac_toe.result(tic_tac_toe.state, computer_move)
			#Print the board
			for i in range(0, 9, 3):
				print(" | ".join(tic_tac_toe.state[i:i+3]))
				if i < 6:
					print("--+---+--")
    #Condition check to display the result
	win_status = tic_tac_toe.check_win(tic_tac_toe.state, first)
	if win_status == TerminalStates.WIN:
		print(f"{first} lost")
	elif win_status == TerminalStates.LOSE:
		print(f"{first} win")
	else:
		print("tie")

# Play Tic Tac Toe
if __name__ == "__main__":
	main()