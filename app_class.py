# This module drives the game play
# Author: Josh Abrahams

import sys
from Button import *
from Player import *
from Enemy import *
from Leaderboard import *

pygame.init()
vec = pygame.math.Vector2

screen = pygame.display.set_mode((610, 670))
pygame.display.set_caption("Pac Trash")

# set background images
BG = pygame.image.load("assets/Background.png")
LB = pygame.image.load("assets/leaderboard_background.png")
SB = pygame.image.load("assets/login_background.png")


def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)


# Reusable logic for defining each menu screen
def menu_logic(self, menu_name, play_x, play_y, play_btn_text, inst_x, inst_y, inst_image, inst_btn_text, quit_x,
               quit_y, lead_btn_text, lead_x, lead_y, back_x, back_y, back_btn_text, top10):
    screen.blit(BG, (0, 0))

    menu_mouse_pos = pygame.mouse.get_pos()

    menu_text = get_font(40).render(menu_name, True, "#b68f40")
    menu_rect = menu_text.get_rect(center=(305, 50))

    play_button = Button(image=None, pos=(play_x, play_y), text_input=play_btn_text, font=get_font(30),
                         base_color="#d7fcd4",
                         hovering_color="White")
    instructions_button = Button(image=inst_image, pos=(inst_x, inst_y), text_input=inst_btn_text, font=get_font(30),
                                 base_color="#d7fcd4", hovering_color="White")
    leaderboard_button = Button(image=None, pos=(lead_x, lead_y), text_input=lead_btn_text, font=get_font(30),
                                 base_color="#d7fcd4", hovering_color="White")
    quit_button = Button(image=None, pos=(quit_x, quit_y), text_input="QUIT", font=get_font(30), base_color=(255,48,48),
                         hovering_color="White")
    back_button = Button(image=None, pos=(back_x, back_y), text_input=back_btn_text, font=get_font(30), base_color="#d7fcd4",
                         hovering_color="White")

    screen.blit(menu_text, menu_rect)

    # returns the top 10 leaderboard scores for the leaderboard menu screen
    if top10:
        col_header = 85
        row_pos = 130
        z = 1
        for line in self.sortlist:
            draw_text('RANK', self.screen, [100, col_header], 35, (255, 255, 255),
                      Start_Font)
            draw_text('NAME', self.screen, [300, col_header], 35, (255, 255, 255),
                      Start_Font)
            draw_text('SCORE', self.screen, [500, col_header], 35, (255, 255, 255),
                      Start_Font)
            draw_text(str(z), self.screen, [100, row_pos], 25, (255, 255, 255),
                      Start_Font)
            draw_text(line[0], self.screen, [300, row_pos], 25, (255, 255, 255),
                      Start_Font)
            draw_text(line[1], self.screen, [500, row_pos], 25, (255, 255, 255),
                      Start_Font)
            row_pos += 40
            z += 1

    # Sets the behaviour for each button
    for btn in [play_button, instructions_button, leaderboard_button, quit_button, back_button]:
        btn.change_color(menu_mouse_pos)
        btn.update(screen)

    # Defines the click action for each button
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if play_button.check_for_input(menu_mouse_pos):
                self.state = 'playing'
                self.play()
            if instructions_button.check_for_input(menu_mouse_pos):
                self.instructions_menu()
                # add instructions
            if leaderboard_button.check_for_input(menu_mouse_pos):
                self.top10_menu()
                # self.leaderboard_screen()
            if quit_button.check_for_input(menu_mouse_pos):
                pygame.quit()
                sys.exit()
            if back_button.check_for_input(menu_mouse_pos):
                self.main_menu()

# A function to draw onto the screen
def draw_text(sentence, scrn, pos, size, colour, font_name):
    font = pygame.font.SysFont(font_name, size)
    text = font.render(sentence, False, colour)
    text_size = text.get_size()
    pos[0] = pos[0] - text_size[0] // 2
    pos[1] = pos[1] - text_size[1] // 2
    scrn.blit(text, pos)


class App:
    def __init__(self):
        self.running = True
        self.state = 'start'
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((width, height))
        self.maze = pygame.image.load('assets/maze.png')
        self.maze = pygame.transform.scale(self.maze, (maze_width, maze_height))
        self.coins = []
        self.walls = []
        self.cell_width = maze_width // COLS
        self.cell_height = maze_height // ROWS
        self.e_pos = []
        self.p_pos = 0
        self.enemies = []
        self.font = pygame.font.SysFont('Arial', 25)
        self.player_name = "Unknown"

        # Creates the maze on the screen
        with open("assets/walls.txt", 'r') as file:
            for yidx, line in enumerate(file):
                for xidx, char in enumerate(line):
                    if char == "1":
                        self.walls.append(vec(xidx, yidx))
                    elif char == "C":
                        self.coins.append((vec(xidx, yidx)))
                    elif char == "P":
                        self.p_pos = [xidx, yidx]
                    elif char in ["2", "3", "4", "5"]:
                        self.e_pos.append([xidx, yidx])
                    elif char == "B":
                        pygame.draw.rect(self.maze, Black, (
                            xidx * self.cell_width, yidx * self.cell_height, self.cell_width, self.cell_height))

        self.player = Player(self, vec(self.p_pos))
        self.make_enemies()
        self.leaderboard = Leaderboard()
        self.leaderboard.high_score()

        self.sortlist = []

        # loads the leaderboard data into an array
        with open("assets/leaderboard.csv", "r") as file:
            reader = csv.reader(file)
            next(reader, None)

            for i in reader:
                if len(i) != 0 and len(i) == 2:
                    self.sortlist.append(i)

            def sort_second(val):
                return int(val[1])

            self.sortlist = sorted(self.sortlist, key=sort_second, reverse=True)[:10]

    # Captures the game start event and sends the user to the login screen
    def run(self):
        while self.running:
            if self.state == 'start':
                self.login_player_name_screen()

    # defines the button and text position on the main menu screen
    def main_menu(self):
        while True:
            menu_name = "Pac Trash"
            play_x = 305
            play_y = 150
            play_btn_text = "PLAY"
            inst_x = 305
            inst_y = 300
            inst_image = None
            inst_btn_text = "INSTRUCTIONS"
            quit_x = 530
            quit_y = 640
            lead_btn_text = "LEADERBOARD"
            lead_x = 305
            lead_y = 450
            back_x = 600
            back_y = 650
            back_btn_text = ""
            top10 = False

            menu_logic(self, menu_name, play_x, play_y, play_btn_text, inst_x, inst_y, inst_image, inst_btn_text, quit_x,
               quit_y, lead_btn_text, lead_x, lead_y, back_x, back_y, back_btn_text, top10)

            pygame.display.update()

    # defines the button and text position on the instructions screen
    def instructions_menu(self):
        while True:
            menu_name = "Instructions"
            play_x = 200
            play_y = 500
            play_btn_text = "PLAY"
            inst_x = 305
            inst_y = 300
            inst_image = pygame.image.load("assets/Instructions.png")
            inst_btn_text = ""
            quit_x = 530
            quit_y = 640
            lead_x = 305
            lead_y = 300
            lead_btn_text = ""
            back_x = 400
            back_y = 500
            back_btn_text = "BACK"
            top10 = False

            menu_logic(self, menu_name, play_x, play_y, play_btn_text, inst_x, inst_y, inst_image, inst_btn_text, quit_x,
               quit_y, lead_btn_text, lead_x, lead_y, back_x, back_y, back_btn_text, top10)

            pygame.display.update()

    # defines the button and text position on the leaderboard screen
    def top10_menu(self):
        while True:
            menu_name = "LEADERBOARD"
            play_x = 200
            play_y = 530
            play_btn_text = "PLAY"
            inst_x = 305
            inst_y = 300
            inst_image = None
            inst_btn_text = ""
            quit_x = 530
            quit_y = 640
            lead_x = 305
            lead_y = 300
            lead_btn_text = ""
            back_x = 400
            back_y = 530
            back_btn_text = "BACK"
            top10 = True

            menu_logic(self, menu_name, play_x, play_y, play_btn_text, inst_x, inst_y, inst_image, inst_btn_text, quit_x,
               quit_y, lead_btn_text, lead_x, lead_y, back_x, back_y, back_btn_text, top10)

            pygame.display.update()

    # defines the button and text position on the game over screen
    def game_over_menu(self):
        while True:
            menu_name = "GAME OVER"
            play_x = 305
            play_y = 200
            play_btn_text = "PLAY AGAIN"
            inst_x = 305
            inst_y = 350
            inst_image = None
            inst_btn_text = "INSTRUCTIONS"
            quit_x = 305
            quit_y = 500
            lead_x = 305
            lead_y = 300
            lead_btn_text = ""
            back_x = 600
            back_y = 650
            back_btn_text = ""
            top10 = False


            menu_logic(self, menu_name, play_x, play_y, play_btn_text, inst_x, inst_y, inst_image, inst_btn_text, quit_x,
                       quit_y, lead_btn_text, lead_x, lead_y, back_x, back_y, back_btn_text, top10)

            pygame.display.update()

    # defines the button and text position on the winner menu screen
    def winner_menu(self):
        while True:
            menu_name = "Winner"
            play_x = 200
            play_y = 520
            play_btn_text = "PLAY"
            inst_x = 305
            inst_y = 300
            inst_image = pygame.image.load("assets/Winner.png")
            inst_btn_text = ""
            quit_x = 530
            quit_y = 640
            lead_x = 305
            lead_y = 300
            lead_btn_text = ""
            back_x = 400
            back_y = 520
            back_btn_text = "BACK"
            top10 = False

            menu_logic(self, menu_name, play_x, play_y, play_btn_text, inst_x, inst_y, inst_image, inst_btn_text, quit_x,
               quit_y, lead_btn_text, lead_x, lead_y, back_x, back_y, back_btn_text, top10)

            pygame.display.update()

    # Creates the events for playing the game
    def play(self):
        while self.running:
            if self.state == 'playing':
                self.playing_draw()
                self.playing_events()
                self.playing_update()
            elif self.state == 'game over':
                self.reset()
                self.game_over_menu()
            else:
                self.running = False

            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()

    # Draws the game screen with the current score, player name and high score
    def playing_draw(self):
        self.screen.fill(Black)
        self.screen.blit(self.maze, (Gap // 2, Gap // 2))
        self.draw_coins()
        self.player.draw()
        draw_text('CURRENT SCORE: {}'.format(self.player.current_score), self.screen, [130, 15], 18, White,
                  Start_Font)
        draw_text('PLAYER: {}'.format(self.player_name), self.screen, [400, 655], 18, White,
                  Start_Font)
        draw_text('HIGH SCORE: {}'.format(self.leaderboard.highest_score), self.screen, [width // 2 + 150, 15], 18,
                  White, Start_Font)
        for enemy in self.enemies:
            enemy.draw()

        pygame.display.update()

    # Draws all rubbish icons on the maze
    def draw_coins(self):
        x = 0
        image = pygame.image.load("assets/full_trash_bin_15.png")
        for coin in self.coins:
            x = x + 1
            screen.blit(image, (int(coin.x * self.cell_width) + self.cell_width // 2 + Gap // 2 - 7.5,
                                               int(coin.y * self.cell_height) + self.cell_height // 2 + Gap // 2 - 7.5))

        # tests to see that all rubbish icons were drawn on the screen
        if self.player.stored_direction is None and self.player.grid_pos == [1, 1]:
            assert x == 287

    # defines the keys for moving the player sprite
    def playing_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.move(vec(-1, 0))
                if event.key == pygame.K_RIGHT:
                    self.player.move(vec(1, 0))
                if event.key == pygame.K_UP:
                    self.player.move(vec(0, -1))
                if event.key == pygame.K_DOWN:
                    self.player.move(vec(0, 1))

    # updates the position of the player and checks if they are in the same position as the enemy
    def playing_update(self):
        self.player.update()
        for enemy in self.enemies:
            enemy.update()

        for enemy in self.enemies:  # if true a player life is removed
            if enemy.grid_pos == self.player.grid_pos:
                self.remove_life()

        if self.player.winner == "winner":  # if player removes all rubbish icons user wins the game
            add_score(self.player_name,
                      self.player.current_score * self.player.lives)  # score is added up and multiplied by lives left
            self.winner_menu()

    # Draws the enemies onto the screen
    def make_enemies(self):
        for idx, pos in enumerate(self.e_pos):
            self.enemies.append(Enemy(self, vec(pos), idx))

    # Removes the players life
    def remove_life(self):
        self.player.lives -= 1
        if self.player.lives == 0:  # if no lives remaining than end the game
            add_score(self.player_name, self.player.current_score)
            self.state = "game over"
        else:  # sets the player and enemies back to their starting positions
            self.player.grid_pos = vec(self.player.starting_pos)
            self.player.pix_pos = self.player.get_pix_pos()
            self.player.direction *= 0
            for enemy in self.enemies:
                enemy.grid_pos = vec(enemy.starting_pos)
                enemy.pix_pos = enemy.get_pix_pos()
                enemy.direction *= 0

    # Resets the entire game screen so the player can play again
    def reset(self):
        self.player.lives = 3
        self.player.current_score = 0
        self.coins = []
        self.player.grid_pos = vec(self.player.starting_pos)
        self.player.pix_pos = self.player.get_pix_pos()
        self.player.direction *= 0
        for enemy in self.enemies:
            enemy.grid_pos = vec(enemy.starting_pos)
            enemy.pix_pos = enemy.get_pix_pos()
            enemy.direction *= 0
        with open("assets/walls.txt", 'r') as file:
            for yidx, line in enumerate(file):
                for xidx, char in enumerate(line):
                    if char == 'C':
                        self.coins.append(vec(xidx, yidx))
        self.state = "playing"

    # defines the login screen
    def login_player_name_screen(self):

        base_font = pygame.font.Font(None, 50)
        user_text = ''

        input_player_name_rect = pygame.Rect(155, 300, 140, 50)

        button_rect = pygame.Rect(230, 500, 140, 50)

        # color_active stores color(lightskyblue3) which
        # gets active when input box is clicked by user
        input_color_active = pygame.Color('lightskyblue3')
        button_color_active = pygame.Color('forestgreen')

        # color_passive store color(chartreuse4) which is
        # color of input box.
        input_color_passive = pygame.Color('chartreuse4')
        input_color = input_color_passive
        button_color_passive = pygame.Color('gainsboro')
        button_color = button_color_passive

        active = False

        while True:
            for event in pygame.event.get():

                # if user types QUIT then the screen will close
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if input_player_name_rect.collidepoint(event.pos):
                        active = True
                    elif button_rect.collidepoint(event.pos):
                        self.player_name = user_text
                        self.main_menu()
                    else:
                        active = False

                if event.type == pygame.KEYDOWN:

                    # Check for backspace
                    if event.key == pygame.K_BACKSPACE:

                        # get text input from 0 to -1 i.e. end.
                        user_text = user_text[:-1]

                    # Unicode standard is used for string
                    # formation
                    else:
                        user_text += event.unicode

            # it will set background color of screen
            screen.blit(SB, (0, 0))

            if active:
                input_color = input_color_active
                button_color = button_color_active
            else:
                input_color = input_color_passive
                button_color = button_color_passive

            # draw rectangle and argument passed which should
            # be on screen

            draw_text('LOGIN', self.screen, [305, 70], 50, White,
                      Start_Font)

            draw_text('PLAYER NAME', self.screen, [305, 270], 30, White,
                      Start_Font)

            pygame.draw.rect(screen, button_color, input_player_name_rect)
            pygame.draw.rect(screen, button_color, button_rect)

            text_surface = base_font.render(user_text, True, (0, 0, 0))

            self.screen.blit(self.font.render('ENTER', True, (0, 0, 0)), (260, 510))
            pygame.display.update()

            # render at position stated in arguments
            screen.blit(text_surface, (input_player_name_rect.x + 5, input_player_name_rect.y + 5))

            # set width of textfield so that text cannot get
            # outside of user's text input
            input_player_name_rect.w = max(300, text_surface.get_width() + 10)

            # display.flip() will update only a portion of the
            # screen to updated, not full area
            pygame.display.flip()

            self.clock.tick(60)

