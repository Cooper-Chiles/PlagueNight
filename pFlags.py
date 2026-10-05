import pygame

class PlayerFlag:
    def __init__(self, x, y):
        self.currentFlagCount = 0
        self.x = x
        self.y = y

        scaledSize = (32, 32)
        self.flag = pygame.image.load("Images/flag.png").convert_alpha()
        self.flag.set_clip(pygame.Rect(4, 7, 34, 52))
        self.image = self.flag.subsurface(self.flag.get_clip())
        self.flagImage = pygame.transform.scale(self.image, scaledSize)
        self.font = pygame.font.Font(None, 40)

    def draw(self, screen):
        self.flagCount = self.font.render(f"{self.currentFlagCount} X ", True, (0, 0, 0))
        screen.blit(self.flagCount, (self.x - (self.flagCount.get_width()) + 10, self.y + (6)))
        screen.blit(self.flagImage, (self.x + 10, self.y + 2))

    def gainFlag(self):
        self.currentFlagCount += 1