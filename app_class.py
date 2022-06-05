import sys
from Button import *
from Player import *

pygame.init()
vec = pygame.math.Vector2

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
                self.play()
            if instructions_button.check_for_input(menu_mouse_pos):
                self.instructions_menu()
                # add instructions
            if quit_button.check_for_input(menu_mouse_pos):
                pygame.quit()
                sys.exit()


def draw_text(sentence, scrn, pos, size, colour, font_name):
    font = pygame.font.SysFont(font_name, size)
    text = font. render(sentence, False, colour)
    text_size = text.get_size()
    pos[0] = pos[0]-text_size[0]//2
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

    def play(self):
        while self.running:
            if self.state == 'playing':
                self.playing_draw()
                self.playing_events()
                self.playing_update()
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
        draw_text('HIGH SCORE: 0', self.screen, [width // 2 + 150, 15], 18, White, Start_Font)

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
