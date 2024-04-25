import pygame, sys
from typing import Tuple
from pygame.key import ScancodeWrapper
from pygame.math import Vector2
from pygame.surface import Surface
from pygame.time import Clock

pygame.init()
WIDTH: int = 1024
HEIGHT: int = 1024
BG_COLOR: Tuple[int,int,int] = (100,100,100)
DISPLAY: Surface = pygame.display.set_mode((HEIGHT, WIDTH))
PLAYER: Surface = pygame.Surface((100,100))
PLAYER_POS: Vector2 = pygame.Vector2(DISPLAY.get_width() / 2, DISPLAY.get_height() / 2)
PLAYER_SPEED: int = 10
CLOCK: Clock = pygame.time.Clock()
laserList: list = []

def inputHandler(keysPressed: ScancodeWrapper) -> None:
    if keysPressed[pygame.K_w]:
        PLAYER_POS.y -= PLAYER_SPEED
    if keysPressed[pygame.K_a]:
        PLAYER_POS.x -= PLAYER_SPEED
    if keysPressed[pygame.K_s]:
        PLAYER_POS.y += PLAYER_SPEED
    if keysPressed[pygame.K_d]:
        PLAYER_POS.x += PLAYER_SPEED
    if keysPressed[pygame.K_SPACE]:
        laserList.append(Laser(Vector2(PLAYER_POS.x, PLAYER_POS.y)))

def keepPlayerInBounds(pPos: Vector2) -> Vector2:
    correctedPos = pPos
    posX, posY = pPos
    if posX >= WIDTH - 100:
        correctedPos.x = posX - 10
    if posX <= 0:
        correctedPos.x = posX + 10
    if posY >= HEIGHT - 100:
        correctedPos.y = posY - 10
    if posY <= 0:
        correctedPos.y = posY + 10
    return correctedPos

class Laser:
    def __init__(self, pos: Vector2):
        self.x = pos.x + 50
        self.y = pos.y
        self.LASER = pygame.Surface((10,30))

    def updatePos(self):
        self.y -= 14

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    DISPLAY.fill(BG_COLOR)
    DISPLAY.blit(PLAYER, PLAYER_POS)
    inputHandler(pygame.key.get_pressed())
    PLAYER_POS = keepPlayerInBounds(PLAYER_POS)
    for laser in laserList:
        laser.updatePos()
        DISPLAY.blit(laser.LASER, (laser.x, laser.y))
    CLOCK.tick(60)
    pygame.display.update()


