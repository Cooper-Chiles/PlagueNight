import pygame, ground, foreground

class Background:
    OVERLAP_X = 1

    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT):
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        
        self.fbgImages = []
        self.createScenes()
        self.adjustScenes()

        self.fbgImages = [self.crop_edges(img, left=5, right=5) for img in self.fbgImages]
        self.fbgImages[0] = self.crop_edges(self.fbgImages[0], left=8, right=8)
        self.layer_speeds = [.40, 0.25, 0.20, 0.18]

        self.fg = foreground.Foreground(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        self.gd = ground.Ground(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        self.drawnTrees = False
        self.drawnBTrees = False
        self.drawnCloseTrees = False
        self.drawnWalls = False

    def createScenes(self):
        for i in range(0, 4): 
            img = pygame.image.load(f"Images/forest{i}.png").convert_alpha()
            self.fbgImages.append(img)
        
    def adjustScenes(self):
        for b in range(0, 3):
            bgHeight = self.fbgImages[b].get_height()
            bgWidth = self.fbgImages[b].get_width()
            heightScale = self.SCREEN_HEIGHT / bgHeight
            newWidth = int(bgWidth * heightScale)
            self.fbgImages[b] = pygame.transform.scale(self.fbgImages[b], (newWidth, self.SCREEN_HEIGHT))

    def crop_edges(self, surface, left=1, right=1, top=0, bottom=0):
        w, h = surface.get_width(), surface.get_height()
        rect = pygame.Rect(left, top, max(1, w - left - right), max(1, h - top - bottom))
        return surface.subsurface(rect).copy()

    def drawbg(self, scroll, screen, lScreenEdge): 
        bgImages = self.fbgImages

        self.draw_tiled_layer(bgImages[0], self.layer_speeds[3], -15, scroll, screen)
        self.draw_tiled_layer(bgImages[1], self.layer_speeds[2], -15, scroll, screen)          
        self.draw_tiled_layer(bgImages[2], self.layer_speeds[1], -15, scroll, screen, 0)    
        self.fg.drawForeGroundTrees(scroll, screen)
        self.gd.drawRocks(scroll, screen, self.SCREEN_WIDTH)
        self.draw_tiled_layer(bgImages[3], self.layer_speeds[0], 405, scroll, screen, 0)  
        self.fg.drawForeGroundWalls(lScreenEdge, screen)
        self.gd.drawDirt(lScreenEdge, screen, self.SCREEN_WIDTH)
        self.gd.drawGround(lScreenEdge, screen, self.SCREEN_WIDTH) 

    def drawOverlays(self, screen):
        overlay = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((200, 200, 200, 50))  # (R,G,B,A) — light gray fog, semi-transparent
        screen.blit(overlay, (0, 0))
        overlay = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(145)
        screen.blit(overlay, (0, 0))
    
    def draw_tiled_layer(self, img, speed, y, scroll, screen, overlap=OVERLAP_X):
        """
        Tiles 'img' across the screen at vertical position 'y' while applying
        horizontal parallax based on global 'scroll' and the given 'speed'.
        """
        w = img.get_width()
        step = max(1, w - overlap)          # overlap tiling to hide seams
        offset = int((-scroll * speed) % step)
        start_x = -w + offset
        tiles = (self.SCREEN_WIDTH // step) + 3
        for i in range(tiles):
            x = start_x + i * step
            screen.blit(img, (x, y))