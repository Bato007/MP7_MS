import pygame
import math
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

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

  def getPos(self):
    return self.x, self.y

class Ball(object):
  def __init__(self, x, y, matrix, screen):
    self.x = x 
    self.y = y
    self.matrix = matrix
    self.screen = screen

  def paintGreen(self):
    self.screen.set_at((self.x, self.y), GREEN)
    self.matrix[self.x][self.y] = EMPTY
  
  def updateBall(self):
    self.screen.set_at((self.x, self.y), RED)
    self.matrix[self.x][self.y] = RED

  def move(self, x, y):
    self.x = x
    self.y = y
    self.paintGreen()
    self.updateBall()

  def getPos(self):
    return self.x, self.y


def createHorizontalLine(xo, xf, y):
  for x in range(xo, xf):
    game[x][y] = GOAL

def createVerticalLine(yo, yf, x):
  for y in range(yo, yf):
    game[x][y] = GOAL


"""
FUZZY LOGIC SETUP
"""

# Ball Finding
## Inputs
### Distance from player to ball, min is at ball, max is hypotenuse
ball_distance = ctrl.Antecedent(np.arange(0, 142, 1), 'ball_dist')
### Position of ball relative, behind is -100, forward is 100
rel_position = ctrl.Antecedent(np.arange(-100, 100, 1), 'ball_pos')
## Output
output_speed = ctrl.Consequent(np.arange(5, 20, 5), 'output_speed')

# Kick Strength
## Inputs
### The speed the player is approaching the ball
player_speed = ctrl.Antecedent(np.arange(5, 20, 5), 'speed')
### Distance from ball to goal
goal_distance = ctrl.Antecedent(np.arange(0, 142, 1), 'goal_dist')
## Output
output_strength = ctrl.Consequent(np.arange(2, 20, 6), 'output_strength')


# Membership functions
ball_distance['near'] = fuzz.trimf(ball_distance.universe, [0, 0, 103])
ball_distance['far'] = fuzz.trimf(ball_distance.universe, [39, 142, 142])
# ball_distance.view()

rel_position.automf(3)
# rel_position.view()

output_speed.automf(3)
# output_speed.view()

player_speed.automf(3)
# player_speed.view()

goal_distance['near'] = fuzz.trimf(goal_distance.universe, [0, 0, 103])
goal_distance['far'] = fuzz.trimf(goal_distance.universe, [39, 142, 142])
# goal_distance.view()

output_strength.automf(3)
# output_strength.view()


# Rules
## Set 1
set1_rule1 = ctrl.Rule((rel_position['good'] & ball_distance['near']) | (rel_position['average'] & ball_distance['far']), output_speed['poor'])
set1_rule2 = ctrl.Rule((rel_position['average'] & ball_distance['near']) | (rel_position['good'] & ball_distance['far']), output_speed['average'])
set1_rule3 = ctrl.Rule((ball_distance['far'] | ball_distance['near']) & rel_position['poor'], output_speed['average'])

## Set 2
set2_rule1 = ctrl.Rule((player_speed['good'] & goal_distance['far']) | (player_speed['average'] & goal_distance['near']), output_strength['poor'])
set2_rule2 = ctrl.Rule((player_speed['average'] & goal_distance['near']), output_strength['average'])
set2_rule3 = ctrl.Rule((player_speed['average'] & goal_distance['far']) | (player_speed['good'] & goal_distance['near']), output_strength['average'])

# Controles
speed_ctrl = ctrl.ControlSystem([set1_rule1, set1_rule2, set1_rule3])
strength_ctrl = ctrl.ControlSystem([set2_rule1, set2_rule2, set2_rule3])

#Simulators
speed = ctrl.ControlSystemSimulation(speed_ctrl)
strength = ctrl.ControlSystemSimulation(strength_ctrl)

# wait = input('press')


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

move_speed = 0
move_strength = 0

run = True
while run:
  for event in pygame.event.get():
      if event.type == pygame.QUIT:
          run = False

  ballx, bally = ball.getPos()
  playx, playy = player.getPos()

  distance = math.sqrt(abs(ballx - playx)**2 + abs(bally - playy)**2)
  if distance < 2:
    strength.input['speed'] = move_speed
    strength.input['goal_dist'] = math.sqrt(abs(ballx - 99)**2 + abs(bally - 50)**2)
    strength.compute()
    move_strength = strength.output['output_strength']
    move_amount = math.sqrt(move_strength**2 / 2)
    if ballx > 50:
      ball.move(ballx + move_amount, bally + move_amount)
    else:
      ball.move(ballx + move_amount, bally - move_amount)
  else:
    speed.input['ball_dist'] = distance
    speed.input['ball_pos'] = ballx - playx
    speed.compute()
    move_speed = speed.output['output_speed']
    move_amount = math.sqrt(move_speed**2 / 2)
    if ballx < playx:
      player.moveLeft(int(move_amount))
    elif ballx > playx:
      player.moveLeft(int(move_amount))
    if bally < playy:
      player.moveUp(int(move_amount))
    elif bally > playy:
      player.moveDown(int(move_amount))
  #player.moveRight(5)
  # ball.move(20, 20)
  pygame.time.delay(10)
  pygame.display.update()
  win.blit(pygame.transform.scale(screen, win.get_rect().size), (0, 0))

pygame.quit()