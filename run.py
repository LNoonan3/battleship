import random
import sys

class Ship:
    """
    Class representing a ship in the game
    """
    def __init__(self, name, size):
        self.name = name # name of the ship
        self.size = size # size of the ship
        self.coordinates = [] # list to hold the ship's coordinates on the grid
        self.hits = 0 # number of hits the ship has taken

    def is_sunk(self):
        """
        Check if the ship is sunk.
        """
        return self.hits == self.size

class Grid:
    """
    Class representing the game grid.
    """
    def __init__(self, size):
        self.size = size # size of the grid (number of rows/columns)
        self.grid = [['~' for _ in range(size)] for _ in range(size)] # initialize the grid with empty water cells
        self.ships = [] # list of hold the ships placed on the grid

    def display(self, show_ships=False):
        """
        Display the grid to the player.
        """
        print("   " + " ".join([chr(65 + i) for i in range(self.size)])) # diplay column headers
        for i, row in enumerate(self.grid):
            row_display = []
            for cell in row:
                #show ship positions if requested; otherwise, show water ('~') or hit/miss status
                if show_ships:
                    row_display.append(cell)
                else:
                    row_display.append('~' if cell == 'S' else cell)
            print(f"{i+1:<2} " + " ".join(row_display)) # display the row number and cells

    def place_ship(self, ship):
        """
        Place a ship on the grid.
        """
        valid_placement = False
        while not valid_placement:
            # randomly choosse orientation for the ship (horizontal or vertical)
            orientation = random.choice(['H', 'V'])
            if orientation == 'H':
                # random row and column for horizontal placement
                row = random.randint(0, self.size - 1)
                col = random.randint(0, self.size - ship.size)
                # check if the placement is valid (no overlap with other ships)
                if all(self.grid[row][col + i] == '~' for i in range(ship.size)):
                    for i in range(ship.size):
                        self.grid[row][col + i] = 'S' # mark ship's position on the grid 
                        ship.coordinates.append((row, col + i)) # store ship's coordinates
                    valid_placement = True
            else:
                # random row and column for vertical placement
                row = random.randint(0, self.size - ship.size)
                col = random.randint(0, self.size - 1)
                # check if the placement is valid
                if all(self.grid[row + i][col] == '~' for i in range(ship.size)):
                    for i in range(ship.size):
                        self.grid[row + i][col] = 'S' # mark ship's position on the grid
                        ship.coordinates.append((row + i, col)) # store ship's coordinates 
                    valid_placement = True
        self.ships.append(ship) # add the placed ship to the list of ships

    def receive_attack(self, row, col):
        """
        Process an attack on the grid .
        """
        if self.grid[row][col] == 'S':
            self.grid[row][col] = 'X' # mark hit position on the grid
            for ship in self.ships:
                if (row, col) in ship.coordinates:
                    ship.hits += 1 # increment the hit count for the ship.
                    break
            return True # attack was a hit
        elif self.grid[row][col] == '~':
            self.grid[row][col] = 'O' # mark miss position on the grid
        return False # attack was a miss

    def all_ships_sunk(self):
        """
        Check if all ships on the grid are sunk.
        """
        return all(ship.is_sunk() for ship in self.ships)

class Player:
    """
    Class representing a player in the game.
    """
    def __init__(self, name, grid_size):
        self.name = name # name of the player
        self.grid = Grid(grid_size) # creates a grid for the player

    def take_turn(self, opponent_grid):
        """
        Take a turn by attacking the opponent's grid.
        """
        valid_input = False
        while not valid_input:
            try:
                target = input(f"{self.name}, enter your target (e.g., A5): ").upper()
                check_for_exit(target) # check if the player wants to exit
                col = ord(target[0]) - 65 # convert letter to column index
                row = int(target[1:]) - 1 # convert number to row index
                #validate the target input
                if row < 0 or col < 0 or row >= opponent_grid.size or col >= opponent_grid.size:
                    print("Target is out of bounds. Try again.")
                elif opponent_grid.grid[row][col] in ['X', 'O']:
                    print("You've already fired at this location. Try again.")
                else:
                    valid_input = True # valid input received
            except (IndexError, ValueError):
                print("Invalid input. Enter a letter and a number (e.g., A5).")
        hit = opponent_grid.receive_attack(row, col) # attack the opponenet's grid
        print("Hit!" if hit else "Miss!") # inform the player of the result

class Computer(Player):
    """
    Class representing the computer player.
    """
    def __init__(self, name, grid_size, difficulty='easy'):
        super().__init__(name, grid_size) # initialize parent class
        self.difficulty = difficulty # difficulty level of the computer
        self.last_hit = None # last hit coorinates
        self.hunt_mode = False # whether in hunt mode after hitting a ship
        self.potential_targets = [] # potential target coorinates to attack

    def take_turn(self, opponent_grid):
        """
        Take a turn by attacking the opponent's grid based on difficulty.
        """
        if self.difficulty == 'easy':
            self.random_fire(opponent_grid)
        elif self.difficulty == 'medium':
            self.smart_fire(opponent_grid)
        else:
            self.advanced_fire(opponent_grid)

    def random_fire(self, opponent_grid):
        """
        Fire randomly at the opponent's grid.
        """
        valid_target = False
        while not valid_target:
            row = random.randint(0, opponent_grid.size - 1)
            col = random.randint(0, opponent_grid.size - 1)
            # check if the target has not been attacked yet
            if opponent_grid.grid[row][col] not in ['X', 'O']:
                valid_target = True
        hit = opponent_grid.receive_attack(row, col) # attack the opponenet's grid
        print(f"Computer fires at {chr(65 + col)}{row + 1}.", "Hit!" if hit else "Miss!")

    def smart_fire(self, opponent_grid):
        """
        Fire intelligently by targeting adjacent cells after a hit.
        """
        if self.last_hit and not self.potential_targets:
            self.potential_targets = self.get_adjacent_cells(self.last_hit, opponent_grid)

        if self.potential_targets:
            row, col = self.potential_targets.pop(0) # take the next potential target
        else:
            # fall back to random firing if no potential targets available
            row, col = random.randint(0, opponent_grid.size - 1), random.randint(0, opponent_grid.size - 1)

        hit = opponent_grid.receive_attack(row, col) # attack the opponent's grid 
        print(f"Computer fires at {chr(65 + col)}{row + 1}.", "Hit!" if hit else "Miss!")
        if hit:
            self.last_hit = (row, col) # update last hit coordinates
            self.hunt_mode = True # switch to hunt mode
        else:
            self.hunt_mode = False # switch to hunt mode

    def advanced_fire(self, opponent_grid):
        """
        Fire with advanced tactics based on previous hits.
        """
        if self.hunt_mode and self.potential_targets:
            row, col = self.potential_targets.pop(0) # take the next target in hunt mode
        else:
            if self.last_hit and not self.potential_targets:
                self.potential_targets = self.get_adjacent_cells(self.last_hit, opponent_grid)

            if not self.potential_targets:
                valid_target = False
                while not valid_target:
                    row = random.randint(0, opponent_grid.size - 1)
                    col = random.randint(0, opponent_grid.size - 1)
                    # check if the target has been attack yet
                    if opponent_grid.grid[row][col] not in ['X', 'O']:
                        valid_target = True
            else:
                row, col = self.potential_targets.pop(0) # take the next potential target

        hit = opponent_grid.receive_attack(row, col) # attack the opponent's grid
        print(f"Computer fires at {chr(65 + col)}{row + 1}.", "Hit!" if hit else "Miss!")
        if hit:
            self.last_hit = (row, col) # update last hit coordinates
            self.hunt_mode = True # switch to hunt mode
        else:
            self.hunt_mode = False # switch back to normal mode

    def get_adjacent_cells(self, hit_coords, grid):
        """
        Get valid adjacent cells for potential attacks
        """
        row, col = hit_coords
        potential_targets = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
        # filter valid targets within grid bounds and not already attacked 
        valid_targets = [(r, c) for r, c in potential_targets if 0 <= r < grid.size and 0 <= c < grid.size and grid.grid[r][c] not in ['X', 'O']]
        return valid_targets

def setup_ships(grid):
    """
    Set up the ships on the given grid
    """
    ships = [
        Ship("Carrier", 5),
        Ship("Battleship", 4),
        Ship("Cruiser", 3),
        Ship("Submarine", 3),
        Ship("Destroyer", 2)
    ]
    for ship in ships:
        grid.place_ship(ship) # place each ship on the grid

def check_for_exit(input_string):
    """
    Check if the input string is an exit command.
    """
    if input_string.lower() == 'exit':
        print("You have exited the game. Goodbye!")
        sys.exit()

def choose_game_options():
    """
    Prompt the user to choose game options for grid size and difficulty.
    """
    while True:
        try:
            grid_size = input("Choose grid size (8, 10, 12): ")
            check_for_exit(grid_size) # check if the player wants to exit
            grid_size = int(grid_size)
            if grid_size not in [8, 10, 12]:
                raise ValueError("Invalid grid size. Please choose 8, 10, or 12.")
            break
        except ValueError as e:
            print(e)

    while True:
        difficulty = input("Choose difficulty (easy, medium, hard): ").lower()
        check_for_exit(difficulty) # check if the player wants to exit
        if difficulty in ['easy', 'medium', 'hard']:
            break
        else:
            print("Invalid difficulty level. Please choose 'easy', 'medium', or 'hard'.")
    return grid_size, difficulty

def play_game():
    """
    main game loop to play Battleship
    """
    while True:
        print("Welcome to Battleship!")
        print("Type 'exit' at any point to quit the game.")
        print("Game Rules:")
        print("1. Take turns firing at the opponent's grid.")
        print("2. Try to sink all of your opponent's ships.")
        print("3. The first player to sink all enemy ships wins.")

        grid_size, difficulty = choose_game_options() # get game options 

        player = Player("Player", grid_size) # create a player
        setup_ships(player.grid) # set up the ships for the player

        computer = Computer("Computer", grid_size, difficulty) # create a computer player
        setup_ships(computer.grid) # set up ships for the computer

        game_over = False
        while not game_over:
            print("\nYour Grid:")
            player.grid.display(show_ships=True) # display player's grid
            print("\nComputer's Grid:")
            computer.grid.display() # display computer's grid (hidden ships)
            player.take_turn(computer.grid) # player's turn to attack
            if computer.grid.all_ships_sunk():
                print("Congratulations! You sunk all the computer's ships!")
                game_over = True # end game if player wins
                continue

            computer.take_turn(player.grid) # computer's turn to attack 
            if player.grid.all_ships_sunk():
                print("The computer has sunk all your ships. You lose.")
                game_over = True # end game if computer wins

        play_again = input("\nWould you like to play again? (y/n): ").lower()
        check_for_exit(play_again) # check if the player want to exit
        if play_again != 'y':
            print("Thanks for playing Battleship! Goodbye!") # end game
            break

if __name__ == "__main__":
    play_game() # start the game
