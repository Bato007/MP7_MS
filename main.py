import pygame

pixel_scale = 5
screen_pixels = 100
width, height = screen_pixels*pixel_scale, screen_pixels*pixel_scale

PLAYER = 0
BALL = 1
GOAL = 3
EMPTY = 999
GOAL = 9999

WHITE = (255, 255, 255)
GREEN = (35, 192, 56)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
class Player(object):
  def __init__(self, x, y, matrix, screen):
    self.x = x 
    self.y = y
    self.matrix = matrix
    self.screen = screen
  
  def paintGreen(self):
    self.screen.set_at((self.x, self.y), GREEN)
    self.matrix[self.x][self.y] = EMPTY
  
  def updatePlayer(self):
    self.screen.set_at((self.x, self.y), BLACK)
    self.matrix[self.x][self.y] = BLACK

  def moveUp(self, scale = 1):
    self.paintGreen()
    self.y -= scale
    self.updatePlayer()
    pass
  
  def moveDown(self, scale = 1):
    self.paintGreen()
    self.y += scale
    self.updatePlayer()
  
    pass
  
  def moveRight(self, scale = 1):
    self.paintGreen()
    self.x += scale
    self.updatePlayer()

    pass
  
  def moveLeft(self, scale = 1):
    self.paintGreen()
    self.x -= scale
    self.updatePlayer()

    pass

class Ball(object):
  def __init__(self, x, y, matrix, screen):
    self.x = x 
    self.y = y
    self.matrix = matrix
    self.screen = screen

  def moveUp(self, scale = 1):
    pass
  
  def moveDown(self, scale = 1):
    pass
  
  def moveRight(self, scale = 1):
    pass
  
  def moveLeft(self, scale = 1):
    pass


def createHorizontalLine(xo, xf, y):
  for x in range(xo, xf):
    game[x][y] = GOAL

def createVerticalLine(yo, yf, x):
  for y in range(yo, yf):
    game[x][y] = GOAL

game = []
def createInitialGame():
  for i in range(screen_pixels):
    new = []
    for j in range(screen_pixels):
      new.append(EMPTY)
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
    if game[x][y] == EMPTY:
      screen.set_at((x, y), GREEN)
    elif game[x][y] == GOAL:
      screen.set_at((x, y), WHITE)
    elif game[x][y] == PLAYER:
      player = Player(
        x,
        y,
        game,
        screen
      )
      screen.set_at((x, y), BLACK)
    elif game[x][y] == BALL:
      ball = Ball(
        x,
        y,
        game,
        screen
      )
      screen.set_at((x, y), RED)

win.blit(pygame.transform.scale(screen, win.get_rect().size), (0, 0))

run = True
while run:
  for event in pygame.event.get():
      if event.type == pygame.QUIT:
          run = False
  player.moveRight(5)
  pygame.time.delay(10)
  pygame.display.update()
  win.blit(pygame.transform.scale(screen, win.get_rect().size), (0, 0))

pygame.quit()