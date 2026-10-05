import pygame

class PlayerCrystals:
    def __init__(self, x, y):
        self.currentCrystalCount = 0
        self.currentPinkCrystalCount = 0
        self.crystalAmtForBoost = 5
        self.x = x
        self.y = y

        scaledSize = (32, 32)
        self.sheetImage = pygame.image.load('Health/Crystals/Green/green0.png').convert()
        self.sheetImage.set_colorkey((255, 255, 255))
        self.purpleCrystalImage = pygame.transform.scale(self.sheetImage, scaledSize)
        self.sheetImage = pygame.image.load('Health/Crystals/Pink/pink0.png').convert()
        self.sheetImage.set_colorkey((255, 255, 255))
        self.pinkCrystalImage = pygame.transform.scale(self.sheetImage, scaledSize)
        self.font = pygame.font.Font(None, 40)


    def draw(self, screen):
        self.crystalCount = self.font.render(f"{self.currentCrystalCount} X ", True, (0, 0, 0))
        screen.blit(self.crystalCount, (self.x - (self.crystalCount.get_width()) + 10, self.y + (6)))
        screen.blit(self.purpleCrystalImage, (self.x, self.y))
        self.crystalCount = self.font.render(f"{self.currentPinkCrystalCount} X ", True, (0, 0, 0))
        screen.blit(self.crystalCount, (self.x - (self.crystalCount.get_width()) + 10, self.y + (36)))
        screen.blit(self.pinkCrystalImage, (self.x, self.y + (30)))

    def useCrystals(self):
        self.currentCrystalCount -= 5

    def gainCrystal(self, color):
        if color == 3:
            self.currentCrystalCount += 1
        elif color == 2:
            self.currentCrystalCount += 2
        elif color == 1:
            self.currentCrystalCount += 3
        elif color == 4:
            self.currentPinkCrystalCount += 1