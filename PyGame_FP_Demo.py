import pygame
import math

WIDTH = 700
HEIGHT = 400
MAP_WIDTH = 100
MAP_HEIGHT = 100
# Going to always have a square map for demo
MAP_SIZE = 10

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BROWN = (80, 80, 80)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("FP Demo")
clock = pygame.time.Clock()

done = False

playerX = 5.0
playerY = 5.0
playerAngle = 0.0

fieldOfView = math.pi / 3.0
depthOfView = 10.0
resolution = 5

mapArr = ["##########",
"#........#",
"#...#....#",
"#...#....#",
"#...#....#",
"#...#....#",
"#........#",
"#....#####",
"#........#",
"##########"]


while not done:

    screen.fill(BLACK)
    dt = clock.tick(60)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            pygame.quit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        playerAngle -= 0.001 * dt
    elif keys[pygame.K_RIGHT]:
        playerAngle += 0.001 * dt

    if keys[pygame.K_UP]:
        playerX += math.cos(playerAngle) * 0.003 * dt
        playerY += math.sin(playerAngle) * 0.003 * dt
        if mapArr[int(playerY)][int(playerX)] == "#":
            playerX -= math.cos(playerAngle) * 0.003 * dt
            playerY -= math.sin(playerAngle) * 0.003 * dt
    elif keys[pygame.K_DOWN]:
        playerX -= math.cos(playerAngle) * 0.003 * dt
        playerY -= math.sin(playerAngle) * 0.003 * dt
        if mapArr[int(playerY)][int(playerX)] == "#":
            playerX += math.cos(playerAngle) * 0.003 * dt
            playerY += math.sin(playerAngle) * 0.003 * dt 

    print(playerX)
    print(playerY)

    for i in range(int(WIDTH/resolution)):
        rayAngle = (playerAngle-(fieldOfView/2)) + ((i/(WIDTH/5))*fieldOfView)

        # Finding distance to a wall using by
        # slowing increasing distance
        distance = 0.0
        hasHitWall = False
        hasHitEdge = False

        while not hasHitWall and distance < depthOfView:

            distance += 0.1
            tempX = int(playerX + math.cos(rayAngle) * distance)
            tempY = int(playerY + math.sin(rayAngle) * distance)

            if tempX < 0 or tempX >= MAP_SIZE or tempX < 0 or tempX >= MAP_SIZE:
                hasHitWall = True
                distance = depthOfView
            else:
                if mapArr[tempY][tempX] == "#":
                    hasHitWall = True

                    wallAngleArr = []

                    # MATH! for edge detection and "texturing"
                    for x in range(2):
                        for y in range(2):
                            vecX = tempX + x - playerX
                            vecY = tempY + y - playerY
                            vecMag = math.sqrt(vecX**2 + vecY**2)
                            try:
                                dotProd = (math.cos(rayAngle) * (vecX / vecMag)) + (math.sin(rayAngle) * (vecY/vecMag))
                            except:
                                dotProd = 0.0
                            wallAngle = math.acos(dotProd)
                            wallAngleArr.append([vecMag, wallAngle])

                    angleBound = 0.01
                    wallAngleArr = sorted(wallAngleArr, key=lambda x:x[1])
                    if wallAngleArr[0][1] < angleBound:
                        hasHitEdge = True
                    if wallAngleArr[1][0] < angleBound:
                        hasHitEdge = True



        # Ceiling and floor
        ceiling = int((HEIGHT/2 - HEIGHT/distance)/resolution)
        floor = int((HEIGHT/resolution - ceiling))

        # Changes darkness of green based on dist
        if distance <= depthOfView / 4.0:
            wallColor = GREEN
        elif distance < depthOfView / 2.0:
            wallColor = (0, 205, 0)
        elif distance < 3.0 * depthOfView / 4.0:
            wallColor = (0, 155, 0)
        elif distance < depthOfView:
            wallColor = (0, 105, 0)
        else:
            wallColor = BLACK

        if hasHitEdge:
            wallColor = BLACK

        for j in range(int(HEIGHT/resolution)):
            if j <= ceiling:
                color = BLACK
            elif j > ceiling and j < floor:
                color = wallColor
            else:
                # Changes floor darkness
                val = 1.0 - ((j - (HEIGHT/resolution)/2.0) / ((HEIGHT/resolution)/2.0))
                if val < 0.25:
                    color = WHITE
                elif val < 0.50:
                    color = (215, 215, 215)
                elif val < 0.75:
                    color = (175, 175, 175)
                elif val < 0.90:
                    color = (125, 125, 125)
                else:
                    color = BLACK

            pygame.draw.rect(screen, color, [i*resolution, j*resolution, resolution, resolution])



    # Drawing side map
    for i in range(len(mapArr)):
        for j in range(len(mapArr[i])):
            if mapArr[i][j] == "#":
                color = WHITE
            elif mapArr[i][j] == ".":
                color = BLACK
            pygame.draw.rect(screen, color, [j*(MAP_SIZE), i*(MAP_SIZE), MAP_SIZE, MAP_SIZE])
    pygame.draw.rect(screen, RED, [int(playerX)*MAP_SIZE, int(playerY)*MAP_SIZE, MAP_SIZE, MAP_SIZE])

    pygame.draw.line(screen, RED, [0, MAP_HEIGHT], [MAP_WIDTH, MAP_HEIGHT])
    pygame.draw.line(screen, RED, [MAP_WIDTH, 0], [MAP_WIDTH, MAP_HEIGHT])

    pygame.display.update()
