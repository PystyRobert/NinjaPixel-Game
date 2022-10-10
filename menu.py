import pygame, sys, random
from pygame import mixer
from game import *
pygame.init()
mixer.music.load("menuMusic.mp3")
mixer.music.set_volume(0.08) # 0.08
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Ninja Pixel")
icon = pygame.image.load("ninjapixel.png")
pygame.display.set_icon(icon)


class Menu:
    def __init__(self, game):
        self.game = game
        self.run_dissplay = True
        self.cursor_rect = pygame.Rect(0, 0, 40, 40)
        self.offset = - 150

    def draw_cursor(self):
        self.game.draw_text(">", 40, self.cursor_rect.x, self.cursor_rect.y)

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()


class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        self.mid_w, self.mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2
        self.state = "Start"
        self.startx, self.starty = self.mid_w, self.mid_h + 60
        self.settingsx, self.settingsy = self.mid_w, self.mid_h + 120
        self.creditx, self.credity = self.mid_w, self.mid_h + 180
        self.quitx, self.quity = self.mid_w, self.mid_h + 240
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
        self.run_dissplay = True

        while self.run_dissplay:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.display.blit(self.game.bg1, (0, 0))
            self.game.draw_text("Main Menu", 70, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 100)
            self.game.draw_text("Start Game", 40, self.startx, self.starty)
            self.game.draw_text("Settings", 40, self.settingsx, self.settingsy)
            self.game.draw_text("Credits", 40, self.creditx, self.credity)
            self.game.draw_text("Quit Game", 40, self.quitx, self.quity)
            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        if self.game.CLICK:
            pass
        if self.game.DOWN_KEY:
            if self.state == "Start":
                self.cursor_rect.midtop = (self.settingsx + self.offset, self.settingsy)
                self.state = "Settings"
                self.game.sounds()
            elif self.state == "Settings":
                self.cursor_rect.midtop = (self.creditx + self.offset, self.credity)
                self.state = "Credits"
                self.game.sounds()
            elif self.state == "Credits":
                self.cursor_rect.midtop = (self.quitx + self.offset, self.quity)
                self.state = "Quit Game"
                self.game.sounds()
            elif self.state == "Quit Game":
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = "Start"
                self.game.sounds()

        elif self.game.UP_KEY:
            if self.state == "Quit Game":
                self.cursor_rect.midtop = (self.creditx + self.offset, self.credity)
                self.state = "Credits"
                self.game.sounds()
            elif self.state == "Settings":
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = "Start"
                self.game.sounds()
            elif self.state == "Credits":
                self.cursor_rect.midtop = (self.settingsx + self.offset, self.settingsy)
                self.state = "Settings"
                self.game.sounds()
            elif self.state == "Start":
                self.cursor_rect.midtop = (self.quitx + self.offset, self.quity)
                self.state = "Quit Game"
                self.game.sounds()

        if self.game.START_KEY:
            if self.state == "Start":
                self.game.sounds()
                self.game.curr_menu = GameModeMenu(self.game)
            elif self.state == "Settings":
                self.game.sounds()
                self.game.curr_menu = SettingsMenu(self.game)
            elif self.state == "Credits":
                self.game.sounds()
                self.game.curr_menu = CreditsMenu(self.game)
            elif self.state == "Quit Game":
                self.game.sounds()
                self.game.curr_menu = QuitMenu(self.game)
            self.run_dissplay = False


class QuitMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        self.mid_w, self.mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2
        self.state = "Yes"
        self.yesx, self.yesy = self.mid_w, self.mid_h + 60
        self.nox, self.noy = self.mid_w, self.mid_h + 120
        self.cursor_rect.midtop = (self.yesx + self.offset, self.yesy)
        self.run_dissplay = True

        while self.run_dissplay:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.display.blit(self.game.bg1, (0, 0))
            self.game.draw_text("Quit Game", 70, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 100)
            self.game.draw_text("Yes", 40, self.yesx, self.yesy)
            self.game.draw_text("No", 40, self.nox, self.noy)
            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        if self.game.BACK_KEY:
            self.game.sounds()
            self.game.curr_menu = self.game.main_menu
            self.run_dissplay = False

        elif self.game.UP_KEY or self.game.DOWN_KEY:
            if self.state == "Yes":
                self.state = "No"
                self.cursor_rect.midtop = (self.nox + self.offset, self.noy)
                self.game.sounds()
            elif self.state == "No":
                self.state = "Yes"
                self.cursor_rect.midtop = (self.yesx + self.offset, self.yesy)
                self.game.sounds()
        elif self.game.START_KEY:
            if self.state == "Yes":
                pygame.quit()
                sys.exit()
            elif self.state == "No":
                self.game.sounds()
                self.game.curr_menu = self.game.main_menu
                self.run_dissplay = False


class SettingsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        self.mid_w, self.mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2
        self.state = "Volume"
        self.volx, self.voly = self.mid_w, self.mid_h + 60
        self.controlx, self.controly = self.mid_w, self.mid_h + 120
        self.graphx, self.graphy = self.mid_w, self.mid_h + 180
        self.cursor_rect.midtop = (self.volx + self.offset, self.voly)
        self.run_dissplay = True

        while self.run_dissplay:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.display.blit(self.game.bg1, (0, 0))
            self.game.draw_text("Settings", 70, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 100)
            self.game.draw_text("Volume", 40, self.volx, self.voly)
            self.game.draw_text("Controls", 40, self.controlx, self.controly)
            self.game.draw_text("Graphics", 40, self.graphx, self.graphy)
            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        if self.game.BACK_KEY:
            self.game.sounds()
            self.game.curr_menu = self.game.main_menu
            self.run_dissplay = False

        elif self.game.DOWN_KEY:
            if self.state == "Volume":
                self.state = "Controls"
                self.cursor_rect.midtop = (self.controlx + self.offset, self.controly)
                self.game.sounds()
            elif self.state == "Controls":
                self.state = "Graphics"
                self.cursor_rect.midtop = (self.graphx + self.offset, self.graphy)
                self.game.sounds()
            elif self.state == "Graphics":
                self.state = "Volume"
                self.cursor_rect.midtop = (self.volx + self.offset, self.voly)
                self.game.sounds()

        elif self.game.UP_KEY:
            if self.state == "Volume":
                self.state = "Graphics"
                self.cursor_rect.midtop = (self.graphx + self.offset, self.graphy)
                self.game.sounds()
            elif self.state == "Controls":
                self.state = "Volume"
                self.cursor_rect.midtop = (self.volx + self.offset, self.voly)
                self.game.sounds()
            elif self.state == "Graphics":
                self.state = "Controls"
                self.cursor_rect.midtop = (self.controlx + self.offset, self.controly)
                self.game.sounds()

        elif self.game.START_KEY:
            if self.state == "Graphics":
                self.game.sounds()
                self.game.curr_menu = Graphics(self.game)
                self.run_dissplay = False


class Graphics(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        self.mid_w, self.mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2
        self.state = "640 x 480"
        self.res1x, self.res1y = self.mid_w, self.mid_h + 60
        self.res2x, self.res2y = self.mid_w, self.mid_h + 100
        self.res3x, self.res3y = self.mid_w, self.mid_h + 140
        self.cursor_rect.midtop = (self.res1x + self.offset, self.res1y)
        self.run_dissplay = True

        while self.run_dissplay:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.display.blit(self.game.bg1, (0, 0))
            self.game.draw_text("Resolutions", 70, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 100)
            self.game.draw_text("640 x 480", 30, self.res1x, self.res1y)
            self.game.draw_text("800 x 600 (Default)", 30, self.res2x, self.res2y)
            self.game.draw_text("1366 x 768", 30, self.res3x, self.res3y)
            self.draw_cursor()
            self.blit_screen()

    def change_res(self):
        self.game.display = pygame.Surface((self.game.DISPLAY_W, self.game.DISPLAY_H))
        self.game.window = pygame.display.set_mode((self.game.DISPLAY_W, self.game.DISPLAY_H))
        self.game.background = pygame.transform.scale(pygame.image.load("background.gif"), (self.game.DISPLAY_W, self.game.DISPLAY_H))
        self.game.bg1 = pygame.transform.smoothscale(pygame.image.load("background1.jpg"), (self.game.DISPLAY_W, self.game.DISPLAY_H))
        self.game.curr_menu = self.game.main_menu
        self.run_dissplay = False

    def check_input(self):
        if self.game.BACK_KEY:
            self.game.sounds()
            self.game.curr_menu = self.game.main_menu
            self.run_dissplay = False

        elif self.game.DOWN_KEY:
            if self.state == "640 x 480":
                self.state = "800 x 600"
                self.cursor_rect.midtop = (self.res2x + self.offset, self.res2y)
                self.game.sounds()
            elif self.state == "800 x 600":
                self.state = "1366 x 768"
                self.cursor_rect.midtop = (self.res3x + self.offset, self.res3y)
                self.game.sounds()
            elif self.state == "1366 x 768":
                self.state = "640 x 480"
                self.cursor_rect.midtop = (self.res1x + self.offset, self.res1y)
                self.game.sounds()

        elif self.game.UP_KEY:
            if self.state == "640 x 480":
                self.state = "1366 x 768"
                self.cursor_rect.midtop = (self.res3x + self.offset, self.res3y)
                self.game.sounds()
            elif self.state == "1366 x 768":
                self.state = "800 x 600"
                self.cursor_rect.midtop = (self.res2x + self.offset, self.res2y)
                self.game.sounds()
            elif self.state == "800 x 600":
                self.state = "640 x 480"
                self.cursor_rect.midtop = (self.res1x + self.offset, self.res1y)
                self.game.sounds()

        elif self.game.START_KEY:
            if self.state == "640 x 480":
                self.game.sounds()
                self.game.DISPLAY_W, self.game.DISPLAY_H = 640, 480
                self.change_res()
            elif self.state == "800 x 600":
                self.game.sounds()
                self.game.DISPLAY_W, self.game.DISPLAY_H = 800, 600
                self.change_res()
            elif self.state == "1366 x 768":
                self.game.sounds()
                self.game.DISPLAY_W, self.game.DISPLAY_H = 1366, 768
                self.change_res()


class CreditsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        self.run_dissplay = True
        while self.run_dissplay:
            self.game.check_events()
            if self.game.BACK_KEY:
                self.game.sounds()
                self.game.curr_menu = self.game.main_menu
                self.run_dissplay = False
            self.game.display.fill(self.game.BLACK)
            self.game.display.blit(self.game.bg1, (0, 0))
            self.game.draw_text("Credits", 70, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 100)
            self.game.draw_text("Team :", 30, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 60)
            self.game.draw_text("- Pysty", 30, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 100)
            self.game.draw_text("Design and pictures :", 30, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 180)
            self.game.draw_text("- Pysty", 30, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 220)
            self.blit_screen()


class LevelMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        self.mid_w, self.mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2
        self.state = "Easy"
        self.easyx, self.easyy = self.mid_w, self.mid_h + 60
        self.normalx, self.normaly = self.mid_w, self.mid_h + 120
        self.hardx, self.hardy = self.mid_w, self.mid_h + 180
        self.vhardx, self.vhardy = self.mid_w, self.mid_h + 240
        self.cursor_rect.midtop = (self.easyx + self.offset, self.easyy)
        self.run_dissplay = True

        while self.run_dissplay:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.display.blit(self.game.background, (0, 0))
            self.game.draw_text("Levels", 70, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 100)
            self.game.draw_text("Easy", 40, self.easyx, self.easyy)
            self.game.draw_text("Normal", 40, self.normalx, self.normaly)
            self.game.draw_text("Hard", 40, self.hardx, self.hardy)
            self.game.draw_text("Very Hard", 40, self.vhardx, self.vhardy)
            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        if self.game.BACK_KEY:
            self.game.sounds()
            self.game.curr_menu = GameModeMenu(self.game)
            self.run_dissplay = False

        elif self.game.DOWN_KEY:
            if self.state == "Easy":
                self.state = "Normal"
                self.cursor_rect.midtop = (self.normalx + self.offset, self.normaly)
                self.game.sounds()
            elif self.state == "Normal":
                self.state = "Hard"
                self.cursor_rect.midtop = (self.hardx + self.offset, self.hardy)
                self.game.sounds()
            elif self.state == "Hard":
                self.state = "VeryHard"
                self.cursor_rect.midtop = (self.vhardx + self.offset, self.vhardy)
                self.game.sounds()
            elif self.state == "VeryHard":
                self.state = "Easy"
                self.cursor_rect.midtop = (self.easyx + self.offset, self.easyy)
                self.game.sounds()

        elif self.game.UP_KEY:
            if self.state == "Easy":
                self.state = "VeryHard"
                self.cursor_rect.midtop = (self.vhardx + self.offset, self.vhardy)
                self.game.sounds()
            elif self.state == "VeryHard":
                self.state = "Hard"
                self.cursor_rect.midtop = (self.hardx + self.offset, self.hardy)
                self.game.sounds()
            elif self.state == "Hard":
                self.state = "Normal"
                self.cursor_rect.midtop = (self.normalx + self.offset, self.normaly)
                self.game.sounds()
            elif self.state == "Normal":
                self.state = "Easy"
                self.cursor_rect.midtop = (self.easyx + self.offset, self.easyy)
                self.game.sounds()

        elif self.game.START_KEY:
            if self.state == "Easy":
                self.game.sounds()
                self.game.diff = "Easy"
                self.game.curr_menu = self.game.play = True
            elif self.state == "Normal":
                self.game.sounds()
                self.game.diff = "Normal"
                self.game.curr_menu = self.game.play = True
            elif self.state == "Hard":
                self.game.sounds()
                self.game.diff = "Hard"
                self.game.curr_menu = self.game.play = True
            elif self.state == "VeryHard":
                self.game.sounds()
                self.game.diff = "VeryHard"
                self.game.curr_menu = self.game.play = True
            self.run_dissplay = False


class GameModeMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        self.mid_w, self.mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2
        self.state = "Default"
        self.defaultx, self.defaulty = self.mid_w, self.mid_h + 60
        self.sharpsx, self.sharpsy = self.mid_w, self.mid_h + 120
        self.survivalx, self.survivaly = self.mid_w, self.mid_h + 180
        self.cursor_rect.midtop = (self.defaultx + self.offset, self.defaulty)
        self.run_dissplay = True

        while self.run_dissplay:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.display.blit(self.game.background, (0, 0))
            self.game.draw_text("Game Mode", 70, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 100)
            self.game.draw_text("Normal", 40, self.defaultx, self.defaulty)
            self.game.draw_text("Sharpshooter", 40, self.sharpsx, self.sharpsy)
            self.game.draw_text("Survival", 40, self.survivalx, self.survivaly)
            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        if self.game.BACK_KEY:
            self.game.sounds()
            self.game.curr_menu = self.game.main_menu
            self.run_dissplay = False

        elif self.game.DOWN_KEY:
            if self.state == "Default":
                self.state = "Sharpshooter"
                self.cursor_rect.midtop = (self.sharpsx + self.offset, self.sharpsy)
                self.game.sounds()
            elif self.state == "Sharpshooter":
                self.state = "Survival"
                self.cursor_rect.midtop = (self.survivalx + self.offset, self.survivaly)
                self.game.sounds()
            elif self.state == "Survival":
                self.state = "Default"
                self.cursor_rect.midtop = (self.defaultx + self.offset, self.defaulty)
                self.game.sounds()

        elif self.game.UP_KEY:
            if self.state == "Default":
                self.state = "Survival"
                self.cursor_rect.midtop = (self.survivalx + self.offset, self.survivaly)
                self.game.sounds()
            elif self.state == "Survival":
                self.state = "Sharpshooter"
                self.cursor_rect.midtop = (self.sharpsx + self.offset, self.sharpsy)
                self.game.sounds()
            elif self.state == "Sharpshooter":
                self.state = "Default"
                self.cursor_rect.midtop = (self.defaultx + self.offset, self.defaulty)
                self.game.sounds()

        elif self.game.START_KEY:
            if self.state == "Default":
                self.game.sounds()
                self.game.game_mode = "Default"
                self.game.curr_menu = LevelMenu(self.game)
            elif self.state == "Sharpshooter":
                self.game.sounds()
                self.game.game_mode = "Sharpshooter"
                self.game.curr_menu = self.game.play = True
            elif self.state == "Survival":
                self.game.sounds()
                self.game.game_mode = "Survival"
                self.game.curr_menu = self.game.play = True
            self.run_dissplay = False
