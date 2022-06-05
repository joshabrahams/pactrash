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

    def get_pix_pos(self):
        return vec((self.grid_pos.x * self.app.cell_width) + Gap // 2 + self.app.cell_width // 2,
                   (self.grid_pos.y * self.app.cell_height) + Gap // 2 + self.app.cell_height // 2)

    def draw(self):
        pygame.draw.circle(self.app.screen, Player_Colour, (int(self.pix_pos.x), int(self.pix_pos.y)),
                           self.app.cell_width // 2 - 2)

        for x in range(self.lives):
            pygame.draw.circle(self.app.screen, Player_Colour, (40 + 30 * x, height - 15), 10)

        assert self.starting_pos == [1, 1]  # check that the player starts in the first grid cell

    def update(self):
        if self.able_to_move:
            self.pix_pos += self.direction * self.speed
        if self.time_to_move():
            if self.stored_direction is not None:
                self.direction = self.stored_direction
            self.able_to_move = self.can_move()

        self.grid_pos[0] = (self.pix_pos[0] - Gap + self.app.cell_width // 2) // self.app.cell_width + 1
        self.grid_pos[1] = (self.pix_pos[1] - Gap + self.app.cell_height // 2) // self.app.cell_height + 1

        if self.on_rubbish():
            self.eat_rubbish()

        assert self.grid_pos == (
            self.grid_pos[0], self.grid_pos[1])  # check that the player sprite has moved to the correct position

    def time_to_move(self):
        if int(self.pix_pos.x + Gap // 2) % self.app.cell_width == 0:
            if self.direction == vec(1, 0) or self.direction == vec(-1, 0) or self.direction == vec(0, 0):
                return True

        if int(self.pix_pos.y + Gap // 2) % self.app.cell_width == 0:
            if self.direction == vec(0, 1) or self.direction == vec(0, -1) or self.direction == vec(0, 0):
                return True

    def can_move(self):
        for wall in self.app.walls:
            if vec(self.grid_pos + self.direction) == wall:
                return False
        return True

    def move(self, direction):
        self.stored_direction = direction

    def on_rubbish(self):
        if self.grid_pos in self.app.coins:
            if int(self.pix_pos.x + Gap // 2) % self.app.cell_width == 0:
                if self.direction == vec(1, 0) or self.direction == vec(-1, 0):
                    return True
            if int(self.pix_pos.y + Gap // 2) % self.app.cell_width == 0:
                if self.direction == vec(0, 1) or self.direction == vec(0, -1):
                    return True
        return False

    def eat_rubbish(self):
        self.app.coins.remove(self.grid_pos)
