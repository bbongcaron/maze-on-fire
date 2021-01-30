from maze import *
import pygame
size = 360

def grid(window, maze):
    spaceDim = size // len(maze)
    x = 0
    y = 0
    for row in maze:
        for space in row:
            spaceBorder = pygame.Rect(x,y,spaceDim, spaceDim)
            if space == 0:
                newSpace = pygame.Rect(x,y,spaceDim, spaceDim)
                pygame.draw.rect(window, (0,0,0), newSpace, width=0)
                pygame.draw.rect(window, (0,0,0), newSpace, width=1)
            elif space == 1:
                newSpace = pygame.Rect(x,y,spaceDim, spaceDim)
                pygame.draw.rect(window, (255,255,255), newSpace, width=0)
                pygame.draw.rect(window, (0,0,0), newSpace, width=1)
            elif space == 2:
                newSpace = pygame.Rect(x,y,spaceDim, spaceDim)
                pygame.draw.rect(window, (255,0,0), newSpace, width=0)
                pygame.draw.rect(window, (0,0,0), newSpace, width=1)
            x += spaceDim
        y += spaceDim
        x = 0

def redraw(window, maze):
    window.fill((255,255,255))
    grid(window, maze)
    pygame.display.update()

def render():
    maze = buildMaze(10, 0.30, 0.1)
    for row in maze:
        print(row)
    rows = len(maze)

    window = pygame.display.set_mode((size,size))

    show = True

    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        redraw(window, maze)

if __name__ == '__main__':
    render()
