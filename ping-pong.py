from pygame import *
import math as m
from random import random

w, h = 700, 500
window = display.set_mode((w, h)) 
sprites = []
movable = []
plrs = []
clock = time.Clock()
game = True
finish = False

class GameSprite(sprite.Sprite):
    def __init__(s, x, y, sx, sy, img, vel = [0, 0], addToSprites = True):
        super().__init__()
        s.x = w*x
        s.y = h*y
        s.sx = int(w*sx)
        s.sy = int(h*sy)
        s.img = transform.scale(image.load(img), (s.sx, s.sy))
        s.rect = s.img.get_rect()
        s.vel = vel
        if addToSprites:
            sprites.append(s)
    def draw(s):
        window.blit(s.img, (s.x, s.y))
    def cx(s):
        return s.x - s.sx/2
    def cy(s):
        return s.y + s.sy/2

typp_keys = [[K_LEFT, K_RIGHT, K_UP, K_DOWN], [K_a, K_d, K_w, K_s]]

class Player(GameSprite):
    def __init__(s, x, y, typp):
        super().__init__(x, y, 0.05, 0.21, "player.png")
        s.velLimited = True
        s.type = typp
        movable.append(s)
        plrs.append(s)

    def move(s, k):
        vel = [0, 0]
        K = typp_keys[s.type]
        if k[K[0]] or k[K[2]]:
            vel[1] -= 1
        if k[K[1]] or k[K[3]]:
            vel[1] -= -1
        if vel[0] == 0 and vel[1] == 0:
            return
        else:
            n = m.sqrt(vel[0]**2 + vel[1]**2)
            s.vel = (s.vel[0] + vel[0]/n*0.4, s.vel[1] + vel[1]/n*0.4)
    
    def checkCollision(s, wall):
        if (s.x+s.sx > wall.x and s.x < wall.x+wall.sx) and (s.y+s.sy > wall.y and s.y < wall.y+wall.sy):
            return True
        else:
            return False
    
class Ball(GameSprite):
    def __init__(s, x, y):
        super().__init__(x, y, 0.05, 0.07, "ball.png")
        s.velLimited = False
        s.vel = [5, 0]
        movable.append(s)

bg = GameSprite(0, 0, 1, 1, "background.png")
Player(0.075, 0.395, 1)
Player(0.875, 0.395, 0)
ball = Ball(0.475, 0.465)

font.init()
font = font.SysFont("Arial", 32)
winT1 = font.render('Выиграл правый игрок', True, (255, 215, 0))
winT2 = font.render('Выиграл левый игрок', True, (255, 215, 0))

def ending():
    display.update()
    clock.tick(1/3)

t = 0
while game:
    clock.tick(60)

    for e in event.get():
        if e.type == QUIT:
            game = False

    for plr in plrs:
        plr.move(key.get_pressed())
        if plr.checkCollision(ball):
            d = [ball.cx() - plr.cx(), ball.cy() - plr.cy()]
            du = m.sqrt(d[0]**2 + d[1]**2)
            d[0] /= du
            d[1] /= du
            ball.vel[0] = d[0]*5
            ball.vel[1] = d[1]*5

    for obj in (movable):
        obj.y = max(min(obj.y + obj.vel[1], h - obj.sy), 0)
        if obj.velLimited:
            obj.x = max(min(obj.x + obj.vel[0], w), 0)
            obj.vel = [obj.vel[0]*0.95, obj.vel[1]*0.95]
            if obj.x == max(min(obj.x + obj.vel[0], w), 0):
                obj.vel[0] = 0
            if obj.y == max(min(obj.y + obj.vel[1], h - obj.sy), 0):
                obj.vel[1] = 0
        else:
            obj.x += obj.vel[0]
            if obj.y == max(min(obj.y + obj.vel[1], h - obj.sy), 0):
                obj.vel[1] *= -1

    if ball.x > w:
        window.blit(winT1, (w/2-64, h/2-32))
        game = False
        ending()
    if ball.x < 0:
        window.blit(winT2, (w/2-64, h/2-32))
        game = False
        ending()

    for sprite in (sprites):
        sprite.draw()

    display.update()