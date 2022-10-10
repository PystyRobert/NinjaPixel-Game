from menu import *
from enemy import *
from pygame import mixer
import pygame
import random
from os import path

pygame.font.init()

WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

# Title and Icon
pygame.display.set_caption("Ninja Pixel")
icon = pygame.image.load("ninjapixel.png")
pygame.display.set_icon(icon)

# Enemies
ENEMY_RED = pygame.image.load("target red.png")
ENEMY_BLUE = pygame.image.load("target blue.png")
ENEMY_GREEN = pygame.image.load("target green.png")
ENEMY_YELLOW = pygame.image.load("target yellow.png")
ENEMY_DBLUE = pygame.image.load("target Dblue.png")
ENEMY_PINK = pygame.image.load("target pink.png")
ENEMY_TEAL = pygame.image.load("target teal.png")

# Player
PLAYER = pygame.image.load("char1.png")
PLAYER2 = pygame.image.load("char attack.png")
PLAYER_R = pygame.image.load("move_r.png")
PLAYER_L = pygame.image.load("move_l.png")

# Weapons
WEAPON = pygame.image.load("shuriken.png")

# Background
BG = pygame.transform.scale(pygame.image.load("background.gif"), (WIDTH, HEIGHT))

HS_FILE = "highscore.txt"


class Game:
    def __init__(self):
        pygame.init()
        self.game_mode = "Default"
        self.diff = "Easy"
        self.run, self.play = True, False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.CLICK = False, False, False, False, False
        self.DISPLAY_W, self.DISPLAY_H = 800, 600
        self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
        self.window = pygame.display.set_mode((self.DISPLAY_W, self.DISPLAY_H))
        self.background = pygame.transform.scale(pygame.image.load("background.gif"), (self.DISPLAY_W, self.DISPLAY_H))
        self.bg1 = pygame.transform.smoothscale(pygame.image.load("background1.jpg"), (self.DISPLAY_W, self.DISPLAY_H))
        self.font_name = pygame.font.get_default_font()
        self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255)
        self.RED, self.GREEN, self.BLUE = (255, 0, 0), (0, 255, 0), (0, 0, 255)
        self.main_menu = MainMenu(self)
        self.curr_menu = self.main_menu
        self.main_font = pygame.font.Font("freesansbold.ttf", 32)
        self.lost_font = pygame.font.Font("freesansbold.ttf", 64)
        self.load_data()
        self.FPS = 60
        self.clock = pygame.time.Clock()

        self.movement = pygame.mouse.get_pos()

    def load_data(self):
        # load high score
        self.dir = path.dirname(__file__)
        with open(path.join(self.dir, HS_FILE), 'w') as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0

    def collision(self, obj):
        return collide(self, obj)

    def blit_screen(self):
        self.window.blit(self.display, (0, 0))
        pygame.display.update()
        self.reset_keys()

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.play = False
                if event.type == pygame.KEYUP:
                    pass
                if event.type == pygame.MOUSEBUTTONDOWN:
                    waiting = False

    def sounds(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            hit_sound = mixer.Sound("menuSelect.mp3")
            hit_sound.set_volume(0.7)
            hit_sound.play()
        if keys[pygame.K_ESCAPE]:
            hit_sound = mixer.Sound("menuSelect.mp3")
            hit_sound.set_volume(0.7)
            hit_sound.play()
        if keys[pygame.K_DOWN]:
            hit_sound = mixer.Sound("menuSelect.mp3")
            hit_sound.set_volume(0.7)
            hit_sound.play()
        if keys[pygame.K_UP]:
            hit_sound = mixer.Sound("menuSelect.mp3")
            hit_sound.set_volume(0.7)
            hit_sound.play()

    def game_loop(self):
        self.level = 0
        self.lives = 5
        self.score = 0
        self.lost_count = 0
        self.enemies = []
        self.wave_lenght = 5
        self.enemy_vel = 0.80

        self.hit = 0

        self.player_vel = 8
        self.weapon_vel = 5
        self.player = Player(self.DISPLAY_W / 2, self.DISPLAY_H - 128)
        self.enemy = Enemy(random.randrange(50, self.DISPLAY_W - 100),
                      random.randrange(-1500, -100),
                      random.choice(["red", "green", "blue", "yellow", "dblue", "pink", "teal"]))
        self.time = 0
        self.lost = False

        while self.play:
            self.check_events()
            self.clock.tick(self.FPS)
            self.display.blit(self.background, (0, 0))
            self.window.blit(self.display, (0, 0))
            self.redraw_window()

            # Check if lost is false
            if not self.lost:
                for enemy in self.enemies[:]:
                    enemy.move(self.enemy_vel)
                    if enemy.y + enemy.get_height() > self.DISPLAY_H:
                        self.lives -= 1
                        self.enemies.remove(enemy)
                self.time += 1

                if self.game_mode == "Default":

                    if self.score > self.highscore:
                        self.highscore = self.score
                        with open(path.join(self.dir, HS_FILE), "w") as f:
                            f.write(str(self.score))

                    # Difficulty changer

                    if self.diff == "Easy":
                        if len(self.enemies) == 0:
                            self.level += 1
                            self.wave_lenght += 1
                            self.enemy_vel += 0.1
                            for i in range(self.wave_lenght):
                                enemy = Enemy(random.randrange(50, self.DISPLAY_W - 100),
                                              random.randrange(-700, -100),
                                              random.choice(["red", "green", "blue", "yellow", "dblue", "pink", "teal"]))
                                self.enemies.append(enemy)
                        if self.time > 250:
                            self.time = 0
                            self.score += 1
                            self.lives += 1

                    if self.diff == "Normal":
                        if len(self.enemies) == 0:
                            self.level += 1
                            self.wave_lenght += 1
                            self.enemy_vel += 0.3
                            for i in range(self.wave_lenght):
                                enemy = Enemy(random.randrange(50, self.DISPLAY_W - 100),
                                              random.randrange(-1000, -100),
                                              random.choice(["red", "green", "blue", "yellow", "dblue", "pink", "teal"]))
                                self.enemies.append(enemy)
                        if self.time > 500:
                            self.time = 0
                            self.score += 1
                            self.lives += 1

                    if self.diff == "Hard":
                        if len(self.enemies) == 0:
                            self.level += 1
                            self.wave_lenght += 1
                            self.enemy_vel += 0.5
                            for i in range(self.wave_lenght):
                                enemy = Enemy(random.randrange(50, self.DISPLAY_W - 100),
                                              random.randrange(-1500, -100),
                                              random.choice(["red", "green", "blue", "yellow", "dblue", "pink", "teal"]))
                                self.enemies.append(enemy)
                        if self.time > 750:
                            self.time = 0
                            self.score += 1
                            self.lives += 1

                    if self.diff == "VeryHard":
                        if len(self.enemies) == 0:
                            self.level += 1
                            self.wave_lenght += 1
                            self.enemy_vel += 1
                            for i in range(self.wave_lenght):
                                enemy = Enemy(random.randrange(50, self.DISPLAY_W - 100),
                                              random.randrange(-2000, -100),
                                              random.choice(["red", "green", "blue", "yellow", "dblue", "pink", "teal"]))
                                self.enemies.append(enemy)
                        if self.time > 1000:
                            self.time = 0
                            self.score += 1
                            self.lives += 1

                if self.game_mode == "Sharpshooter":

                    if self.level > self.highscore:
                        self.highscore = self.level
                        with open(path.join(self.dir, HS_FILE), "w") as f:
                            f.write(str(self.level))

                    if len(self.enemies) == 0:
                        self.level += 1
                        self.wave_lenght += 1
                        self.enemy_vel = 0
                        for i in range(self.wave_lenght):
                            enemy = Enemy(random.randrange(50, self.DISPLAY_W - 100),
                                          random.randrange(0, 250),
                                          random.choice(["red", "green", "blue", "yellow", "dblue", "pink", "teal"]))
                            self.enemies.append(enemy)
                    if self.time > 60:
                        self.time = 0
                        self.score += 1

                    if self.score > 20:
                        self.lost = True

                if self.game_mode == "Survival":
                    if len(self.enemies) == 0:
                        self.level += 1
                        self.wave_lenght += 1
                        self.enemy_vel += 0.3
                        for i in range(self.wave_lenght):
                            enemy = Enemy(random.randrange(50, self.DISPLAY_W - 100),
                                          random.randrange(-1000, -100),
                                          random.choice(["red", "green", "blue", "yellow", "dblue", "pink", "teal"]))
                            self.enemies.append(enemy)
                    if self.time > 500:
                        self.time = 0
                        self.score += 1
                        self.lives += 1

            # If lost game stops
            if self.lives <= 0:
                self.lost = True
                self.lost_count += 1

            if self.lost:
                self.play = False
                self.show_defeat_screen()

            # Player Movement
            keys = pygame.key.get_pressed()
            if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and self.player.x - self.player_vel > 0:  # Left
                self.player.x -= self.player_vel
                self.player.moveleft()
            if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and self.player.x + self.player_vel + self.player.get_width() < self.DISPLAY_W:  # Right
                self.player.x += self.player_vel
                self.player.moveright()
            if keys[pygame.K_SPACE]:
                self.player.shoot()

            self.player.move_weapons(- self.weapon_vel, self.enemies)

            if self.BACK_KEY:
                self.sounds()
                self.play = False
                self.curr_menu = self.main_menu
                self.run_dissplay = False

            pygame.display.update()
            self.reset_keys()

    def redraw_window(self):
        self.window.blit(self.background, (0, 0))
        # Draw Text
        lives_label = self.main_font.render(f"Lives : {self.lives}", 1, (255, 255, 255))
        level_label = self.main_font.render(f"Level : {self.level}", 1, (255, 255, 255))
        time_label = self.main_font.render(f"Time : {int(self.time)}", 1, (255, 255, 255))
        score_label = self.main_font.render(f"Score : {self.score}", 1, (255, 255, 255))
        highscore_label = self.main_font.render(f"Highscore : {self.highscore}", 1, (255, 255, 255))

        for enemy in self.enemies:
            enemy.draw(self.window)

        self.player.draw(self.window)

        self.window.blit(lives_label, (10, 10))
        self.window.blit(score_label, (self.DISPLAY_W / 2 - score_label.get_width() / 2 - 100, 10))
        self.window.blit(time_label, (self.DISPLAY_W / 2 - time_label.get_width() / 2 + 100, 10))
        self.window.blit(level_label, (self.DISPLAY_W - level_label.get_width() - 10, 10))

        pygame.display.update()

    def show_start_screen(self):
        # start screen / control keys
        self.display.fill(self.BLACK)
        self.display.blit(self.background, (0, 0))
        self.draw_text("Ninja Adventure", 60, self.DISPLAY_W / 2, self.DISPLAY_H / 7)
        self.draw_text("Left - A , Right - D , Shoot - Space", 40, self.DISPLAY_W / 2, self.DISPLAY_H / 2)
        self.draw_text("Press click to play", 40, self.DISPLAY_W / 2, self.DISPLAY_H / 2 + 100)
        self.blit_screen()
        pygame.display.update()

    def show_defeat_screen(self):
        # game over screen / retry
        self.display.fill(self.BLACK)
        self.display.blit(self.background, (0, 0))
        self.draw_text("Defeat", 60, self.DISPLAY_W / 2, self.DISPLAY_H / 2 - 120)
        self.draw_text("High Score: " + str(self.highscore), 40, self.DISPLAY_W / 2, self.DISPLAY_H / 2)
        self.draw_text("Press click to retry", 20, self.DISPLAY_W / 2, self.DISPLAY_H / 2 + 160)
        self.curr_menu = self.main_menu
        self.blit_screen()
        pygame.display.update()

    # check what keys are pressed and functions
    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.CLICK = True
                self.movement = pygame.mouse.get_pos()
                print(self.movement)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_ESCAPE:
                    self.BACK_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True
            if event.type == pygame.KEYUP:
                self.reset_keys()

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False

    def draw_text(self, text, size, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.display.blit(text_surface, text_rect)


class Weapon:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x + 16, self.y + 10))

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return not (self.y <= height and self.y >= 0)

    def collision(self, obj):
        return collide(self, obj)

# General class
class Gen:
    COOLDOWN = 30

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.def_img = None
        self.weapon_img = None
        self.weapons = []
        self.cool_down_counter = 0
        self.state = "Idle"

    def draw(self, window):
        window.blit(self.def_img, (self.x, self.y))
        for weapon in self.weapons:
            weapon.draw(window)

    def move_weapons(self, vel, obj):
        self.cooldown()
        for weapon in self.weapons:
            weapon.move(vel)
            if weapon.off_screen(HEIGHT):
                self.weapons.remove(weapon)
            elif weapon.collision(obj):
                self.weapons.remove(weapon)

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def moveright(self):
        if self.state == "Idle" or self.state == "Attack" or self.state == "MoveLeft":
            self.state = "MoveRight"
            self.def_img = PLAYER_R

    def moveleft(self):
        if self.state == "Idle" or self.state == "Attack" or self.state == "MoveRight":
            self.state = "MoveLeft"
            self.def_img = PLAYER_L

    def shoot(self):
        # Aicia merge

        if self.cool_down_counter == 0:
            weapon = Weapon(self.x, self.y, self.weapon_img)
            self.weapons.append(weapon)
            shuriken_sound = mixer.Sound("shuriken.mp3")
            shuriken_sound.set_volume(0.1)
            shuriken_sound.play()
            self.cool_down_counter = 1

            if self.state == "Idle" or self.state == "MoveLeft" or self.state == "MoveRight":
                self.state = "Attack"
                self.def_img = PLAYER2
            elif self.state == "Attack" or self.state == "MoveRight" or self.state == "MoveLeft":
                self.state = "Idle"
                self.def_img = PLAYER

    def get_width(self):
        return self.def_img.get_width()

    def get_height(self):
        return self.def_img.get_height()


class Player(Gen):
    def __init__(self, x, y,):
        super().__init__(x, y)
        self.def_img = PLAYER
        self.weapon_img = WEAPON
        self.mask = pygame.mask.from_surface(self.def_img)

    def move_weapons(self, vel, objs):
        self.cooldown()
        for weapon in self.weapons:
            weapon.move(vel)
            if weapon.off_screen(HEIGHT):
                self.weapons.remove(weapon)
            else:
                for obj in objs:
                    if weapon.collision(obj):
                        objs.remove(obj)
                        hit_sound = mixer.Sound("hit.mp3")
                        hit_sound.set_volume(0.04)
                        hit_sound.play()
                        if weapon in self.weapons:
                            self.weapons.remove(weapon)


def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) is not None
