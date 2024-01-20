import pygame
import math

class Dot:
    
    def __init__(self, drawnDot, xPos: int, yPos: int) -> None:
        self.drawnDot = drawnDot
        self.xPos = xPos
        self.yPos = yPos

class Line:

    def __init__(self, startPos: tuple, endPos: tuple, angle: int, pivotPoint: Dot, clockwise: bool, ignoreDot) -> None:
        self.startPos = startPos
        self.endPos = endPos
        self.angle = angle
        self.pivotPoint = pivotPoint
        self.clockwise = clockwise

    def rotate(self) -> None:
        if self.clockwise:
            self.startPos = (10000 * math.cos(self.angle) + (screenWidth / 2), 10000 * math.sin(self.angle) + (screenHeight / 2))
            self.angle += 0.001
        else:
            self.startPos = (10000 * math.cos(self.angle) + (screenWidth / 2), 10000 * math.sin(self.angle) + (screenHeight / 2))
            self.angle -= 0.001
    
    def detectDotCollide(self) -> Dot:
        for dot in dotArray:
            x = dot.drawnDot.clipline(self.startPos, self.endPos)
            if x != () and dot != self.pivotPoint:
                return dot
    
    def changePivot(self, dot) -> None:
        for line in lineArray:
            line.pivotPoint = dot
            line.endPos = (dot.xPos, dot.yPos)
            
screenWidth, screenHeight = 1000, 800
dotArray, lineArray = [], []

screen = pygame.display.set_mode((screenWidth, screenHeight), vsync=1)
pygame.display.set_caption("Windmill Dots")

# Initial lines
lineArray.append(Line((0, 0), (screenWidth/2, screenHeight/2), 0, None, True, None))
lineArray.append(Line((screenWidth, screenHeight), (screenWidth/2, screenHeight/2), math.pi, None, True, None))

# test dots
"""
for i in range(round(screenWidth / 20)):
    for n in range(round(screenHeight / 20)):
        dot = pygame.draw.circle(screen, (255, 255, 255), (i*20, n*20), 5)
        dotArray.append(Dot(dot, i*20, n*20))
"""

run = True
counter = 0
while run:

    screen.fill(0)

    for dot in dotArray:
        pygame.draw.circle(screen, (255, 255, 255), (dot.xPos, dot.yPos), 5)

    for line in lineArray:
        pygame.draw.line(screen, (255, 0, 0), line.startPos, line.endPos, width=2)
        line.rotate()
        dot = line.detectDotCollide()
        if dot:
            line.changePivot(dot)
            line.ignoreDot = dot
            counter = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            removed = False
            for i in dotArray:
                #Check if a dot is in the location clicked
                if x - 5 <= i.xPos <= x + 5 and y - 5 <= i.yPos <= y + 5:
                    dotArray.remove(i)
                    removed = True
            if not removed:
                dot = pygame.draw.circle(screen, (255, 255, 255), (x, y), 5)
                dotArray.append(Dot(dot, x, y))

    pygame.display.update()

pygame.quit()