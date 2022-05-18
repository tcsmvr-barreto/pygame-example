import pygame, time, math
from random import randint,randrange
from pygame.locals import *

# https://www.youtube.com/watch?v=iik25wqIuFo


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
	'light-red' : (255, 90, 90)
}

class Player(pygame.sprite.Sprite):
  def __init__(self):
    super().__init__()
    self.surf = pygame.Surface((30,30))
    self.surf.fill(COLORS['red'])
    self.rect = self.surf.get_rect()

    self.pos = vec((WIDTH/2,HEIGHT-35))
    self.vel = vec(0,0)
    self.acc = vec(0,0)

    self.jumping = False
    self.bouncing = False
    self.score = 0

  def move(self):
    self.acc = vec(0,0.5)

    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[K_LEFT]:
      self.acc.x = -acc
    if pressed_keys[K_RIGHT]:
      self.acc.x = acc
      
    self.acc.x += self.vel.x * fric
    self.vel += self.acc
    self.pos += self.vel + 0.5 * self.acc
    #  d     =     v     + 1/2 *    a

    hits = pygame.sprite.spritecollide(P1,platforms, False)
    if not hits:  
      if self.pos.x > (WIDTH+15) - bumpDist:
        self.pos.x = -15 + bumpDist
      if self.pos.x < -15 + bumpDist:
        self.pos.x = (WIDTH+15) - bumpDist
    
    self.rect.midbottom = self.pos

  def update(self):
    hits = pygame.sprite.spritecollide(P1,platforms, False)
    if self.vel.y > 0:
      for hit in hits:
        if self.rect.center[1] < hit.rect.bottom:
          self.pos.y = hit.rect.top + 1
          self.jumping = False 
          if hit.bounce and abs(self.vel.y) >= 1:
            self.vel.y = -abs(self.vel.y * 0.9)
            if not self.bouncing:
              self.bouncing = True
              self.vel.y -= 5
            self.vel.x = hit.speed
          else:
            self.vel.y = 0 
            self.bouncing = False
          # repeat for ice
          if hit.ice:
            acc = ACC_ICE
            fric = FRIC_ICE
          else:
            acc = ACC
            fric = FRIC
          if hit.vol and not hit.isCounting:
            hit.isCounting = True
            pygame.mixer.Sound.play(sound_vol_platform)
          self.jumping = False
          self.pos.x += hit.speed
          if hit.point:
            self.score += hit.rank
            hit.point = False
#abs(self.vel.y) + 2

  def jump(self):
    hits = pygame.sprite.spritecollide(P1,platforms, False)
    if hits and not self.jumping:
      self.jumping = True
      self.vel.y = -15

  def cancel_jump(self):
    if self.jumping:
      if self.vel.y < -3:
        self.vel.y = -3

class Platform(pygame.sprite.Sprite):
  def __init__(self):
    super().__init__()
    self.surf = pygame.Surface((randint(50,100),12))
    self.surf.fill(COLORS['blue'])
    self.rect = self.surf.get_rect(center = (randint(0, WIDTH),randint(0,HEIGHT-30)))

    self.speed = randint(-1,1)
    if self.speed == 0:
      self.moving = False
    else:
      self.moving = True
    self.point = True
    self.rank = 1
    self.bounce = False
    self.ice = False
    self.vol = False
    self.safe = False
    self.place = False
    if randint(1,100) > 70:
      if randint(1,100) > 85:
        self.ice = True
        self.surf = pygame.Surface((randint(75,150),12))
        self.surf.fill(COLORS['ice'])
        self.rect = self.surf.get_rect()
        self.rank = 3
      elif randint(1,100) < 11:
        self.vol = True
        self.surf.fill(COLORS['purple'])
        self.rect = self.surf.get_rect()
        self.rank = 3
        self.counter = 180
        self.isCounting = False
      else:
        self.bounce = True
        self.surf.fill(COLORS['lime'])
        self.rank = 2

  def move(self): # we changed the wrap around to tighten the screen width
    if self.moving:
      self.rect.centerx += self.speed
      if self.rect.left > WIDTH - bumpDist:
        hits = pygame.sprite.spritecollide(self,all_players,False)
        if hits:
          if hits[0].rect.left > WIDTH - bumpDist:
            offset = hits[0].rect.centerx - self.rect.centerx
            self.rect.right = bumpDist
            hits[0].rect.centerx = self.rect.centerx + offset
        else:
          self.rect.right = bumpDist
      if self.rect.right < bumpDist:
        hits = pygame.sprite.spritecollide(self,all_players,False)
        self.rect.left = WIDTH - bumpDist
        if hits:
          if hits[0].rect.right < bumpDist:
            offset = hits[0].rect.centerx - self.rect.centerx
            self.rect.left = WIDTH - bumpDist
            hits[0].rect.centerx = self.rect.centerx + offset

  def update(self):
    global PLACED_COUNT
    if self.vol and self.isCounting:
      self.counter -= 1
      if self.counter <= 0:
        if self.safe:
          PLACED_COUNT -= 1
        self.kill()
      else:
        t = f1.render(str(self.counter//60 + 1),True,COLORS['light-red'])
        color = self.surf.get_at((self.rect.width//2,self.rect.height//2))
        # t = f1.render(color.__str__(),True,COLORS['white'])
        offset = math.sqrt(max(color) // self.counter)
        self.surf.fill((max(color[0]-offset,0),max(color[1]-offset,0),max(color[2]-offset,0)))
        displaySurface.blit(t,(self.rect.center[0],self.rect.center[1]-6))


class Bumper(pygame.sprite.Sprite):
  def __init__(self,left):
    super().__init__()
    self.surf = pygame.Surface((WIDTH/2,HEIGHT))
    self.surf.fill(COLORS['red'])
    self.left = left
    self.bumpDist = BUMPDIST_START
    if left:
      self.rect = self.surf.get_rect(topright = (BUMPDIST_START,0))
    else:
      self.rect = self.surf.get_rect(topleft = (WIDTH-BUMPDIST_START,0))

  def move(self):
    pass

  def update(self,score):
    if type(score) == int and self.bumpDist > 0:
      self.bumpDist = BUMPDIST_START - score // 3
    if self.left:
      self.rect.right = self.bumpDist
    else:
      self.rect.left = WIDTH - self.bumpDist

class Pickup(pygame.sprite.Sprite):
  def __init__(self,type="PLACE"):
    super().__init__()
    self.surf = pygame.Surface((5,5))
    self.type = type
    if type == "PLACE":
      self.surf.fill(COLORS["orange"])
      #not volatile
    elif type == "SAFE":
      self.surf.fill(COLORS["cyan"])
      #volatile
    self.rect = self.surf.get_rect()

    self.platform = None

  def move(self):
    pass

  def update(self):
    global pickup_safe
    global pickup_place
    hits = pygame.sprite.spritecollideany(self, all_players)
    if hits:
      if self.type == "SAFE":
        pickup_safe += 1
      elif self.type == "PLACE":
        pickup_place += 1
      self.kill()
    else:
      self.rect.centerx = self.platform.rect.centerx


def plat_gen():
  global PLACED_COUNT
  while len(platforms) < 7+PLACED_COUNT:
    width = randint(50,100)
    p = None
    C = True
    while C:
      p = Platform()
      #modified their x range to fit inside
      p.rect.center = (randrange(0+bumpDist,WIDTH - width - bumpDist),randrange(-70,0))
      C = check(p,platforms)
    platforms.add(p)
    spawnPickup(p)
    all_sprites.add(p)

def check(platform,platforms):
  if pygame.sprite.spritecollideany(platform,platforms):
    return True
  else:
    for plat in platforms:
      if plat == platform:
        continue
      if abs(platform.rect.top - plat.rect.bottom) < 40 and abs(platform.rect.bottom - plat.rect.top) < 40:
        return True
    return False


def spawn_safe():
  global pickup_safe
  global all_sprites
  global platforms
  global PLACED_COUNT
  if pickup_safe > 0:
    PT1 = Platform()
    PT1.surf = pygame.Surface((WIDTH,12))
    PT1.surf.fill(COLORS['cyan'])
    PT1.rect = PT1.surf.get_rect(center = (WIDTH/2, HEIGHT - 6))
    PT1.moving = False
    PT1.speed = 0
    PT1.point = False
    PT1.bounce = False
    PT1.ice = False
    PT1.vol = True
    PT1.isCounting = True
    PT1.counter = 600
    PT1.safe = True
    all_sprites.add(PT1)
    platforms.add(PT1)
    pickup_safe -= 1
    PLACED_COUNT += 1

def spawn_place():
  global pickup_place
  global all_sprites
  global platforms
  global PLACED_COUNT
  if pickup_place > 0:
    PT1 = Platform()
    PT1.surf = pygame.Surface((50,12))
    PT1.surf.fill(COLORS['orange'])
    PT1.rect = PT1.surf.get_rect(center = pygame.mouse.get_pos())
    PT1.moving = False
    PT1.speed = 0
    PT1.point = False
    PT1.bounce = False
    PT1.vol = False
    PT1.ice = False
    PT1.place = True
    all_sprites.add(PT1)
    platforms.add(PT1)
    pickup_place -= 1
    PLACED_COUNT += 1

    

pygame.init()
sound_vol_platform = pygame.mixer.Sound("volatile3new.wav")
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
#HWEIIDGTHHT[0] , HWEIIDGTHHT[1]

FramePerSec = pygame.time.Clock()

displaySurface = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Game")

P1 = None
PT1 = None
all_sprites = None
platforms = None
pickups = None
all_players = pygame.sprite.Group()
all_bumpers = pygame.sprite.Group()
PLACED_COUNT = 0



def startGame():
  global pickups
  global all_sprites
  global all_players
  global pickup_place
  global pickup_safe
  global PLACED_COUNT
  pickup_place = 0
  pickup_safe = 0
  PLACED_COUNT = 0
  P1 = Player()
  PT1 = Platform()
  PT1.surf = pygame.Surface((WIDTH,12))
  PT1.surf.fill(COLORS['blue'])
  PT1.rect = PT1.surf.get_rect(center = (WIDTH/2, HEIGHT - 6))
  PT1.moving = False
  PT1.speed = 0
  PT1.point = False
  PT1.bounce = False
  PT1.ice = False
  PT1.vol = False
  all_sprites = pygame.sprite.Group()
  all_sprites.add(P1)
  all_sprites.add(PT1)
  platforms = pygame.sprite.Group()
  platforms.add(PT1)
  #all_players = pygame.sprite.Group()
  all_players.add(P1)
  bumpDist = BUMPDIST_START
  all_bumpers = pygame.sprite.Group()
  leftBumper = Bumper(True)
  rightBumper = Bumper(False)
  #TODO - FOR TESTING THE EDGES 
  leftBumper.surf.set_alpha(128)
  rightBumper.surf.set_alpha(128)
  all_bumpers.add(leftBumper)
  all_bumpers.add(rightBumper)
  pickups = pygame.sprite.Group()

  for x in range(randint(5,6)):
    C = True
    while C:
      p = Platform()
      p.rect.center = (randrange(0+bumpDist,WIDTH - p.rect.width - bumpDist),randrange(0,HEIGHT))
      C = check(p,platforms)
    platforms.add(p)
    spawnPickup(p)
    all_sprites.add(p)
  return P1,PT1,all_sprites,platforms,all_bumpers,pickups

def spawnPickup(platform):
  global pickups
  global all_sprites
  type = None
  if randint(1,100) > 80:
    if randint(1,100) > 75:
      type = "SAFE"
    else:
      type = "PLACE"
    pickup = Pickup(type)
    pickup.platform = platform
    pickup.rect.center = (platform.rect.x,platform.rect.y - 15)
    pickups.add(pickup)
    all_sprites.add(pickup)

f = pygame.font.SysFont("Times",16)
f1 = pygame.font.SysFont("Arial",12)

gameOver = True

while True:
  if gameOver:
    P1,PT1,all_sprites,platforms,all_bumpers,pickups = startGame()
    gameOver = False

  for event in pygame.event.get():
    if event.type == QUIT:
      pygame.quit()
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_SPACE:
        P1.jump()
      if event.key == pygame.K_s:
        spawn_safe()
      if event.key == pygame.K_a:
        spawn_place()
    if event.type == pygame.KEYUP:
      if event.key == pygame.K_SPACE:
        P1.cancel_jump()


  if P1.rect.top > HEIGHT:
    P1.kill()
    for plat in platforms:
      plat.kill()
    P1.score = "Game over"
    gameOver = True
    displaySurface.fill(COLORS['blue'])
    pygame.display.update()
    time.sleep(0.1)
    displaySurface.fill(COLORS['red'])
    pygame.display.update()
    time.sleep(0.1)
    displaySurface.fill(COLORS['blue'])
    pygame.display.update()
    time.sleep(0.1)
    displaySurface.fill(COLORS['red'])
    pygame.display.update()
    time.sleep(0.1)
    displaySurface.fill(COLORS['blue'])
    pygame.display.update()
    g = f.render(str(P1.score),True,COLORS['white'])
    gRect = g.get_rect()
    text_width = gRect.width
    text_height = gRect.height
    displaySurface.blit(g,(WIDTH/2-(text_width/2),HEIGHT/2 - (text_height/2)))
    pygame.display.update()
    time.sleep(1)
    bumpDist = BUMPDIST_START
  else:
    displaySurface.fill(COLORS['black'])

  for entity in all_sprites:
    displaySurface.blit(entity.surf,entity.rect) 
    entity.move()
    entity.update()

  g = f.render(str(P1.score),True,COLORS['white']) 
  displaySurface.blit(g,(WIDTH/2,10))
  g = f.render(str(pickup_safe),True,COLORS['cyan'])
  displaySurface.blit(g,((WIDTH/2)-40,10))
  g = f.render(str(pickup_place),True,COLORS['orange'])
  displaySurface.blit(g,((WIDTH/2)-70,10))
  
  if P1.rect.top <= HEIGHT / 3:
    P1.pos.y += abs(P1.vel.y)
    for plat in platforms:
      if not plat.safe:
        plat.rect.y += abs(P1.vel.y)
        if plat.rect.top >= HEIGHT:
          if plat.place:
            PLACED_COUNT -= 1
          plat.kill()
    for pick in pickups:
      pick.rect.y += abs(P1.vel.y)
      if pick.rect.top >= HEIGHT:
        pick.kill()

    plat_gen()

  for plt in platforms:
    if plt.point:
      if plt.bounce or plt.ice:
        t = f1.render(str(plt.rank),True,COLORS['black'])
      else:
        t = f1.render(str(plt.rank),True,COLORS['white'])
      displaySurface.blit(t,(plt.rect.center[0],plt.rect.center[1]-6))
  # it's get_rect with a 'c' not get_rekt or cet_rekt

  for bumper in all_bumpers:
    displaySurface.blit(bumper.surf,bumper.rect) 
    bumper.move()
    bumper.update(P1.score)
    bumpDist = bumper.bumpDist

  #todo: add code to update bumpDist according to score
  #if type(P1.score) == int and bumpDist > 0:
  #  bumpDist = BUMPDIST_START - P1.score // 3

  pygame.draw.line(displaySurface,COLORS['white'],(bumpDist,0),(bumpDist,HEIGHT),2)
  pygame.draw.line(displaySurface,COLORS['white'],(WIDTH-bumpDist,0),(WIDTH-bumpDist,HEIGHT),2)

  pygame.display.update()
  FramePerSec.tick(FPS)