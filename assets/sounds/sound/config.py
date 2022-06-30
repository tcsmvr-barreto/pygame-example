import pygame, time, math
from random import randint,randrange
from pygame.locals import *


COLORS = {
	'black'     : (0, 0, 0), 
	'white'     : (255, 255, 255),
	'red'       : (255, 0, 0),
	'green'     : (0, 128, 0),
	'blue'      : (0, 0, 255),
	'yellow'    : (255, 255, 0),
	'orange'    : (255, 128, 0),
  	'lime'      : (0, 255, 0),
  	'purple'    : (128, 0, 255),
  	'cyan'      : (0, 255, 255),
  	'ice'       : (90, 255, 255),
	'light-red' : (255, 90, 90),
	'dark-gray' : (25, 25, 25)
}

vec = pygame.math.Vector2 # basically just (x,y)
HEIGHT = 450
WIDTH = 400
ACC = 0.5 #def = default
ACC_ICE = 0.75
acc = ACC
FRIC = -0.12 #def = default
FRIC_ICE = -0.03
fric = FRIC
FPS = 60
HWEIIDGTHHT = (WIDTH,HEIGHT)
BUMPDIST_START = 100
bumpDist = BUMPDIST_START

pickup_safe = 0
pickup_place = 0

P1 = None
PT1 = None
all_sprites = None
platforms = None
pickups = None
bombs = None
all_players = pygame.sprite.Group()
all_bumpers = pygame.sprite.Group()
PLACED_COUNT = 0

