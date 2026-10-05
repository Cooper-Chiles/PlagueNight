import pygame

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y

        self.scaledSize = (32, 32)
        self.sheet = pygame.image.load('Sprites/PlagueKnightSpritesheet.png').convert()
        explosionRect = pygame.Rect(2, 557, 59, 51)
        self.explosionImage = self.sheet.subsurface(explosionRect)
        self.explosionImage.set_colorkey((0, 255, 0))
        self.image = pygame.transform.scale(self.explosionImage, self.scaledSize)
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

        self.frame = 0
        self.lastUpdate = 0
        self.animated = False
        self.explosion_states = {0: (2, 557, 59, 51), 1: (63, 557, 59, 51), 2: (124, 557, 59, 51), 3: (185, 557, 59, 51), 4: (246, 557, 59, 51), 5: (307, 557, 59, 51), 6: (368, 557, 59, 51), 7: (429, 557, 59, 51)}
    
    def trigger(self):
        self.frame = 0
        self.animated = True
        self.lastUpdate = pygame.time.get_ticks()

    def updateExplosion(self):
        if not self.animated:
            return

        if pygame.time.get_ticks() - self.lastUpdate > 100:
            self.frame += 1
            self.lastUpdate = pygame.time.get_ticks()
            if self.frame >= len(self.explosion_states):
                self.animated = False
                self.frame = 0
                self.kill()
                return

        frameRect = pygame.Rect(self.explosion_states[self.frame])
        self.image = self.sheet.subsurface(frameRect)
        self.image = pygame.transform.scale(self.image, self.scaledSize)
        self.image.set_colorkey((0, 255, 0))

    def draw(self, screen):
        screen.blit(self.image, self.rect)