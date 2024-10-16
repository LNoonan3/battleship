import random


class Ship:
    """
    A class representing a ship in the game of Battleship.
    """

    def __init__(self, name, size):
        self.name = name
        self.size = size
        self.coordinates = []
        self.hits = 0

    def is_sunk(self):
        """
        Check if the ship is sunk.
        """
        return self.hits == self.size

class Grid:
    """
    A class representing a player's grid in the game of Battleship.
    """

    def __init__(self, size):
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
