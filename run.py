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
        """
        Processes an attack and return whether it was a hit or miss.
        """
        if self.grid[row][col] == 'S':
            self.grid[row][col] = 'X'
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
                    print("Targetis out of bounds. Try again.")
                elif opponent_grid.grid[row][col] in ['X', 'O']:
                    print("You've already fired at this location. Try again.")
                else:
                    valid_input = True
            except (IndexError, ValueError):
                print("Invalid input. Enter a letter and a number (e.g., A5).")
        hit = opponent_grid.receive_attack(row, col)
        print("Hit!" if hit else "Miss!")
