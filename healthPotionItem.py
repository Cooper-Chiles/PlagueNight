import pygame

class HealthPotion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.floatingY = y

        scaledSize = (32, 32)
        self.sheetImage = pygame.image.load('Health/alchemySprites.png').convert()
        potionRect = pygame.Rect(39, 22, 13, 12)
        self.potionImage = self.sheetImage.subsurface(potionRect)
        self.potionImage.set_colorkey((255, 0, 255))
        self.image = pygame.transform.scale(self.potionImage, scaledSize)
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.hitbox = self.rect.inflate(40, 0)

        self.timeToUpdate = 400
        self.beforeUpdate = 0
        self.afterUpdate = 0
        self.interacted = False

    def draw(self, screen, scroll):
        if not self.interacted:
            x = self.x - scroll 
            y = self.floatingY
            self.rect.topleft = (x, y)
            self.hitbox.midbottom = self.rect.midbottom
            screen.blit(self.image, (x, y))

    def update(self):
        self.beforeUpdate = pygame.time.get_ticks()
        if abs(self.beforeUpdate - self.afterUpdate) > self.timeToUpdate:
            if self.floatingY == self.y:
                self.floatingY -= 5
                self.afterUpdate = pygame.time.get_ticks()
            elif self.floatingY < self.y:
                self.floatingY += 5

    def interact(self):
        if not self.interacted:
            self.interacted = True
            