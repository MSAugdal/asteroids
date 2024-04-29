import pygame, sys
from random import randint
from typing import Tuple
from pygame.key import ScancodeWrapper
from pygame.math import Vector2
from pygame.surface import Surface
from pygame.time import Clock
from pygame import Rect

pygame.init()

# Global constants
WIDTH: int = 1024
HEIGHT: int = 1024
BG_COLOR: Tuple[int,int,int] = (100,100,100)
DISPLAY: Surface = pygame.display.set_mode((HEIGHT, WIDTH))
CLOCK: Clock = pygame.time.Clock()

# counter for score and lists to hold lasers and enemies
score: int = 0
laserList: list = []
enemyList: list = []

# Player class. the methods of the class explain themselves pretty clearly
class Player:
    def __init__(self):
        self.rect: Rect = pygame.Rect(WIDTH//2, HEIGHT//2, 50, 50)
        self.speed: int = 12

    def inputHandler(self, keysPressed: ScancodeWrapper) -> None:
        if keysPressed[pygame.K_w]:
            self.rect.y -= self.speed
        if keysPressed[pygame.K_a]:
            self.rect.x -= self.speed
        if keysPressed[pygame.K_s]:
            self.rect.y += self.speed
        if keysPressed[pygame.K_d]:
            self.rect.x += self.speed
        # spawns laser when SPACE key pressed
        if keysPressed[pygame.K_SPACE]:
            if len(laserList) < 5:
                laserList.append(Laser(Vector2(self.rect.x - 25, self.rect.y)))

    def keepInBounds(self) -> None:
        if self.rect.x >= WIDTH - 100:
            self.rect.x -= 10
        if self.rect.x <= 0:
            self.rect.x += 10
        if self.rect.y >= HEIGHT - 100:
            self.rect.y -= 10
        if self.rect.y <= 0:
            self.rect.y += 10

    def draw(self):
        pygame.draw.rect(DISPLAY, "black", self.rect)

    def checkCollisionWithEnemy(self):
        for enemy in enemyList:
            if self.rect.colliderect(enemy.rect):
                print(f"You died\nYour score was: {score}")
                pygame.QUIT
                sys.exit()

class Enemy:
    def __init__(self, x):
        self.x = x
        self.y = -20
        self.rect = pygame.Rect(self.x, self.y, 40, 40)

    # Updated position of enemy (moves it down). goes faster as score goes up
    def updatePos(self):
        self.rect.y += round(10 + score*0.2) if score > 10 else 10

    def draw(self):
        pygame.draw.rect(DISPLAY, "blue", self.rect)


class Laser:
    def __init__(self, pos: Vector2):
        self.x = pos.x + 50
        self.y = pos.y
        self.rect = pygame.Rect(self.x, self.y, 8, 8)

    def updatePos(self):
        self.rect.y -= 20

    def draw(self):
        pygame.draw.rect(DISPLAY, "red", self.rect)

    # removes enemy from enemyList if collided with and increases score
    def checkCollisionWithEnemy(self, enemy: Enemy):
        global score
        if enemy.rect.colliderect(self.rect):
            enemyList.pop(enemyList.index(enemy))
            score += 1
            pygame.display.set_caption(f"score: {score}")
            return True


#initilization of player
PLAYER = Player()

while True: # game loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    DISPLAY.fill(BG_COLOR)

    PLAYER.checkCollisionWithEnemy()
    PLAYER.draw()
    PLAYER.inputHandler(pygame.key.get_pressed())
    PLAYER.keepInBounds()

    # remove laser if out of bounds. update laser pos
    for laser in laserList:
        if laser.rect.y < 0:
            laserList.pop(laserList.index(laser))
        else:
            laser.updatePos()
            laser.draw()

    # spawn enemies, update enemy pos, remove enemy if out of bounds
    if len(enemyList) < 10:
        enemyList.append(Enemy(randint(40, WIDTH - 40)))
    for enemy in enemyList:
        if enemy.rect.y > HEIGHT:
            enemyList.pop(enemyList.index(enemy))
        else:
            enemy.updatePos()
            enemy.draw()

    # check for laser collision with enemy
    for laser in laserList:
        for enemy in enemyList:
            laser.checkCollisionWithEnemy(enemy)

    CLOCK.tick(30)
    pygame.display.update()

