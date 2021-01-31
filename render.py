from maze import *
import pygame, numpy, copy
size = 600

def grid(window, maze):
    dim = len(maze)
    spaceDim = size // dim
    x = 0
    y = 0
    pathColor = (30,30,30)
    for row in maze:
        for space in row:
            newSpace = pygame.Rect(x, y, spaceDim, spaceDim)
            if space == 0:
                pygame.draw.rect(window, (0,0,0), newSpace, width=0)
                pygame.draw.rect(window, (0,0,0), newSpace, width=1)
            elif space == 1:
                pygame.draw.rect(window, (255,255,255), newSpace, width=0)
                pygame.draw.rect(window, (0,0,0), newSpace, width=1)
            elif space == 2:
                pygame.draw.rect(window, (255,0,0), newSpace, width=0)
                pygame.draw.rect(window, (0,0,0), newSpace, width=1)
            elif space == 3:
                pygame.draw.rect(window, pathColor, newSpace, width=0)
                pygame.draw.rect(window, (0,0,0), newSpace, width=1)
                numMoves -= 1
            elif space == -1:
                pygame.draw.rect(window, (0,255,255), newSpace, width=0)
                pygame.draw.rect(window, (0,0,0), newSpace, width=1)
            x += spaceDim
        y += spaceDim
        x = 0
    goalSpace = pygame.Rect(dim - 1 ,dim - 1, spaceDim, spaceDim)
    pygame.draw.rect(window, (255,255,0), newSpace, width=0)
    pygame.draw.rect(window, (0,0,0), newSpace, width=1)

def path(maze, prev):
    returnMaze = copy.deepcopy(maze)
    dim = len(maze)
    spaceDim = size // dim
    # prev is None when a search algorithm has failed to find a path
    if prev is None:
        #print("No solution")
        return maze
    # Loop and count the number of moves in the path found by the search algorithm
    numMoves = 0
    currentSpace = (dim - 1, dim - 1)
    while currentSpace != (0,0):
        currentSpace = prev[currentSpace]
        returnMaze[currentSpace[0]][currentSpace[1]] = 3
        numMoves += 1
    return returnMaze

def draw(window, maze):
    window.fill((255,255,255))
    grid(window, maze)
    pygame.display.update()

def movementTwo(window, maze):
    agentLocation = (0,0)
    spacesTraveled = [agentLocation]
    atGoal = False
    while not atGoal:
        dim = len(maze)
        spaceDim = size // dim
        prev = DFS(maze, agentLocation, spacesTraveled)
        if prev is None:
            return True
        currentSpace = (dim - 1, dim - 1)
        while prev[currentSpace] != agentLocation:
                currentSpace = prev[currentSpace]

        prevSpace = pygame.Rect(prev[currentSpace][1]*spaceDim, prev[currentSpace][0]*spaceDim, spaceDim, spaceDim)
        pygame.draw.rect(window, (100, 100, 100), prevSpace, width=0)
        pygame.draw.rect(window, (0,0,0), prevSpace, width=1)
        pygame.display.update()
        time.sleep(0.2)
        newCurrent = pygame.Rect(currentSpace[1]*spaceDim, currentSpace[0]*spaceDim, spaceDim,  spaceDim)
        pygame.draw.rect(window, (0,255,255), newCurrent, width=0)
        pygame.draw.rect(window, (0,0,0), newCurrent, width=1)
        pygame.display.update()

        spacesTraveled.append(currentSpace)
        agentLocation = currentSpace
        if agentLocation == (dim - 1, dim - 1):
            return True


def render():
    maze = buildMaze(30, 0.25, 0.1)
    maze[0][0] = -1

    dim = len(maze)

    window = pygame.display.set_mode((size,size))
    show = True
    draw(window, maze)
    pygame.display.update()
    #origin = pygame.Rect(0, 0, size // dim, size // dim)
    #pygame.draw.rect(window, (0,255,255), origin, width=0)
    #pygame.draw.rect(window, (0,0,0), origin, width=1)
    attemptedPath = False
    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                show = False
            if not attemptedPath:
                attemptedPath = movementTwo(window, maze)


if __name__ == '__main__':
    render()
