import pygame

from game import *
pygame.init()

# Enemies
ENEMY_RED = pygame.image.load("target red.png")
ENEMY_BLUE = pygame.image.load("target blue.png")
ENEMY_GREEN = pygame.image.load("target green.png")
ENEMY_YELLOW = pygame.image.load("target yellow.png")
ENEMY_DBLUE = pygame.image.load("target Dblue.png")
ENEMY_PINK = pygame.image.load("target pink.png")
ENEMY_TEAL = pygame.image.load("target teal.png")
# Weapons
WEAPON = pygame.image.load("shuriken.png")


class Enemy:
    COLOR_MAP = {
        "red": (ENEMY_RED, WEAPON),
        "green": (ENEMY_GREEN, WEAPON),
        "blue": (ENEMY_BLUE, WEAPON),
        "yellow": (ENEMY_YELLOW, WEAPON),
        "dblue": (ENEMY_DBLUE, WEAPON),
        "pink": (ENEMY_PINK, WEAPON),
        "teal": (ENEMY_TEAL, WEAPON),
    }

    def __init__(self, x, y, color):
        self.y = y
        self.x = x
        self.def_img = None
        self.weapon_img = None
        self.weapons = []
        self.cool_down_counter = 0
        self.def_img, self.weapon_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.def_img)

    def get_width(self):
        return self.def_img.get_width()

    def get_height(self):
        return self.def_img.get_height()

    def draw(self, window):
        window.blit(self.def_img, (self.x, self.y))
        for weapon in self.weapons:
            weapon.draw(window)

    def move(self, vel):

        self.y += vel


# make class/def for movement , border, appearance,
