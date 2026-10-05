import pygame

class HealthPotions:
    def __init__(self, potionCount, x, y):
        self.maxPotionCount = potionCount
        self.currentPotionCount = potionCount
        self.x = x
        self.y = y

        scaledSize = (32, 32)
        self.sheetImage = pygame.image.load('Health/alchemySprites.png').convert()
        potionRect = pygame.Rect(39, 22, 13, 12)
        self.potionImage = self.sheetImage.subsurface(potionRect)
        self.potionImage.set_colorkey((255, 0, 255))
        self.potionImage = pygame.transform.scale(self.potionImage, scaledSize)

        self.font = pygame.font.Font(None, 40)

    def draw(self, screen):
        self.potionCount = self.font.render(f"{self.currentPotionCount} X ", True, (0, 0, 0))
        screen.blit(self.potionCount, (self.x - (self.potionCount.get_width() - 10), self.y + (6)))
        screen.blit(self.potionImage, (self.x + 10, self.y))

    def usePotion(self):
        if self.currentPotionCount > 0:
            self.currentPotionCount -= 1

    def gainPotion(self):
        if self.currentPotionCount < self.maxPotionCount:
            self.currentPotionCount += 1