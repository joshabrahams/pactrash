# This module controls the player position and movement
# Author: Josh Abrahams

import pygame
from settings import *

vec = pygame.math.Vector2


class Player:
    def __init__(self, app, pos):
        self.app = app
        self.starting_pos = [pos.x, pos.y]
        self.grid_pos = pos
        self.pix_pos = self.get_pix_pos()
        self.direction = vec(1, 0)
        self.stored_direction = None
        self.able_to_move = True
        self.speed = 2
        self.lives = 3
        self.current_score = 0
        self.winner = ""

    # return the position of the player on the grid
    def get_pix_pos(self):
        return vec((self.grid_pos.x * self.app.cell_width) + Gap // 2 + self.app.cell_width // 2,
                   (self.grid_pos.y * self.app.cell_height) + Gap // 2 + self.app.cell_height // 2)

    # Drawing the player sprite to the screen
    def draw(self):
        image = pygame.image.load("assets/pacman_20.png")
        self.app.screen.blit(image, (int(self.pix_pos.x) - 10, int(self.pix_pos.y) - 10))

    # Drawing players lives on the bottom of the screen
        for x in range(self.lives):
            self.app.screen.blit(image, (40 + 30 * x, height - 25))

        assert self.starting_pos == [1, 1]  # checks that the player starts in the first grid cell

    # Updating the players position on the screen in the set direction
    def update(self):
        if self.able_to_move:
            self.pix_pos += self.direction * self.speed
        if self.time_to_move():
            if self.stored_direction is not None:
                self.direction = self.stored_direction
            self.able_to_move = self.can_move()

        # Sets players position in the middle of the cell so that they are not on the walls
        self.grid_pos[0] = (self.pix_pos[0] - Gap + self.app.cell_width // 2) // self.app.cell_width + 1
        self.grid_pos[1] = (self.pix_pos[1] - Gap + self.app.cell_height // 2) // self.app.cell_height + 1

        # Checks to see if the player is on rubbish and if so remove rubbish
        if self.on_rubbish():
            self.eat_rubbish()

        assert self.grid_pos == (
            self.grid_pos[0], self.grid_pos[1])  # check that the player sprite has moved to the correct position

    # Detects if the player is in the middle of the wall cell
    def time_to_move(self):
        if int(self.pix_pos.x + Gap // 2) % self.app.cell_width == 0:
            if self.direction == vec(1, 0) or self.direction == vec(-1, 0) or self.direction == vec(0, 0):
                return True

        if int(self.pix_pos.y + Gap // 2) % self.app.cell_width == 0:
            if self.direction == vec(0, 1) or self.direction == vec(0, -1) or self.direction == vec(0, 0):
                return True

    # Checks if the player is able to move into the next grid space without hitting a wall
    def can_move(self):
        for wall in self.app.walls:
            if vec(self.grid_pos + self.direction) == wall:
                return False
        return True

    # Keeps player moving in the same direction
    def move(self, direction):
        self.stored_direction = direction

    # Player sprite is on top of the rubbish icon
    def on_rubbish(self):
        if self.grid_pos in self.app.coins:
            if int(self.pix_pos.x + Gap // 2) % self.app.cell_width == 0:
                if self.direction == vec(1, 0) or self.direction == vec(-1, 0):
                    return True
            if int(self.pix_pos.y + Gap // 2) % self.app.cell_width == 0:
                if self.direction == vec(0, 1) or self.direction == vec(0, -1):
                    return True
        return False

    # Removes the rubbish element from the array and adds 1 to the current score
    def eat_rubbish(self):
        self.app.coins.remove(self.grid_pos)
        self.current_score += 1
        if len(self.app.coins) == 0:  # if no rubbish left then player wins
            self.winner = "winner"



