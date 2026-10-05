import pygame, random 

class Foreground:
    OVERLAP_X = 1

    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT):
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT

        self.platforms = pygame.sprite.Group()
        self.treeImages = []
        self.bTreeImages = []
        self.grayWallImages = []
        self.tanWallImages = []
        self.closeTreeImages = []
        self.bTrees = []
        self.trees = []
        self.closeTrees = []
        self.grayWalls = []
        self.tanWalls = []
        self.wallPlacementX = [1375, 2200, 2900, 4725, 5500]
        self.wallColors = []

        self.layerSpeeds = [.7, .35, .30, .37]

        for i in range(0, 3): 
            img = pygame.image.load(f"Images/blueTree{i}.png").convert_alpha()
            self.bTreeImages.append(img)
        self.adjustTrees("blue")
        for i in range(0, 3): 
            img = pygame.image.load(f"Images/tree{i}.png").convert_alpha()
            self.treeImages.append(img)
        self.adjustTrees("not close")
        
        for i in range(0, 4):
            img = pygame.image.load(f"Images/graywall{i}.png").convert_alpha()
            self.grayWallImages.append(img)

        for i in range(0, 8):
            img = pygame.image.load(f"Images/tanwall{i}.png").convert_alpha()
            self.tanWallImages.append(img)
        
        for i in range(0, 2):
            img = pygame.image.load(f"Images/closeground tree {i}.png").convert_alpha()
            self.closeTreeImages.append(img)
        self.adjustTrees("close")

    def drawForeGroundTrees(self, scroll, screen):
        self.moveTrees(2, scroll, screen, "blue")
        self.moveTrees(1, scroll, screen, "not close")

    def drawForeGroundWalls(self, scroll, screen):
        self.moveWalls(3, scroll, screen, "gray")
        self.moveWalls(3, scroll, screen, "tan")

    def drawCloseGround(self, scroll, screen):
        self.moveTrees(0, scroll, screen, "close")

    def drawTrees(self, treeImages, GAMESCREENX, placement):
        x = -500  # start a bit off-screen to the left
        while x < GAMESCREENX:
            img = random.choice(treeImages)
            if placement == "close":
                self.closeTrees.append((x,img))
                spacing = random.randint(7,10)
            elif placement == "blue":
                self.bTrees.append((x, img))
                spacing = random.randint(2, 4)
            else:
                self.trees.append((x, img))
                spacing = random.randint(4, 7)

            spacing *= 100
            x += spacing

    def moveTrees(self, speedPos, scroll, screen, placement):
        speed = self.layerSpeeds[speedPos]
        if placement == "close":
            treeStorage = self.closeTrees
        elif placement == "blue":
            treeStorage = self.bTrees
        else:
            treeStorage = self.trees
        for (x, img) in treeStorage:
            drawX = x - scroll * speed
            if -img.get_width() < drawX < self.SCREEN_WIDTH:
                screen.blit(img, (drawX, self.SCREEN_HEIGHT - img.get_height() + 20))

    def drawWalls(self, numWalls):
        wallsDrawn = 0
        columns = 2
        rows = 3
        while (wallsDrawn < numWalls):
            self.tanWalls.append([])
            self.grayWalls.append([])
            wallchoice = random.random()
            if (wallchoice < .99):
                wallImages = self.tanWallImages
                wallWidth = wallImages[0].get_width()
                wallHeight = wallImages[0].get_height()
                for col in range(columns):
                    for row in range(rows):
                        x = self.wallPlacementX[wallsDrawn] + (col * (wallHeight - 10))
                        y = self.SCREEN_HEIGHT - (2 * wallHeight) - 55 + (row * (wallHeight - 10))
                        wall = wallImages[random.randint(0, 1)]
                        self.tanWalls[wallsDrawn].append((x, y, wall))

                wallchoice = random.random()
                if (wallchoice < .01):
                    flipped = pygame.transform.flip(wallImages[2], True, False)
                    toFlip = random.random()
                    if toFlip < .50:
                        self.tanWalls[wallsDrawn].append((self.wallPlacementX[wallsDrawn] + 10, 225, wallImages[2]))
                    else:
                        self.tanWalls[wallsDrawn].append((self.wallPlacementX[wallsDrawn] + 10, 225, flipped))
                else:
                    flip3 = pygame.transform.flip(wallImages[3], True, False)
                    flip2 = pygame.transform.flip(wallImages[4], True, False)
                    flip1 = pygame.transform.flip(wallImages[5], True, False)
                    toFlip = random.random()
                    if toFlip < .50:
                        self.tanWalls[wallsDrawn].append((self.wallPlacementX[wallsDrawn], 236, wallImages[3]))
                        self.tanWalls[wallsDrawn].append((self.wallPlacementX[wallsDrawn] + 60, 255, wallImages[4]))
                        self.tanWalls[wallsDrawn].append((self.wallPlacementX[wallsDrawn] + 115, 236, wallImages[5]))
                    else:
                        self.tanWalls[wallsDrawn].append((self.wallPlacementX[wallsDrawn], 236, flip1))
                        self.tanWalls[wallsDrawn].append((self.wallPlacementX[wallsDrawn] + 60, 255, flip2))
                        self.tanWalls[wallsDrawn].append((self.wallPlacementX[wallsDrawn] + 115, 236, flip3))

                self.tanWalls[wallsDrawn].append((self.wallPlacementX[wallsDrawn] - 10, 255, wallImages[6]))
                self.tanWalls[wallsDrawn].append((self.wallPlacementX[wallsDrawn] - 10, 310, wallImages[6]))
                self.tanWalls[wallsDrawn].append((self.wallPlacementX[wallsDrawn] - 10, 350, wallImages[6])) 

                self.tanWalls[wallsDrawn].append((x + wallImages[0].get_width() - 10, 255, wallImages[7]))
                self.tanWalls[wallsDrawn].append((x + wallImages[0].get_width() - 10, 310, wallImages[7]))
                self.tanWalls[wallsDrawn].append((x + wallImages[0].get_width() - 10, 350, wallImages[7]))
                self.tanWalls[wallsDrawn].append((x + wallImages[0].get_width() - 10, 370, wallImages[7]))
                self.tanWalls[wallsDrawn].append((x + wallImages[0].get_width() - 10, 400, wallImages[7]))
                self.tanWalls[wallsDrawn].append((x + wallImages[0].get_width() - 10, 420, wallImages[7]))
                self.wallColors.append(0)

            else:
                wallImages = self.grayWallImages
                wallWidth = wallImages[0].get_width()
                wallHeight = wallImages[0].get_height()
                for col in range(columns):
                    for row in range(rows):
                        x = self.wallPlacementX[wallsDrawn] + (col * (wallHeight - 10))
                        y = self.SCREEN_HEIGHT - (2 * wallHeight) - 55 + (row * (wallHeight - 10))
                        self.grayWalls[wallsDrawn].append((x, y, wallImages[0]))
                
                flipped = pygame.transform.flip(wallImages[1], True, False)
                toFlip = random.randint(0, 2)
                if toFlip == 0:
                    self.grayWalls[wallsDrawn].append((self.wallPlacementX[wallsDrawn] + 2, 200, wallImages[1])) 
                else:
                    self.grayWalls[wallsDrawn].append((self.wallPlacementX[wallsDrawn] + 2, 200, flipped))

                flipped = pygame.transform.flip(wallImages[3], False, True)
                for i in range(0, 2):
                    y1 = self.SCREEN_HEIGHT - (2 * wallImages[0].get_height()) - 50
                    y2 = self.SCREEN_HEIGHT - (2 * wallImages[0].get_height()) - 55
                    img = wallImages[3]
                    if (i == 1):
                        y1 += (wallImages[2].get_height() - 15)
                        y2 += (wallImages[3].get_height() - 15)
                        img = flipped
                    self.grayWalls[wallsDrawn].append((self.wallPlacementX[wallsDrawn] - 10, y1, wallImages[2]))
                    self.grayWalls[wallsDrawn].append((x + wallImages[0].get_width() - 10, y2, img))

                self.wallColors.append(1)

            wallsDrawn += 1

    def moveWalls(self, speedPos, scroll, screen, placement):
        speed = self.layerSpeeds[speedPos]
        if placement == "gray":
            wallStorage = self.grayWalls
        elif placement == "tan":
            wallStorage = self.tanWalls
        for wall in wallStorage:
            for (x, y, img) in wall:
                drawX = x - scroll
                if -img.get_width() < drawX < self.SCREEN_WIDTH:
                    screen.blit(img, (drawX, y))

    def adjustTrees(self, fgLayer):
        if fgLayer == "close":
            area = range(0, 2)
            fgImages = self.closeTreeImages
        else:
            area = range(0, 3)
            if fgLayer == "blue":
                fgImages = self.bTreeImages
            else:
                fgImages = self.treeImages

        for i in area:
            fgHeight = fgImages[i].get_height()
            fgWidth = fgImages[i].get_width()
            heightScale = (self.SCREEN_HEIGHT + 30) / fgHeight
            newWidth  = int(fgWidth * heightScale)
            newHeight = int(fgHeight * heightScale)
            fgImages[i] = pygame.transform.scale(fgImages[i], (newWidth, newHeight))

        if fgLayer == "close":
            self.closeTreeImages = fgImages
        elif fgLayer == "blue":
            fgImages = self.bTreeImages
        else:
            fgImages = self.treeImages
            