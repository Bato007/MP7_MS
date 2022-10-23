import pygame

pixel_scale = 5
screen_pixels = 100
width, height = screen_pixels*pixel_scale, screen_pixels*pixel_scale

PLAYER = 0
BALL = 1
GOAL = 3
GREEN = 999
WHITE = 9999

class Simulation(object):
  def __init__(self, screen):
    self.screen = screen
    self.modx = screen_pixels 
    self.mody = screen_pixels

  def moveUp(self, x, y, scale = 1):
    pass
  
  def moveDown(self, x, y, scale = 1):
    pass
  
  def moveRight(self, x, y, scale = 1):
    pass
  
  def moveLeft(self, x, y, scale = 1):
    pass


def createHorizontalLine(xo, xf, y):
  for x in range(xo, xf):
    game[x][y] = WHITE

def createVerticalLine(yo, yf, x):
  for y in range(yo, yf):
    game[x][y] = WHITE

game = []
def createInitialGame():
  for i in range(screen_pixels):
    new = []
    for j in range(screen_pixels):
      new.append(999)
    game.append(new)

  goalWidth = 10
  linesHeight = 20

  goalHeight = 50
  goalCenter = int(screen_pixels/2 - goalHeight/2)

  createHorizontalLine(screen_pixels-goalWidth, screen_pixels, linesHeight)
  createHorizontalLine(screen_pixels-goalWidth, screen_pixels, screen_pixels-linesHeight)
  createVerticalLine(linesHeight, screen_pixels-linesHeight, screen_pixels-goalWidth)

  createVerticalLine(goalCenter, goalCenter + goalHeight, screen_pixels-2)
  createVerticalLine(goalCenter, goalCenter + goalHeight, screen_pixels-1)

  playerX = 2
  gameCenter = int(screen_pixels / 2)
  game[playerX][gameCenter] = PLAYER
  game[playerX + 10][gameCenter] = BALL



createInitialGame()
pygame.init()

win = pygame.display.set_mode((screen_pixels*pixel_scale, screen_pixels*pixel_scale))
screen = pygame.Surface((screen_pixels, screen_pixels))


for x in range(len(game)):
  for y in range(len(game[x])):
    if game[x][y] == GREEN:
      screen.set_at((x, y), (35, 192, 56))
    elif game[x][y] == WHITE:
      screen.set_at((x, y), (255, 255, 255))
    elif game[x][y] == PLAYER:
      screen.set_at((x, y), (0, 0, 0))
    elif game[x][y] == BALL:
      screen.set_at((x, y), (255, 0, 0))

win.blit(pygame.transform.scale(screen, win.get_rect().size), (0, 0))
simulation = Simulation(
  screen
)

run = True
while run:
  for event in pygame.event.get():
      if event.type == pygame.QUIT:
          run = False

  pygame.display.update()
pygame.quit()