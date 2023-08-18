import pygame
from pygame import mixer
from pygame.locals import *
import sys
import generator
from generator import Labyrinth
import numpy

pygame.init()

# constants
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 900
bg_color = pygame.Color(255, 255, 255)
player_color = pygame.Color(0, 0, 255)
wall_color = pygame.Color(0, 0, 0)
money_dark_color = pygame.Color(0, 127, 0)
money_light_color = pygame.Color(100, 255, 100)

pygame.time.Clock().tick(60)
canvas = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

def lobsterCall():
    lobster = pygame.image.load("./media/lobster.png")
    canvas.blit(lobster, lobster.get_rect())
    mixer.music.play()

TILE_SIZE = 100
WALL_THICKNESS = int(TILE_SIZE/15)
LB_W = int(WINDOW_WIDTH/TILE_SIZE)
LB_H = int(WINDOW_HEIGHT/TILE_SIZE)
lb = Labyrinth((LB_W, LB_H))
    
def drawTile(p, show_player=False):
    i, j = p
    thickness = int(WALL_THICKNESS*2) if show_player else WALL_THICKNESS
    walls = []
    if show_player:
        pygame.draw.circle(canvas, player_color, generator.tuple_add((i*TILE_SIZE, j*TILE_SIZE), (int(TILE_SIZE/2), int(TILE_SIZE/2))), int(TILE_SIZE/5))
    if (lb.isWallDir(p, 'right')):
        _x = (i)*TILE_SIZE
        _y = (j)*TILE_SIZE-thickness*(1-show_player)
        _w = thickness
        _h = TILE_SIZE+thickness*2*(1-show_player)
        walls.append(pygame.Rect((_x, _y), (_w, _h)))
    if (lb.isWallDir(p, 'down')):
        _x = i*TILE_SIZE-thickness*(1-show_player)
        _y = (j+1)*TILE_SIZE-thickness
        _w = TILE_SIZE+thickness*2*(1-show_player)
        _h = thickness
        walls.append(pygame.Rect((_x, _y), (_w, _h)))
    if (lb.isWallDir(p, 'left')):
        _x = (i+1)*TILE_SIZE-thickness
        _y = (j)*TILE_SIZE-thickness*(1-show_player)
        _w = thickness
        _h = TILE_SIZE+thickness*2*(1-show_player)
        walls.append(pygame.Rect((_x, _y), (_w, _h)))
    if (lb.isWallDir(p, 'up')):
        _x = i*TILE_SIZE-thickness*(1-show_player)
        _y = (j)*TILE_SIZE
        _w = TILE_SIZE+thickness*2*(1-show_player)
        _h = thickness
        walls.append(pygame.Rect((_x, _y), (_w, _h)))
    for w in walls:
        pygame.draw.rect(canvas, wall_color, w)

def drawLabyrinth():
    for i in range(LB_W):
        for j in range(LB_H):
            drawTile((i,j), False)

mixer.init()
mixer.music.load("./media/toccata_cut.mp3")
pygame.display.set_caption("Labyrinth")

# 0 - preview, 1 - game, 2 - lobster
state = 0

while True:
    pygame.display.update()
            
    if state == 0:
        player_pos = (0, 0)
        canvas.fill(bg_color)
        lb = Labyrinth((LB_W, LB_H))
        lb.generate((0, 0))
        drawLabyrinth()
        pygame.display.update()
        pygame.time.wait(2000)
        state = 1
        continue

    if state == 1: 
        canvas.fill(bg_color)
        drawTile(player_pos, True)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if state == 1 and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                new_pos = generator.tuple_add(player_pos, (-1, 0))
                if lb.isWallDir(player_pos, 'right'):
                    state = 2
                else:
                    player_pos = new_pos
                
            if event.key == pygame.K_RIGHT:
                new_pos = generator.tuple_add(player_pos, (1, 0))
                if lb.isWallDir(player_pos, 'left'):
                    state = 2
                else:
                    player_pos = new_pos

            if event.key == pygame.K_UP:
                new_pos = generator.tuple_add(player_pos, (0, -1))
                if lb.isWallDir(player_pos, 'up'):
                    state = 2
                else:
                    player_pos = new_pos

            if event.key == pygame.K_DOWN:
                new_pos = generator.tuple_add(player_pos, (0, 1))
                if lb.isWallDir(player_pos, 'down'):
                    state = 2
                else:
                    player_pos = new_pos

            continue
        
    if state == 3 and not mixer.music.get_busy():
        state = 0
        continue
        pygame.quit()
        sys.exit()
    if state == 2:
        lobsterCall()
        state = 3


