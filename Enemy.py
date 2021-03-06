# This module controls the enemy position and movement
# Author: Josh Abrahams

import pygame
import random
from settings import *

vec = pygame.math.Vector2


class Enemy:
    def __init__(self, app, pos, number):
        self.app = app
        self.grid_pos = pos
        self.starting_pos = [pos.x, pos.y]
        self.pix_pos = self.get_pix_pos()
        self.radius = int(self.app.cell_width // 2.3)
        self.number = number
        self.colour = self.set_colour()
        self.personality = self.set_personality()
        self.target = None
        self.direction = vec(0, 0)
        self.speed = self.set_speed()

    # return the position of the enemy on the grid
    def get_pix_pos(self):
        return vec((self.grid_pos.x * self.app.cell_width) + Gap // 2 + self.app.cell_width // 2,
                   (self.grid_pos.y * self.app.cell_height) + Gap // 2 + self.app.cell_height // 2)

    # creates a different image for each enemy
    def set_colour(self):
        if self.number == 0:
            return pygame.image.load("assets/blue_monster_4_20.png")
        if self.number == 1:
            return pygame.image.load("assets/purple_monster_20.png")
        if self.number == 2:
            return pygame.image.load("assets/green_monster_20.png")
        if self.number == 3:
            return pygame.image.load("assets/gray_monster_20.png")

    # sets a diffrent personality trait to each enemy
    def set_personality(self):
        if self.number == 0:
            return "speedy"
        elif self.number == 1:
            return "slow"
        elif self.number == 2:
            return "random"
        else:
            return "scared"

    # Draws the enemy on the screen
    def draw(self):
        self.app.screen.blit(self.colour, (int(self.pix_pos.x)-10, int(self.pix_pos.y)-10))

    # Sets the speedy and slow enemies to chase the player
    def set_target(self):
        if self.personality == "speedy" or self.personality == "slow":
            return self.app.player.grid_pos
        else:
            if self.app.player.grid_pos[0] > COLS//2 and self.app.player.grid_pos[1] > ROWS//2:
                return vec(1, 1)
            if self.app.player.grid_pos[0] > COLS//2 and self.app.player.grid_pos[1] < ROWS//2:
                return vec(1, ROWS-2)
            if self.app.player.grid_pos[0] < COLS//2 and self.app.player.grid_pos[1] > ROWS//2:
                return vec(COLS-2, 1)
            else:
                return vec(COLS-2, ROWS-2)

    # Detects if the enemy is in the middle of the wall cell
    def time_to_move(self):
        if int(self.pix_pos.x + Gap // 2) % self.app.cell_width == 0:
            if self.direction == vec(1, 0) or self.direction == vec(-1, 0) or self.direction == vec(0, 0):
                return True

        if int(self.pix_pos.y + Gap // 2) % self.app.cell_width == 0:
            if self.direction == vec(0, 1) or self.direction == vec(0, -1) or self.direction == vec(0, 0):
                return True
        return False

    # sets the movement speed of each enemy
    def set_speed(self):
        if self.personality in ["speedy", "scared", "random"]:
            speed = 1.2
        else:
            speed = 1
        return speed

    # Defines the movement direction of each enemy
    def move(self):
        if self.personality == "random":
            self.direction = self.get_random_direction()
        if self.personality == "slow":
            self.direction = self.get_path_direction(self.target)
        if self.personality == "speedy":
            self.direction = self.get_path_direction(self.target)
        if self.personality == "scared":
            self.direction = self.get_path_direction(self.target)

    # Works out the enemies path direction to the player
    def get_path_direction(self, target):
        next_cell = self.find_next_move(target)
        xdir = next_cell[0] - self.grid_pos[0]
        ydir = next_cell[1] - self.grid_pos[1]
        return vec(xdir, ydir)

    # Finds an eligible next move to chase the player
    def find_next_move(self, target):
        path = self.bfs([int(self.grid_pos.x), int(self.grid_pos.y)], [int(target[0]), int(target[1])])
        return path[1]

    # Works out best possible path to the player from the enemy
    def bfs(self, start, target):
        grid = [[0 for x in range(28)] for x in range(30)]
        for cell in self.app.walls:
            if cell.x < 28 and cell.y < 30:
                grid[int(cell.y)][int(cell.x)] = 1
        queue = [start]
        path = []
        visited = []
        while queue:  # Creates a dictionary of sequence of steps for the enemy to follow
            current = queue[0]
            queue.remove(queue[0])
            visited.append(current)
            if current == target:  # breaks out of loop if player is found
                break
            else:  # checks each possible grid positions for the next best step
                neighbours = [[0, -1], [1, 0], [0, 1], [-1, 0]]
                for neighbour in neighbours:
                    if neighbour[0]+current[0] >= 0 and neighbour[0] + current[0] < len(grid[0]):
                        if neighbour[1]+current[1] >= 0 and neighbour[1] + current[1] < len(grid):
                            next_cell = [neighbour[0] + current[0], neighbour[1] + current[1]]
                            if next_cell not in visited:
                                if grid[next_cell[1]][next_cell[0]] != 1:
                                    queue.append(next_cell)
                                    path.append({"Current": current, "Next": next_cell})
        shortest = [target]
        while target != start:  # works backwards through the path to create a sequence of steps for the enemy
            for step in path:
                if step["Next"] == target:
                    target = step["Current"]
                    shortest.insert(0, step["Current"])
        return shortest

    # Randomises the direction for the random enemy
    def get_random_direction(self):
        while True:
            number = random.randint(-2, 1)
            if number == -2:
                x_dir, y_dir = 1, 0
            elif number == -1:
                x_dir, y_dir = 0, 1
            elif number == 0:
                x_dir, y_dir = -1, 0
            else:
                x_dir, y_dir = 0, -1
            next_pos = vec(self.grid_pos.x + x_dir, self.grid_pos.y + y_dir)
            if next_pos not in self.app.walls:  # checks that the random position for the enemy is in the maze
                break
        return vec(x_dir, y_dir)

    # updates the position of the enemy on the screen in the set direction
    def update(self):
        self.target = self.set_target()
        if self.target != self.grid_pos:
            self.pix_pos += self.direction * self.speed
            if self.time_to_move():
                self.move()

        # setting grid position in reference to grid position
        self.grid_pos[0] = (self.pix_pos[0] - Gap + self.app.cell_width // 2) // self.app.cell_width + 1
        self.grid_pos[1] = (self.pix_pos[1] - Gap + self.app.cell_height // 2) // self.app.cell_height + 1
