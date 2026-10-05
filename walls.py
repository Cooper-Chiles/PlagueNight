import pygame, ground

class Wall:
    def __init__(self, image, lcap, rcap):
        self.walls = [[]]
        self.walledge = [[]]
        self.platformWalls = [[]]
        self.wallCount = 0
        self.holeCount = 0
        self.platWallCount = 0
        self.image = image
        self.lcap = lcap
        self.rcap = rcap
        self.betweenTiles = 20

    def createWall(self, x, y, tileHeight, wallTopGroup):
        self.wallCount = len(self.walls) - 1

        for i in range(tileHeight):
            tile = ground.GroundTile(self.image, x, y - (i* self.betweenTiles))
            if i == tileHeight - 1:
                ltile = ground.GroundTile(self.lcap, x - 10, y - (i* self.betweenTiles))
                self.walledge[self.wallCount].append(ltile)
                wallTopGroup.add(tile)
                rtile = ground.GroundTile(self.rcap, x + 75, y - (i* self.betweenTiles))
                self.walledge[self.wallCount].append(rtile)
            else:
                ltile = ground.GroundTile(self.lcap, x - 10, y - (i* self.betweenTiles))
                self.walledge[self.wallCount].append(ltile)
                self.walls[self.wallCount].append(tile)
                rtile = ground.GroundTile(self.rcap, x + 75, y - (i* self.betweenTiles))
                self.walledge[self.wallCount].append(rtile)
        self.wallCount += 1
        self.walls.append([])  
        self.walledge.append([])

    def createPlatform(self, x, y, img, platformGroup, hasWall):
        self.platWallCount = len(self.platformWalls) - 1
        tile = ground.GroundTile(img, x, y)
        platformGroup.add(tile)
        if hasWall:
            tile = ground.GroundTile(img, x, y + 5)
            self.platformWalls[self.platWallCount].append(tile)
            self.platWallCount += 1
            self.platformWalls.append([])

    def addHoleWall(self, x, y, tileHeight, wallTopGroup, direction):
        self.holeCount = len(self.walls) - 1
        offset = 0
        if direction == "left":
            img = self.lcap
            offset = -20
        else:
            img = self.rcap
            offset = 75

        tiles = tileHeight

        for i in range(tileHeight):
            tile = ground.GroundTile(self.image, x, y + (i * self.betweenTiles))
            if i == 0:
                wallTopGroup.add(tile)
            else:
                self.walls[self.holeCount].append(tile)

        edgey = y + (tileHeight - 1) * self.betweenTiles
        for i in range(tileHeight):  
            edge = ground.GroundTile(img, x + offset, edgey - (i * self.betweenTiles))
            if i == tileHeight - 1:
                self.walledge[self.wallCount].append(edge)
            else:
                self.walledge[self.wallCount].append(edge)
            self.holeCount += 1
            self.walls.append([])  
            self.walledge.append([])

    def drawWalls(self, lScreenEdge, screen, SCREEN_WIDTH):
        lVisibleEnd = lScreenEdge
        rVisibleEnd = lScreenEdge + SCREEN_WIDTH

        for wall in self.walls:
            for tile in wall:
                if tile.rect.right > lVisibleEnd and tile.rect.left < rVisibleEnd:
                    x = tile.rect.x - lScreenEdge
                    screen.blit(tile.image, (x, tile.rect.y))


    def drawWallEdges(self, lScreenEdge, screen, SCREEN_WIDTH):
        lVisibleEnd = lScreenEdge
        rVisibleEnd = lScreenEdge + SCREEN_WIDTH

        for wall in self.walledge:
            for tile in wall:
                if tile.rect.right > lVisibleEnd and tile.rect.left < rVisibleEnd:
                    x = tile.rect.x - lScreenEdge
                    screen.blit(tile.image, (x, tile.rect.y))


    def getWalls(self):
        return self.walls

    def getPlatformWalls(self):
        return self.platformWalls