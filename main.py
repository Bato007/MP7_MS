import pygame

width, height = 480, 480

PLAYER = 0
BALL = 1
GOAL = 3
GREEN = 999
WHITE = 9999

class Simulation(object):
  def __init__(self, screen, initial=None):
    self.screen = screen
    self.modx = width 
    self.mody = height

    for point in initial:
      self.paint(point[0], point[1])

  def paint(self, x, y, color=(255, 255, 255)):
    px = x*pixel_len
    py = y*pixel_len

    for i in range(px, px+pixel_len):
      for j in range(py, py+pixel_len):
        self.screen.set_at((i, j), color)

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
  for i in range(width):
    new = []
    for j in range(height):
      new.append(999)
    game.append(new)

  goalWidth = 60
  linesHeight = 80

  goalHeight = 200
  goalCenter = int(height/2 - goalHeight/2)

  createHorizontalLine(width-goalWidth, width, linesHeight)
  createHorizontalLine(width-goalWidth, width, height-linesHeight)
  createVerticalLine(linesHeight, height-linesHeight, width-goalWidth)

  createVerticalLine(goalCenter, goalCenter + goalHeight, width-2)
  createVerticalLine(goalCenter, goalCenter + goalHeight, width-1)

  playerX = 6
  gameCenter = int(height / 2)
  game[playerX][gameCenter] = PLAYER
  game[playerX + 10][gameCenter] = BALL



createInitialGame()

pygame.init()
screen = pygame.display.set_mode((width, height))

for x in range(len(game)):
  for y in range(len(game[x])):
    if game[x][y] == GREEN:
      screen.set_at((x, y), (35, 192, 56))
    elif game[x][y] == WHITE:
      screen.set_at((x, y), (255, 255, 255))
    elif game[x][y] == PLAYER:
      screen.set_at((x, y), (0, 255, 0))

pygame.display.flip()

lines = []
# # Porteria [17 - 27]

simulation = Simulation(
  screen,
  initial=lines,
)

ITERATIONS = 100
for _ in range(ITERATIONS):
  pygame.time.delay(10)
  pygame.display.flip()