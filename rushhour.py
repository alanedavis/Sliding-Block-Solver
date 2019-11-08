import sys
from random import randint
import math
import queue
import heapq

class Car():
	def __init__(self, orientation, coordinate, letter):
		self.orientation = orientation # Will hold whether the car is vertical or horizontal
		self.coordinate = coordinate # Stores a list of coordinates
		self.letter = letter # Stores the letter that the car is made up of

class Path():
	def __init__(self):
		self.paths = [] # List of boards that will make up a 'path'
	
	def add(self,board):
		self.paths.append(board.board) # Append an instance of the board class
	
	def path_print(self):
		board.print_format(self.paths,True) # Uses Boards print_paths in order to save wasted lines of code

class Board():
	def __init__(self,state = "  o aa|  o   |xxo   |ppp  q|     q|     q"): # Default board is built into the class
		self.board = [] # Current Board Instance
		self.moves = [] # Will store all possible moves
		self.cars = [] # Will store all Car() instances
		self.paths = [] # Will store all paths that lead to current board
		self.path = Path() # This allows for Board to use Path() methods and look clean
		self.filled = 0 # Will hold the number of non blank values in the state string
		self.cloned = "" # Can store temporary state

		str2list = [[' ']*6 for x in range(6)] # Empty string that will be filled in order to make up the board
		car_eval = [] # List of evaluated cars
		cur = 0; index = 0 # current and index

		for i in range(len(state)): # for every row in the board
			if state[i] == "|": # delimit on '|'
				cur = cur + 1
				index = 0
			else:
				str2list[cur][index] = state[i] # make the temp list take the current value in state
				index += 1 # iterate 1
				if state[i] not in car_eval and state[i] != " ": # If the value isnt blank  
					car_eval.append(state[i])
					if state[i-1] == state[i] or state[i+1] == state[i]: # Determine whether the car moves horizontally or vertically
						self.cars.append(Car("horizontal", [[index-1,cur]], state[i]))
					else:                                              
						self.cars.append(Car("vertical", [[index-1,cur]], state[i]))
				elif state[i] in car_eval and state[i] != " ": 
					current = self.grab_car(state[i])
					current.coordinate.append([index-1,cur])

		self.board = str2list # Make the current board a list of lists
		goal_path = max(x[0] for x in self.grab_car('x').coordinate) # Grab the 'x' coordinates
		
		for i in range(goal_path + 1, 6): # Count how many spaces are filled in with non-blanks
			if self.board[2][i] != ' ':
				self.filled += 1
		
		# Calculate the cost x has from teh goal
		# Create heuristic variables
		self.h = self.filled * 1 
		self.cost = len(self.path.paths)
		self.f = self.h + self.cost
	
	def print_state(self):
		print(" ------ ") # Board Top
		for i in range(len(self.board)):
			# List comprehension for printing the game board
			print("|",end="")
			[print(str(self.board[i][j]), end="") for j in range(len(self.board[0]))]
			if i != 2: # Don't print a wall on row 3
				print("|")
			else:
				print("")
		print(" ------ ") # Board Bottom

	def print_list(self, start, end, current_list, path):
		# If not a Path object
		if not path:
			# For every row, including top and bottom, iterate throw
			for i in range(8):
				# Print every row and append walls as needed
				# If the boards have reached a width of 8 boards
				# Make a new line of boards
				for j in range(start, end):
					if i != 0 and i != 7:
						print("|",end='')  
					else:
						print(" ",end='')

					for k in range(6): 
						if i == 0 or i == 7:
							print("-",end="")
						else:
							print(current_list[j].board[i-1][k],end='')
					if i != 0 and i != 7:
						if i == 3:
							print(" ",end=' ') 
						else:
							print("|",end=' ')
					else:
						print(" ",end=' ')
				print("")
		# If not a Board instance remove the '.board' on line 123
		else:
			# For every row, including top and bottom, iterate throw
			for i in range(8):
				# Print every row and append walls as needed
				# If the boards have reached a width of 8 boards
				# Make a new line of boards
				for j in range(start, end):
					if i != 0 and i != 7:
						print("|",end='')  
					else:
						print(" ",end='')

					for k in range(6): 
						if i == 0 or i == 7:
							print("-",end="")
						else:
							print(current_list[j][i-1][k],end='')
					if i != 0 and i != 7:
						if i == 3:
							print(" ",end=' ') 
						else:
							print("|",end=' ')
					else:
						print(" ",end=' ')
				print("")
	
	# Print the game board as a string
	def string_state(self):
		temp = ''
		for i in range(len(self.board)):
			for j in range(len(self.board[i])):
				temp += self.board[i][j]
			temp += '|'
		# Remove the very last character in temp because it is an unecessary wall
		return temp[:-1]
	
	# Grab the car that is inputted
	def grab_car(self,car):
		for i in range(len(self.cars)):
			if self.cars[i].letter == car:
				return self.cars[i]
	
	# This is a function that checks for overflow of boards
	# This allows for many boards to be printed no matter the screen size
	def print_format(self, current_list, path = False):
		if len(current_list) < 8: # If there are less than 8 boards, print normally
			self.print_list(0, len(current_list), current_list, path)
		else: # else, we will print them 5 at a time
			i = int(math.floor(len(current_list) / 8)) # This will calculate how many lines of boards we need
			remainder = int(len(current_list) % 8) # If not divisible by 8
			for j in range(i): # Remainder boards
				self.print_list(j*8, (j+1)*8, current_list, path) # Print all boards besides last line
			if remainder > 0:
				self.print_list(i*8, i*8+remainder, current_list, path)

	def clone(self):
		return Board(self.string_state()) # return a new instance of the board
	
	def done(self):
		return self.grab_car('x').coordinate == [[4, 2], [5, 2]] # Return True if the 'x' car is in goal positioning, else if not
	
	def next_for_car(self, car, path):
		car_moves = [] # Make a temporary list for all car moves to be stored
		current = self.clone() # Make a new instance of Board to use for new moves
		current_car = current.grab_car(car) # Grab the current ca
		current_board = current.board # This is the current Board of the new Board instance
		i = 0 # For indexing

		if current_car.orientation == 'horizontal': # If the car moves horizontally
			y_pos = current_car.coordinate[0][1] # Grab the y position
			right = max([i[0] for i in current_car.coordinate]) # This right most position of the car (max value in coordinates)
			left = min([i[0] for i in current_car.coordinate]) # This left most position of the car (min value in coordinates)
			
			while right + 1 + i < 6 and current_board[y_pos][right + 1 + i] == ' ': # While there is still room to move right
				# Add 1 to all of the y coordinates
				# Replace leftmost coordinate with a blank space
				# Add 1 to i
				# Append the proper board
				current_board[y_pos][right + 1 + i] = car
				current_board[y_pos][left + i] = ' '
				i += 1
				car_moves.append(Board(current.string_state()))
				# If you only want to be able to move car once
				if path:
					break
			
			# Reset the gameboard if the car is able to move in the left direction
			if left - 1 - i > -1 and current_board[y_pos][left - 1 - i] == ' ':
				current = self.clone()
				current_board = current.board
				i = 0
			
			while left - 1 - i > -1 and current_board[y_pos][left - 1 - i] == ' ':# While there is still room to move left
				# Subtract 1 from all of the y coordinates
				# Replace rightmost coordinate with a blank space
				# Subtract 1 from i
				# Append the proper board
				current_board[y_pos][left - 1 - i] = car
				current_board[y_pos][right - i] = ' '
				i += 1
				car_moves.append(Board(current.string_state()))
				# If you only want to be able to move car once
				if path:
					break
		else:
			x_pos = current_car.coordinate[0][0] # Grab the x position
			low = max([i[1] for i in current_car.coordinate]) # This lowest position of the car (max value in coordinates)
			high = min([i[1] for i in current_car.coordinate])# This highest most position of the car (min value in coordinates)

			while high - 1 - i > -1 and current_board[high - 1 - i][x_pos] == ' ': # While there is still room to move up
				# Subtract 1 from all of the x coordinates
				# Replace bottom most coordinate with a blank space
				# Subtract 1 from i
				# Append the proper board
				current_board[high - 1 - i][x_pos] = car
				current_board[low - i][x_pos] = ' '
				i += 1
				car_moves.append(Board(current.string_state()))
				# If you only want to be able to move car once
				if path:
					break
			
			# Reset the gameboard if the car is able to move downward
			if low + 1 + i < 6 and current_board[low + 1 + i][x_pos] == ' ':
				current = self.clone()
				current_board = current.board
				i = 0
				
			while low + 1 + i < 6 and current_board[low + 1 + i][x_pos] == ' ': # While there is still room to move down
				# Add 1 to all of the x coordinates
				# Replace bottom most coordinate with a blank space
				# Add 1 to i
				# Append the proper board
				current_board[low + 1 + i][x_pos] = car
				current_board[high + i][x_pos] = ' '
				i += 1
				car_moves.append(Board(current.string_state()))
				if path:
					break
		
		# Add all the new car moves to the move list
		self.moves.extend(car_moves)

	def next(self, skip = False, path = False):
		# For every car on the board
		# Find all of the possible moves
		for car in self.cars:
			self.next_for_car(car.letter, path)
		
		# If you dont want the moves printed... skip
		if skip:
			return
		
		# Print all of the moves to terminal
		self.print_format(self.moves)

	def struct_moves(self,bfs): # Handles Astar and BFS algorithm due to the similar code
		# While loop condition
		stop = False

		# All nodes visited so that you do not revisit nodes
		visited_nodes = []
		visited_nodes.append(self.board)

		# Add the current Board instance to the path list
		# Print the current board instance
		self.path.add(self)
		self.path.path_print()

		# Using the queue library
		# Put the current instance at the front of the queue
		if bfs:
			q = queue.Queue()
			q.put(self)
		else:
			# Store the order that the nodes came
			# Make a count
			# Make a heap that holds the count, boards, and heurisitic
			order = []
			count = 0
			heapq.heappush(order, (self.f, count, self))
		
		while not stop: # While stop is false
			if bfs:
				board = q.get()  # Pop off the first item in the queue
				path = board.path.paths  # Add board to Path class paths list
			else:
				board = heapq.heappop(order) # Pop off board with the least distance to the goal
				board = board[2] # Grab the board which is the third value in the tuple
				path = board.path.paths # Save the full path to the current board
			
			board.next(True) # Find all next moves for current board
			
			for i in range(len(board.moves)): # Iterate through all of the possible moves
				if board.moves[i].board not in visited_nodes: # If the new node (move) hasn't been visited, add it to the visited_nodes list
					visited_nodes.append(board.moves[i].board) # Append board to lost
					board.moves[i].path_add(path) # Add path of board to the list
					board.moves[i].path.add(board.moves[i]) # Add board being expanded by path
					board.moves[i].path.path_print() # Print the current path that has been expanded
					if board.moves[i].done() == True: # Check if the baord is in a solved state
						print('It took {} node visits to solve.'.format(len(visited_nodes) + 1)) # Print 'victory message'
						stop = True # Meet the while loop condition
						break # break for loop
					else:
						if bfs:	# If breadth first search
							q.put(board.moves[i]) # Push new node onto queue
						else:
							count += 1 # Add one to count
							heapq.heappush(order, (board.moves[i].f, count, board.moves[i])) # Generate new heuristic value, count, and board heap

	def path_add(self, path): 
		self.path.paths.extend(path) # Add path to list
		self.cost = len(path) # Calculate Cost to goal
		self.f += len(path)

	def random(self, total_moves = 10):
		current = self # Make a new instance equal to the current board instance
		current.paths.append(self) # Append self to paths

		if current.done(): # Check if the current board instance is solved
			current.print_state() # Print solved board
		
		for _ in range(total_moves): # For all moves in list
			path = current.paths # Set path equal to the paths list
			current.next(True,True) # Check for next moves that only move a max of 1 distance from current state (per car)
			num = len(self.moves) # Print number of moves
			current = current.moves[randint(0, num - 1)] # Pick a random move in the list
			current.paths.extend(path) # Extend Paths
			current.paths.append(current) # Add current Board instance to path
			
			if current.done(): # Check if done, if so break
				break
		
		# Print random path
		current.print_format(current.paths)

	def bfs(self):
		# Run premade function with True value
		self.struct_moves(True)
		return

	def astar(self):
		# Run premade function with False value
		self.struct_moves(False)
		return


if __name__ == "__main__":
	if len(sys.argv) == 3:
		string = sys.argv[2]
		board = Board(sys.argv[2])
	else:
		board = Board()
	if sys.argv[1] == 'print':
		board.print_state()
	elif sys.argv[1] == 'next':
		board.next(False)
	elif sys.argv[1] == 'done':
		print(board.done())
	elif sys.argv[1] == 'random':
		board.random()
	elif sys.argv[1] == 'bfs':
		board.bfs()
	elif sys.argv[1] == 'astar':
		board.astar()