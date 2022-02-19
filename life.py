import random
import numpy as np
from PIL import Image, ImageTk

# A Life class manages the state of the neighborhood
class Life:

    def __init__(self, start_size, neighborhood_size):
        # Starting block
        self.block = np.zeros(start_size)

        # Max size neighborhood
        self.neighborhood = np.zeros(neighborhood_size)

        # Changes for every frame
        self.change = []

        self.img = 0
        self.curr_img = 0
        self.scale = 1
        
        self.is_paused = True
        self.finish = False

        self.generate()

    def __repr__(self):
        res = ""
        for row in range(self.neighborhood.shape[0]):
            for col in range(self.neighborhood.shape[1]):
                res += str(int(self.neighborhood[row][col]))
                if (col != self.neighborhood.shape[1] - 1):
                    res += " "
            if (row != self.neighborhood.shape[0] - 1):
                res += "\n"
        return res

    # Generate a random neighborhood
    def generate(self):
        self.finish = False
        for row in range(self.block.shape[0]):
            lower_row = int((self.neighborhood.shape[0] - self.block.shape[0]) / 2) + row
            for col in range(self.block.shape[1]):
                lower_col = int((self.neighborhood.shape[1] - self.block.shape[1]) / 2) + col
                self.neighborhood[lower_row][lower_col] = float(random.getrandbits(1))

    # Empty a neighborhood
    def make_empty(self):
        self.configure(self.block.shape, self.neighborhood.shape)
        
    # Configure neighborhood to given starting neighborhood size and neighborhood size
    def configure(self, start_size, neighborhood_size):
        self.finish = False
        self.block = np.zeros(start_size)
        self.neighborhood = np.zeros(neighborhood_size)

    # Change the state of a block
    def change_cell(self, row, col):
        try:
            self.neighborhood[row][col] = not self.neighborhood[row][col]
        except:
            print("cell index out of range")

    # Return true if neighborhood is empty, false otherwise
    def is_empty(self):
        return not self.neighborhood.any()

    # Return true if neighborhood does not change
    def is_finish(self):
        return self.finish

    # Pause the state of the game
    def pause(self):
        self.is_paused = True

    # Unpause the state of the game
    def unpause(self):
        self.is_paused = False

    # Update the neighborhood depending on Conway's algorithm
    def update(self):
        for row in range(self.neighborhood.shape[0]):
            for col in range(self.neighborhood.shape[1]):
                self.check_neighbors(row, col)

        for block in self.change:
            self.change_cell(block[0], block[1])

        if self.change == []:
            self.finish = True

        self.change = []

    # Checks which neighbors are to change based on Conway's algorithm
    def check_neighbors(self, row, col):
        neighbor = 0
        
        if row - 1 >= 0 and col - 1 >= 0:
            neighbor += int(self.neighborhood[row - 1][col - 1])
        if row - 1 >= 0 and col >= 0:
            neighbor += int(self.neighborhood[row - 1][col])
        if row - 1 >= 0 and col + 1 < len(self.neighborhood[0]):
            neighbor += int(self.neighborhood[row - 1][col + 1])

        if row >= 0 and col - 1 >= 0:
            neighbor += int(self.neighborhood[row][col - 1])
        if row >= 0 and col + 1 < len(self.neighborhood[0]):
            neighbor += int(self.neighborhood[row][col + 1])

        if row + 1 < len(self.neighborhood) and col - 1 >= 0:
            neighbor += int(self.neighborhood[row + 1][col - 1])
        if row + 1 < len(self.neighborhood) and col >= 0:
            neighbor += int(self.neighborhood[row + 1][col])
        if row + 1 < len(self.neighborhood) and col + 1 < len(self.neighborhood[0]):
            neighbor += int(self.neighborhood[row + 1][col + 1])

        if (neighbor > 3 or neighbor < 2) and self.neighborhood[row][col] == 1.0:
            self.change.append((row, col))
        elif neighbor == 3 and self.neighborhood[row][col] == 0.0:
            self.change.append((row, col))

    # Update the image of the neighborhood
    def update_img(self):
        arr = np.zeros((self.neighborhood.shape[0] * self.scale, self.neighborhood.shape[1] * self.scale))
        for row in range(self.neighborhood.shape[0]):
            for col in range(self.neighborhood.shape[1]):
                state = self.neighborhood[row][col] * 255
                pixel = np.full((self.scale, self.scale), state)
                arr[row * self.scale : (row + 1) * self.scale, col * self.scale : (col + 1) * self.scale] = pixel
         
        self.img = ImageTk.PhotoImage(image = Image.fromarray(arr))

    # Get final image
    def get_img(self):
        return self.img
