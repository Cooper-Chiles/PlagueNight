import pygame, walls, random

class Ground:
    OVERLAP_X = 1

    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT):
        self.GAMESCREENX = SCREEN_WIDTH * 4
        self.groundImage = pygame.image.load("Images/forestground.png").convert_alpha()
        self.groundLCapImage = pygame.image.load("Images/groundleftcap.png").convert_alpha()
        self.groundRCapImage = pygame.image.load("Images/groundrightcap.png").convert_alpha()
        self.dirt = pygame.image.load("Images/dirt.png").convert_alpha()
        self.dirtImage = pygame.transform.flip(self.dirt, False, True)
        self.rockImage = pygame.image.load("Images/tanrocks.png").convert_alpha()
        self.rockImageFlip = pygame.transform.flip(self.rockImage, True, False)
        self.groundImage = self.crop_edges(self.groundImage, left=2, right=2)
        self.groundLCapImage = self.crop_edges(self.groundLCapImage, left=2, right=2, top=2)
        self.groundRCapImage = self.crop_edges(self.groundRCapImage, left=2, right=2, top=2)
        self.grayPlatform = pygame.image.load("Images/grayplatform.png").convert_alpha()
        self.tanPlatform = pygame.image.load("Images/tanplatform.png").convert_alpha()

        self.groundGroup = pygame.sprite.Group()
        self.platformGroup = pygame.sprite.Group()
        self.dirtGroup = pygame.sprite.Group()
        self.groundEndGroup = pygame.sprite.Group()
        self.rockGroup = pygame.sprite.Group()
        self.tileWidth = self.groundImage.get_width()
        self.tilesNeeded = (self.GAMESCREENX // self.tileWidth) + 2  # +2 for overlap safety
        self.walls = walls.Wall(self.groundImage, self.groundLCapImage, self.groundRCapImage)
        self.numWalls = 0
        self.wallTopGroup = pygame.sprite.Group()
        self.holeTopGroup = pygame.sprite.Group()
        self.rockSpread = 100
        self.lastX = 0


        for i in range(self.tilesNeeded):
            x = i * (self.tileWidth - self.OVERLAP_X)

            if x - self.lastX > self.rockSpread:
                self.lastX = x
                toPrint = random.randint(0, 2)
                if toPrint == 1:
                    toFlip = random.randint(0, 2)
                    if toFlip == 0:
                        tile = RockTile(self.rockImage, x - 30, 395)
                        self.rockGroup.add(tile) 
                    else:
                        tile = RockTile(self.rockImageFlip, x - 30, 395)
                        self.rockGroup.add(tile)  
            if not i in [10, 11, 12, 22, 23, 24, 36, 37, 38]:
                if i in [9, 13, 21]:
                    if i in [9, 21]:
                        direction = "right"
                    else:
                        direction = "left"
                    self.walls.addHoleWall(x, 450, 3, self.wallTopGroup, direction)
                tile = GroundTile(self.groundImage, x, 450)
                self.groundGroup.add(tile)
                if i in [3, 4, 8, 14, 15, 18, 19, 20, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 39, 40, 46]:
                    if i in [8, 15, 35]:
                        self.walls.createWall(x, 430, 4, self.wallTopGroup)
                    elif i in [3, 18, 19, 28]:
                        self.walls.createWall(x, 430, 3, self.wallTopGroup)
                    elif i in [4, 25, 27, 31]:
                        self.walls.createWall(x, 430, 6, self.wallTopGroup)
                    elif i in [14, 34]:
                        self.walls.createWall(x, 430, 7, self.wallTopGroup)
                    elif i in [39, 33]:
                        self.walls.createWall(x, 430, 2, self.wallTopGroup)
                    elif i == 29:
                        self.walls.createWall(x, 430, 14, self.wallTopGroup)
                    elif i == 32:   
                        self.walls.createWall(x, 430, 18, self.wallTopGroup)
                    else:
                        self.walls.createWall(x, 430, 10, self.wallTopGroup)
            else:    
                fakeX = x
                for i in range(0, 3):
                    tile = DirtTile(self.dirtImage, fakeX, 450)
                    self.dirtGroup.add(tile)
                    tile = DirtTile(self.dirtImage, fakeX, 465)
                    self.dirtGroup.add(tile)
                    tile = DirtTile(self.dirtImage, fakeX, 480)
                    self.dirtGroup.add(tile)
                    tile = DirtTile(self.dirtImage, fakeX, 495)
                    self.dirtGroup.add(tile)
                    tile = DirtTile(self.dirtImage, fakeX, 510)
                    self.dirtGroup.add(tile)
                    tile = DirtTile(self.dirtImage, fakeX, 525)
                    self.dirtGroup.add(tile)
                    fakeX += self.dirtImage.get_width() - 10

    def createPlatforms(self, wallColors):
        for i in range(self.tilesNeeded):
            x = i * (self.tileWidth - self.OVERLAP_X)
            if i in [11, 17, 23, 37, 43]:
                if wallColors[self.numWalls] == 0:
                    if i == 11:
                        self.walls.createPlatform(x + 5, 305, self.tanPlatform, self.platformGroup, True)
                        self.walls.createPlatform(x + 60, 420, self.tanPlatform, self.platformGroup, True)
                    elif i == 23:
                        self.walls.createPlatform(x + 60, 275, self.tanPlatform, self.platformGroup, True)
                        self.walls.createPlatform(x + 40, 420, self.tanPlatform, self.platformGroup, True)
                    elif i == 37:
                        self.walls.createPlatform(x + 55, 275, self.tanPlatform, self.platformGroup, True)
                        self.walls.createPlatform(x + 10, 420, self.tanPlatform, self.platformGroup, True)
                    elif i == 43:
                        self.walls.createPlatform(x + 90, 275, self.tanPlatform, self.platformGroup, True)
                        self.walls.createPlatform(x + 5, 365, self.tanPlatform, self.platformGroup, False)
                    else:
                        self.walls.createPlatform(x + 57, 285, self.tanPlatform, self.platformGroup, True)
                elif wallColors[self.numWalls] == 1:
                    if i == 11:
                        self.walls.createPlatform(x + 5, 305, self.grayPlatform, self.platformGroup, True)
                        self.walls.createPlatform(x + 60, 420, self.grayPlatform, self.platformGroup, True)
                    elif i == 23:
                        self.walls.createPlatform(x + 60, 275, self.tanPlatform, self.platformGroup, True)
                        self.walls.createPlatform(x + 40, 420, self.tanPlatform, self.platformGroup, True)
                    elif i == 37:
                        self.walls.createPlatform(x + 55, 275, self.tanPlatform, self.platformGroup, True)
                        self.walls.createPlatform(x + 10, 420, self.tanPlatform, self.platformGroup, True)
                    elif i == 43:
                        self.walls.createPlatform(x + 90, 275, self.tanPlatform, self.platformGroup, True)
                        self.walls.createPlatform(x + 5, 365, self.tanPlatform, self.platformGroup, False)
                    else: 
                        self.walls.createPlatform(x + 57, 285, self.grayPlatform, self.platformGroup, True)

    def crop_edges(self, surface, left=1, right=1, top=0, bottom=0):
        w, h = surface.get_width(), surface.get_height()
        rect = pygame.Rect(left, top, max(1, w - left - right), max(1, h - top - bottom))
        return surface.subsurface(rect).copy()

    def drawRocks(self, scroll, screen, SCREEN_WIDTH):
        for rock in self.rockGroup:
            x = rock.rect.x - (scroll * .30)
            if -rock.image.get_width() < x < SCREEN_WIDTH:
                screen.blit(rock.image, (x, 395))

    def drawGround(self, lScreenEdge, screen, SCREEN_WIDTH):
        lVisibleEnd = lScreenEdge
        rVisibleEnd = lScreenEdge + SCREEN_WIDTH

        for ground in self.groundGroup:
            if ground.rect.right > lVisibleEnd and ground.rect.left < rVisibleEnd:
                x = ground.rect.x - lScreenEdge
                screen.blit(ground.image, (x, ground.rect.y))
                
        for end in self.groundEndGroup:
           if end.rect.right > lVisibleEnd and end.rect.left < rVisibleEnd:
                x = end.rect.x - lScreenEdge
                screen.blit(end.image, (x, end.rect.y))

        self.walls.drawWalls(lScreenEdge, screen, SCREEN_WIDTH)

        for wallTop in self.wallTopGroup:
            if wallTop.rect.right > lVisibleEnd and wallTop.rect.left < rVisibleEnd:
                x = wallTop.rect.x - lScreenEdge
                screen.blit(wallTop.image, (x, wallTop.rect.y))
        
        self.walls.drawWallEdges(lScreenEdge, screen, SCREEN_WIDTH)

        for platform in self.platformGroup:
            if platform.rect.right > lVisibleEnd and platform.rect.left < rVisibleEnd:
                x = platform.rect.x - lScreenEdge
                screen.blit(platform.image, (x, platform.rect.y))
            
    def drawDirt(self, lScreenEdge, screen, SCREEN_WIDTH):
        lVisibleEnd = lScreenEdge
        rVisibleEnd = lScreenEdge + SCREEN_WIDTH

        for dirt in self.dirtGroup:
            if dirt.rect.right > lVisibleEnd and dirt.rect.left < rVisibleEnd:
                x = dirt.rect.x - lScreenEdge
                screen.blit(dirt.image, (x, dirt.rect.y))

    def getGroundGroup(self):
        return self.groundGroup

class GroundTile(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = image
        self.rect = image.get_rect(topleft=(x,y))

class DirtTile(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = image
        self.rect = image.get_rect(topleft=(x,y))

class RockTile(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = image
        self.rect = image.get_rect(topleft=(x,y))