import sys
from Button import *
from Player import *
from Enemy import *
from Leaderboard import *

pygame.init()
vec = pygame.math.Vector2

screen = pygame.display.set_mode((610, 670))
pygame.display.set_caption("PacMan")

BG = pygame.image.load("assets/Background.png")


def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)


def menu_logic(self, menu_name, play_x, play_y, play_btn_text, inst_x, inst_y, inst_image, inst_btn_text, quit_x,
               quit_y):
    screen.blit(BG, (0, 0))

    menu_mouse_pos = pygame.mouse.get_pos()

    menu_text = get_font(50).render(menu_name, True, "#b68f40")
    menu_rect = menu_text.get_rect(center=(305, 100))

    play_button = Button(image=None, pos=(play_x, play_y), text_input=play_btn_text, font=get_font(30),
                         base_color="#d7fcd4",
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
                self.play()
            if instructions_button.check_for_input(menu_mouse_pos):
                self.instructions_menu()
                # add instructions
            if quit_button.check_for_input(menu_mouse_pos):
                pygame.quit()
                sys.exit()


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

    def run(self):
        while self.running:
            if self.state == 'start':
                self.login_player_name_screen()
                # self.main_menu()

    def main_menu(self):
        while True:
            menu_name = "Pac Trash"
            play_x = 305
            play_y = 200
            play_btn_text = "PLAY"
            inst_x = 305
            inst_y = 350
            inst_image = None
            inst_btn_text = "INSTRUCTIONS"
            quit_x = 305
            quit_y = 500

            menu_logic(self, menu_name, play_x, play_y, play_btn_text, inst_x, inst_y, inst_image, inst_btn_text,
                       quit_x, quit_y)

            pygame.display.update()

    def instructions_menu(self):
        while True:
            menu_name = "Instructions"
            play_x = 205
            play_y = 500
            play_btn_text = "PLAY"
            inst_x = 305
            inst_y = 300
            inst_image = pygame.image.load("assets/Instructions.png")
            inst_btn_text = ""
            quit_x = 405
            quit_y = 500

            menu_logic(self, menu_name, play_x, play_y, play_btn_text, inst_x, inst_y, inst_image, inst_btn_text,
                       quit_x, quit_y)

            pygame.display.update()

    def game_over_menu(self):
        while True:
            menu_name = "Pac Trash"
            play_x = 305
            play_y = 200
            play_btn_text = "PLAY AGAIN"
            inst_x = 305
            inst_y = 350
            inst_image = None
            inst_btn_text = "INSTRUCTIONS"
            quit_x = 305
            quit_y = 500

            menu_logic(self, menu_name, play_x, play_y, play_btn_text, inst_x, inst_y, inst_image, inst_btn_text,
                       quit_x, quit_y)

            pygame.display.update()

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

    def draw_coins(self):
        x = 0
        for coin in self.coins:
            x = x + 1
            pygame.draw.circle(self.screen, (124, 123, 7), (
                int(coin.x * self.cell_width) + self.cell_width // 2 + Gap // 2,
                int(coin.y * self.cell_height) + self.cell_height // 2 + Gap // 2), 5)

        if self.player.stored_direction is None and self.player.grid_pos == [1, 1]:
            assert x == 287

    # playing functions
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

    def playing_update(self):
        self.player.update()
        for enemy in self.enemies:
            enemy.update()

        for enemy in self.enemies:
            if enemy.grid_pos == self.player.grid_pos:
                self.remove_life()

    def make_enemies(self):
        for idx, pos in enumerate(self.e_pos):
            self.enemies.append(Enemy(self, vec(pos), idx))

    def remove_life(self):
        self.player.lives -= 1
        if self.player.lives == 0:
            add_score(self.player_name, self.player.current_score)
            self.state = "game over"
        else:
            self.player.grid_pos = vec(self.player.starting_pos)
            self.player.pix_pos = self.player.get_pix_pos()
            self.player.direction *= 0
            for enemy in self.enemies:
                enemy.grid_pos = vec(enemy.starting_pos)
                enemy.pix_pos = enemy.get_pix_pos()
                enemy.direction *= 0

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

    def login_player_name_screen(self):

        base_font = pygame.font.Font(None, 32)
        user_text = ''

        input_player_name_rect = pygame.Rect(200, 200, 140, 32)

        button_rect = pygame.Rect(200, 400, 140, 32)

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
            screen.fill((255, 255, 255))

            if active:
                input_color = input_color_active
                button_color = button_color_active
            else:
                input_color = input_color_passive
                button_color = button_color_passive

            # draw rectangle and argument passed which should
            # be on screen

            draw_text('PacMan Login', self.screen, [300, 55], 24, Black,
                      Start_Font)

            draw_text('Enter Your Player Name:', self.screen, [200, 180], 18, Black,
                      Start_Font)

            pygame.draw.rect(screen, input_color, input_player_name_rect)
            pygame.draw.rect(screen, button_color, button_rect)

            text_surface = base_font.render(user_text, True, (255, 255, 255))

            self.screen.blit(self.font.render('Next >>', True, (255, 0, 0)), (230, 400))
            pygame.display.update()

            # render at position stated in arguments
            screen.blit(text_surface, (input_player_name_rect.x + 5, input_player_name_rect.y + 5))

            # set width of textfield so that text cannot get
            # outside of user's text input
            input_player_name_rect.w = max(100, text_surface.get_width() + 10)

            # display.flip() will update only a portion of the
            # screen to updated, not full area
            pygame.display.flip()
