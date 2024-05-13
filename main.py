import pygame
from math import atan2, sin, cos, sqrt
width, height = 1000, 800
max_size = 50
from random import random
WIN = pygame.display.set_mode((width, height))

#Use LMB to grab a Ball
#Use RMB to add force to a Ball

class Ball:
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.ax = 0
        self.ay = 0
        self.r = r
        self.mass = r*r
        self. color = "white"
    def draw(self):
        pygame.draw.circle(WIN, self.color, (self.x, self.y), self.r,1)
        pygame.draw.line(WIN, self.color, (self.x, self.y), (self.x+self.vx*self.r, self.y+self.vy*self.r), 2)

def doCirclesOverlap(x1, y1, r1, x2, y2, r2):
    return abs((x1-x2)*(x1-x2)+(y1-y2)*(y1-y2)) < ((r1+r2)*(r1+r2))-0.1
def isPointInCircle(x1, y1, r1, x, y):
    return abs((x1 - x) * (x1 - x) + (y1 - y) * (y1 - y)) < (r1*r1)

def main():
    colliding_pairs = []
    selected = False
    run = True
    balls = [Ball(random()*width, random()*height, random()*80) for i in range(40)]
    for ball in balls:
        ball.draw()
    while run:
        pygame.time.Clock().tick(60)
        pygame.draw.rect(WIN, "black", (0,0,width, height))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if (event.button == 1) | (event.button == 3):
                    #print(pygame.mouse.get_pressed()[0])
                    for ball in balls:
                        if isPointInCircle(ball.x, ball.y, ball.r, event.pos[0], event.pos[1]):
                            selected = ball
                            break
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    selected = False
                if event.button == 3:
                    if selected:
                        selected.vx += (selected.x - pygame.mouse.get_pos()[0])/50
                        selected.vy += (selected.y - pygame.mouse.get_pos()[1])/50
                        selected = False
        if pygame.mouse.get_pressed()[0]:
            if selected:
                selected.x, selected.y = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[2]:
            if selected:
                pygame.draw.line(WIN, "blue", (selected.x, selected.y), pygame.mouse.get_pos())
        for ball in balls:
            for other in balls:
                if ball != other:
                    if doCirclesOverlap(ball.x, ball.y, ball.r, other.x, other.y, other.r):
                        if ([ball, other] not in colliding_pairs) & ([other, ball] not in colliding_pairs):
                            colliding_pairs.append([ball, other])
                        ball.color = "red"
                        distance = sqrt(((ball.x-other.x)*(ball.x-other.x))+((ball.y-other.y)*(ball.y-other.y)))
                        overlap = (distance-ball.r-other.r)/2


                        ball.x -= (ball.x-other.x)*overlap/distance
                        ball.y -= (ball.y-other.y)*overlap/distance
                    else:
                        ball.color = "white"
        for p in colliding_pairs:
            b1 = p[0]
            b2 = p[1]

            distance = sqrt((b1.x-b2.x)*(b1.x-b2.x)+(b1.y-b2.y)*(b1.y-b2.y))

            nx = (b1.x-b2.x)/distance
            ny = (b1.y-b2.y)/distance

            tx = -ny
            ty = nx

            dpTan1 = b1.vx*tx+b1.vy*ty
            dpTan2 = b2.vx*tx+b2.vy*ty

            dpNor1 = b1.vx*nx+b1.vy*ny
            dpNor2 = b2.vx*nx+b2.vy*ny

            m1 = (dpNor1 * (b1.mass - b2.mass) + 2 * b2.mass *dpNor2)/(b1.mass + b2.mass)
            m2 = (dpNor2 * (b2.mass - b1.mass) + 2 * b1.mass *dpNor1)/(b1.mass + b2.mass)

            b1.vx = tx*dpTan1 +nx*m1
            b1.vy = ty*dpTan1 +ny*m1
            b2.vx = tx*dpTan2 +nx*m2
            b2.vy = ty*dpTan2 +ny*m2

            colliding_pairs.remove(p)
        for ball in balls:
            ball.ax = (ball.vx * 0.01)
            ball.ay = (ball.vy * 0.01)

            ball.vx = ball.vx - ball.ax
            ball.vy = ball.vy - ball.ay

            ball.x += ball.vx
            ball.y += ball.vy

            if abs(ball.x * ball.x + ball.y * ball.y) < 0.01:
                ball.vx = 0
                ball.vy = 0
            if ball.x < 0:
                ball.x += width
            elif ball.x > width:
                ball.x -= width
            if ball.y < 0:
                ball.y += height
            elif ball.y > height:
                ball.y -= height
            ball.draw()
        pygame.display.update()



main()