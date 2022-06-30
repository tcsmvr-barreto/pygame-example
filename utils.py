from config import *

class Spritesheet:
  def __init__(self, filename):
    try:
      self.sheet = pygame.image.load(filename)
    except pygame.error as e:
      print(f"Unable to load spritesheet image: {filename}")
      raise SystemExit(e)

  def image_at(self, rectangle, colorkey = None):
    rect = pygame.Rect(rectangle)
    image = pygame.Surface(rect.size)
    image.blit(self.sheet, (0,0), rect)
    if colorkey is not None:
      if colorkey == -1:
        colorkey = image.get_at((0,0))
      image.set_colorkey(colorkey, pygame.RLEACCEL)
    return image

  def images_at(self, rects, image_count, colorkey = None):
    return [self.image_at(rect, colorkey) for rect in rects]