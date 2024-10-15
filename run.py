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