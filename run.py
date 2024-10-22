import random


class Ship:
    """
    A class representing a ship in the game of Battleship.
    """

    def __init__(self, name, size):
        """
        Initializes the ships object with a name, size, and empty coordinates list.
        """
        self.name = name
        self.size = size
        self.coordinates = []
        self.hits = 0

    def is_sunk(self):
        """
        Check if the ship is sunk (i.e., if the number of hits equals the size of the ship.)
        """
        return self.hits == self.size

class Grid:
    """
    A class representing a player's grid in the game of Battleship.
    """

    def __init__(self, size):
        """
        Initializes the Grid onject with a given size and an empty grid of water (~).
        """
        self.size = size
        self.grid = [['~' for _ in range(size)] for _ in range(size)]
        self.ships = []

    def display(self, show_ships=False):
        """
        Displays the grid. Optionally show ships based on the 'show_ships' flags.
        """
        # print column headers
        print("   " + " ".join([chr(65 + i) for i in range(self.size)])) #Column letters

        for i, row in enumerate(self.grid):
            row_display = []
            for cell in row:
                if show_ships:
                    row_display.append(cell) #Show ships as 'S'
                else:
                    row_display.append('~' if cell == 'S' else cell) #Hides ships as '~'
            
            #Adjust row numbers to aligin with single/double digits
            print(f"{i+1<2} " + " ".join(row_display))

    def place_ship(self, ship):
        """
        Places a ship randomly on the grid.
        """
        valid_placement = False
        while not valid_placement:
            orientation = random.choice(['H', 'V']) #Horizontal or Vertical
            if orientation == 'H':
                row = random.randint(0, self.size - 1)
                col = random.randint(0, self.size - ship.size)
                if all(self.grid[row][col + i] == '~' for i in range(ship.size)):
                    for i in range(ship.size):
                        self.grid[row][col + i] = 'S'
                        ship.coordinates.append((row, col + i))
                    valid_placement = True
            else:
                row = random.randint(0, self.size - ship.size)
                col = random.randint(0, self.size - 1)
                if all(self.grid[row + i][col] == '~' for i in range(ship.size)):
                    for i in range(ship.size):
                        self.grid[row + i][col] == 'S'
                        ship.coordinates.append((row + i, col))
                    valid_placement = True
        self.ships.append(ship)

    def receive_attack(self, row, col):
        """Processes an attack and returns whether it was a hit or miss."""
        if self.grid[row][col] == 'S':
            self.grid[row][col] = 'X'
            # Find which ship was hit and update its hits
            for ship in self.ships:
                if (row, col) in ship.coordinates:
                    ship.hits += 1
                    break
            return True
        elif self.grid[row][col] == '~':
            self.grid[row][col] = 'O'
        return False

    def all_ships_sunk(self):
        """
        Checks if all ships have been sunk.
        """
        return all(ship.is_sunk() for ship in self.ships)

class Player:
    """
    A class representing a player in the game of Battleship.
    """

    def __init__(self, name, grid_size):
        """
        Initializes the player object with a name and a grid.
        """
        self.name = name
        self.grid = Grid(grid_size)

    def take_turn(self, opponent_grid):
        """
        Allows the player to take a turn and attack the opponent's grid.
        """
        valid_input = False
        while not valid_input:
            try:
                target = input(
                    f"{self.name}, enter your target (e.g., A5: )").upper()
                col = ord(target[0]) - 65 #convert letter to column index
                row = int(target[1:]) - 1 #convert number to row index
                if row < 0 or col < 0 or row >= opponent_grid.size or col >= opponent_grid.size:
                    print("Target is out of bounds. Try again.")
                elif opponent_grid.grid[row][col] in ['X', 'O']:
                    print("You've already fired at this location. Try again.")
                else:
                    valid_input = True
            except (IndexError, ValueError):
                print("Invalid input. Enter a letter and a number (e.g., A5).")
        hit = opponent_grid.receive_attack(row, col)
        print("Hit!" if hit else "Miss!")

class Computer(Player):
    """
    a class representing the computer player with enhanced AI.
    """
    def __init__(self, name, grid_size, dificulty='easy'):
        super().__init__(name, grid_size)
        self.difficulty = difficulty
        self.last_hit = None
        self.hunt_mode = False
        self.potential_targets = []

    def take_turn(self, opponent_grid):
        """
        Allows the computer to take a turn with enhanced AI based on difficulty.
        """
        if self.difficulty == 'easy':
            self.random_fire(opponent_grid)
        elif self.difficulty == 'medium':
            self.smart_fire(opponent_grid)
        else:
            self.advanced_fire(opponent_grid)

    def random_fire(self, opponent_grid):
        """
        Computer fires randomly at the grid (Easy AI).
        """
        valid_target = False
        while not valid_target:
            row = random.randint(0, opponent_grid.size - 1)
            col = random.randint(0, opponent_grid.size - 1)
            if opponent_grid.grid[row][col] not in ['X', 'O']:
                valid_target = True
        hit = opponent_grid.receive_attack(row, col)
        print(f"Computer fires at {chr(65 + col)}{row + 1}.",
                "Hit!" if hit else "Miss!")

    def smart_fire(self, opponent_grid):
        """
        Computer fires smarty by focusing on adjacent cells after a hit (Medium AI).
        """
        if self.last_hit and not self.potential_targets:
            self.potential_targets = self.get_adjacent_cells(
                self.last_hit, opponent_grid)

        if self.potential_targets:
            row, col = self.potential_targets.pop(0)
        else:
            row, col = random.randint(
                0, opponent_grid.size - 1), random.randint(
                    0, opponent_grid.size - 1)

        hit = opponent_grid.receive_attack(row, col)
        print(f"Computer fires at {chr(65 + col)}{row + 1}.",
                "Hit!" if hit else "Miss!")
        if hit:
            self.last_hit = (row, col)
            self.hunt_mode = True
        else:
            self.hunt_mode = False
