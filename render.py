from maze import *
import pygame, numpy, copy
size = 360

def grid(window, maze, numMoves=1):
    dim = len(maze)
    spaceDim = size // dim
    x = 0
    y = 0
    if numMoves is not None:
        grayscale = numpy.linspace(20,240,numMoves,dtype='int')
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
                pygame.draw.rect(window, (grayscale[numMoves-1], grayscale[numMoves-1], grayscale[numMoves-1]), newSpace, width=0)
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

def path(window, maze, prev):
    returnMaze = copy.deepcopy(maze)
    dim = len(maze)
    spaceDim = size // dim
    # prev is None when a search algorithm has failed to find a path
    if prev is None:
        #print("No solution")
        return maze, None
    # Loop and count the number of moves in the path found by the search algorithm
    numMoves = 0
    currentSpace = (dim - 1, dim - 1)
    while currentSpace != (0,0):
        currentSpace = prev[currentSpace]
        returnMaze[currentSpace[0]][currentSpace[1]] = 3
        numMoves += 1
    return returnMaze, numMoves

def redraw(window, maze):
    window.fill((255,255,255))
    prev = DFS(maze)
    solvedMaze, numMoves = path(window, maze, prev)

    grid(window, solvedMaze, numMoves)

    pygame.display.update()

def render():
    maze = buildMaze(10, 0.25, 0.1)
    agentLocation = (0,0)
    maze[0][0] = -1

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
