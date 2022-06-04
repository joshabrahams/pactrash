import pygame
import sys
from Button import *


pygame.init()

screen = pygame.display.set_mode((610, 670))
pygame.display.set_caption("PacMan")

BG = pygame.image.load("assets/Background.png")


def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)


def menu_logic(self, menu_name, play_x, play_y, inst_x, inst_y, inst_image, inst_btn_text, quit_x, quit_y):
    screen.blit(BG, (0, 0))

    menu_mouse_pos = pygame.mouse.get_pos()

    menu_text = get_font(50).render(menu_name, True, "#b68f40")
    menu_rect = menu_text.get_rect(center=(305, 100))

    play_button = Button(image=None, pos=(play_x, play_y), text_input="PLAY", font=get_font(30), base_color="#d7fcd4",
                         hovering_color="White")
    instructions_button = Button(image=inst_image, pos=(inst_x, inst_y), text_input=inst_btn_text, font=get_font(30),
                                 base_color="#d7fcd4", hovering_color="White")
    quit_button = Button(image=None, pos=(quit_x, quit_y), text_input="QUIT", font=get_font(30), base_color="#d7fcd4",
                         hovering_color="White")

    screen.blit(menu_text, menu_rect)

    for btn in [play_button, instructions_button, quit_button]:
        btn.change_color(menu_mouse_pos)
        btn.update(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if play_button.check_for_input(menu_mouse_pos):
                self.state = 'playing'
                # self.play()
            if instructions_button.check_for_input(menu_mouse_pos):
                self.instructions_menu()
                # add instructions
            if quit_button.check_for_input(menu_mouse_pos):
                pygame.quit()
                sys.exit()


class App:
    def __init__(self):
        self.running = True
        self.state = 'start'

    def run(self):
        while self.running:
            if self.state == 'start':
                self.main_menu()

    def main_menu(self):
        while True:
            menu_name = "Pac Trash"
            play_x = 305
            play_y = 200
            inst_x = 305
            inst_y = 350
            inst_image = None
            inst_btn_text = "INSTRUCTIONS"
            quit_x = 305
            quit_y = 500

            menu_logic(self, menu_name, play_x, play_y, inst_x, inst_y, inst_image, inst_btn_text, quit_x, quit_y)

            pygame.display.update()

    def instructions_menu(self):
        while True:
            menu_name = "Instructions"
            play_x = 205
            play_y = 500
            inst_x = 305
            inst_y = 300
            inst_image = pygame.image.load("assets/Instructions.png")
            inst_btn_text = ""
            quit_x = 405
            quit_y = 500

            menu_logic(self, menu_name, play_x, play_y, inst_x, inst_y, inst_image, inst_btn_text, quit_x, quit_y)

            pygame.display.update()
