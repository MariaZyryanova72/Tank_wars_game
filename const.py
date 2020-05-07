# coding=utf-8
import pygame
import os
# Файл констант

def load_sound(filename, sound_lvl=1.0):
    path = os.path.join('static', 'sound', filename)
    sound = pygame.mixer.Sound(path)
    sound.set_volume(sound_lvl)  # Настройка громкости звука
    return sound


LENGTH_ENEMY = 52
WIDTH_ENEMY = 35

LENGTH_ENEMY_SHOOTING = 51
WIDTH_ENEMY_SHOOTING = 61

LENGTH_SHOOTING_ENEMY = 15
WIDTH_SHOOTING_ENEMY = 25


LENGTH_PLAYER = 95
WIDTH_PLAYER = 89


LENGTH_SHOOTING = 17
WIDTH_SHOOTING = 12


LENGTH_EXPLOSION = 64
WIDTH_EXPLOSION = 60


WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 750

INIT_ENERGY = 100

DISPLAYMODE = (WINDOW_WIDTH, WINDOW_HEIGHT)
FPS = 40
RATE_ENEMY_SPEED = 2
DELAY_EXPLOSION = 5
MAX_NUMBER_ENEMY = 5
RATE_PLAYER_SPEED = 3

COUNT_SHOOTING = 50
COUNT_ENEMY = 10

# Шрифты
pygame.init()
window = pygame.display.set_mode(DISPLAYMODE)
TEXTCOLOR = (255, 255, 255)
font_1 = pygame.font.SysFont("Impact", 22)
font_2 = pygame.font.SysFont("Impact", 15)
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
FONT = pygame.font.Font(None, 32)

# Настроить звуки
intro_sound = load_sound('intro.ogg', 0.3)
explosion_enemy = load_sound('explosion_enemy.ogg', 0.3)
shooting_player = load_sound("shooting_player.ogg", 0.3)
shooting_enemy = load_sound('shooting_enemy.ogg', 0.3)
explosion_player = load_sound("explosion_player.ogg", 0.3)
hit_player = load_sound("explosion_player.ogg", 0.3)

music_channel = pygame.mixer.Channel(4)