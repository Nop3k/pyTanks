import pygame
from settings import *
import sys


class Tank(pygame.sprite.Sprite):
    _counter = 0
    _registry = []

    def __init__(self, game, name, x, y):
        self._registry.append(self)
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.name = name
        self.type = 'PzKpfw VI Tiger'
        self.image = pygame.Surface((32, 32))
        self.image.fill(GRAY)
        self.rect = self.image.get_rect()
        self.move(x, y)  # spawn tank on battlefield
        Tank._counter += 1
        self.id = Tank._counter
        self.hp = 100
        self.damage = 35

    def move(self, x, y):
        if x * TILESIZE < BATTLEFIELD_WIDTH and y * TILESIZE < BATTLEFIELD_HEIGHT:
            self.rect.x = x * TILESIZE
            self.rect.y = y * TILESIZE

    def update(self):
        if self.hp <= 0:
            print("BYEBYE")
            self.kill()

class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()

        self.WIN = pygame.display.set_mode(
            (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.battlefield = pygame.Rect((0, 0), (
            BATTLEFIELD_WIDTH, BATTLEFIELD_HEIGHT))
        self.menu = pygame.Rect((BATTLEFIELD_WIDTH, 0),
                                (MENU_WIDTH, MENU_HEIGHT))
        self.myfont = pygame.font.SysFont('Comic Sans MS', 14)
        pygame.display.set_caption("pyTanks!")
        self.all_sprites = pygame.sprite.Group()

        self.clock = pygame.time.Clock()

        self.selected_unit = []
        self.targeted_unit = []
        self.wittman = Tank(self, 'M. Wittman', 5, 5)
        self.knispel = Tank(self, 'K. Knispel', 5, 7)
        self.draw_menu()

    def create_grid(self):
        for x in range(0, SCREEN_WIDTH, TILESIZE):
            pygame.draw.line(self.WIN, BLACK, (x, 0),
                             (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, TILESIZE):
            pygame.draw.line(self.WIN, BLACK, (0, y),
                             (SCREEN_WIDTH, y))

    def draw_window(self):
        self.WIN.fill(BLACK, self.battlefield)  # background (menu)
        pygame.draw.rect(self.WIN, GREEN_GRASS, self.battlefield)
        self.create_grid()
        self.all_sprites.draw(self.WIN)
        pygame.display.update(self.battlefield)

    def draw_menu(self):
        self.WIN.fill(BLACK, self.menu)

        unit_selected_string = 'Currently selected: '
        if self.selected_unit:
            unit_selected_string += f'{self.selected_unit.name} ' \
                                    f'- {self.selected_unit.type} ' \
                                    f'[{self.selected_unit.id}]'
        s1 = self.myfont.render(unit_selected_string,
                                True,
                                WHITE)
        self.WIN.blit(s1, (BATTLEFIELD_WIDTH + 10, 10))

        unit_targeted_string = 'Current target: '
        if self.targeted_unit:
            unit_targeted_string += f'{self.targeted_unit.name} ' \
                                    f'- {self.targeted_unit.type} ' \
                                    f'[{self.targeted_unit.id}]'
        s2 = self.myfont.render(unit_targeted_string,
                                True,
                                WHITE)
        self.WIN.blit(s2, (BATTLEFIELD_WIDTH + 10, 34))

        self.button_fire = pygame.Rect(
            (BATTLEFIELD_WIDTH + 25, MENU_HEIGHT // 8),
            (100, 28))
        pygame.draw.rect(self.WIN, GRAY, self.button_fire)

        button_fire_text = self.myfont.render('Fire!', True, WHITE)
        self.WIN.blit(button_fire_text, (
            BATTLEFIELD_WIDTH + 25 + 50 - button_fire_text.get_width() // 2,
            MENU_HEIGHT // 8 + 14 - button_fire_text.get_height() // 2))

        button_2 = pygame.Rect((BATTLEFIELD_WIDTH + 150, MENU_HEIGHT // 8),
                               (100, 28))
        button_3 = pygame.Rect((BATTLEFIELD_WIDTH + 275, MENU_HEIGHT // 8),
                               (100, 28))
        pygame.draw.rect(self.WIN, GRAY, button_2)
        pygame.draw.rect(self.WIN, GRAY, button_3)

        pygame.display.update(self.menu)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x_pos, mouse_y_pos = pygame.mouse.get_pos()
                battlefield_clicked = self.battlefield.collidepoint(
                    mouse_x_pos,
                    mouse_y_pos)
                menu_clicked = self.menu.collidepoint(mouse_x_pos, mouse_y_pos)

                if battlefield_clicked:
                    if event.button == LMB:
                        self.get_selected_unit_sprite()
                    if event.button == RMB:
                        self.move_selected_sprite()
                    if event.button == MMB:
                        self.get_target_sprite()

                if menu_clicked:
                    if event.button == LMB:
                        if self.button_fire.collidepoint(mouse_x_pos,
                                                         mouse_y_pos):
                            self.fire_at_target()

    def get_selected_unit_sprite(self):
        x, y = pygame.mouse.get_pos()
        if x < BATTLEFIELD_WIDTH and y < BATTLEFIELD_HEIGHT:
            self.selected_unit = next((sprite for sprite in self.all_sprites if
                                       sprite.rect.collidepoint(x, y)),
                                      None)
            self.targeted_unit = None

        self.draw_menu()

    def get_target_sprite(self):
        x, y = pygame.mouse.get_pos()
        if self.selected_unit:  # only target if unit is selected
            if x < BATTLEFIELD_WIDTH and y < BATTLEFIELD_HEIGHT:
                self.targeted_unit = next(
                    (sprite for sprite in self.all_sprites if
                     sprite.rect.collidepoint(x, y)), None)
        self.draw_menu()

    def move_selected_sprite(self):
        if self.selected_unit:  # only move if unit is selected
            x, y = pygame.mouse.get_pos()
            self.selected_unit.move(x // TILESIZE, y // TILESIZE)

    def run(self):
        self.run = True
        while self.run:
            self.clock.tick(FPS)
            self.all_sprites.update()
            self.handle_events()
            self.draw_window()

    def fire_at_target(self):
        if self.targeted_unit:
            print("FIRE AT", self.targeted_unit.name, self.targeted_unit.type)
            self.targeted_unit.hp -= self.selected_unit.damage
            print(
                f'{self.selected_unit.name} damaged for {self.selected_unit.damage} DMG',
                f'{self.targeted_unit.name} = {self.targeted_unit.hp} HP')
        elif not self.selected_unit:
            print("SELECT UNIT FIRST")
        else:
            print("NO TARGET")

    def quit(self):
        pygame.quit()
        sys.exit()


g = Game()
g.run()
