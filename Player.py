import pygame
from settings import *

vec = pygame.math.Vector2


class Player:
    def __init__(self, app, pos):
        self.app = app
        self.starting_pos = [pos.x, pos.y]
        self.grid_pos = pos
        self.pix_pos = self.get_pix_pos()

    def get_pix_pos(self):
        return vec((self.grid_pos.x * self.app.cell_width) + Gap // 2 + self.app.cell_width // 2,
                   (self.grid_pos.y * self.app.cell_height) + Gap // 2 + self.app.cell_height // 2)

    def draw(self):
        pygame.draw.circle(self.app.screen, Player_Colour, (int(self.pix_pos.x), int(self.pix_pos.y)),
                           self.app.cell_width // 2 - 2)

        assert self.starting_pos == [1, 1]  # check that the player starts in the first grid cell
