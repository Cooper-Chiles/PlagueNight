import pygame

class CrystalItem(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.x = x
        self.y = y
        self.floatingY = y
        self.color = color
        self.images = []

        self.scaledSize = (40, 40)
        if color == 1:
            folder = "Blue"
            img = "blue"
        elif color == 2:
            folder = "Red"
            img = "red"
        elif color == 3:
            folder = "Purple"
            img = "purple"
        elif color == 4:
            folder = "Pink"
            img = "pink"

        for i in range(0, 4):
            path = f"Health/Crystals/{folder}/{img}{i}.png"
            image = pygame.image.load(path)
            image.set_colorkey((255, 255, 255))
            self.images.append(image)

        self.frame = 0
        self.counter = 0
        self.image = pygame.transform.scale(self.images[self.frame], self.scaledSize)
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.timeToUpdate = 600
        self.beforeUpdate = 0
        self.afterUpdate = 0
        self.interacted = False

    def update(self):
        self.counter += 1
        if self.counter >= 4:
            self.counter = 0
            self.frame = (self.frame + 1) % 4
            self.image = self.images[self.frame]
            self.image = pygame.transform.scale(self.images[self.frame], self.scaledSize)

        self.beforeUpdate = pygame.time.get_ticks()
        if abs(self.beforeUpdate - self.afterUpdate) > self.timeToUpdate:
            if self.floatingY == self.y:
                self.floatingY -= 5
                self.afterUpdate = pygame.time.get_ticks()
            elif self.floatingY < self.y:
                self.floatingY += 5
    
    def draw(self, screen, scroll):
        if not self.interacted:
            x = self.x - scroll 
            y = self.floatingY
            self.rect.topleft = (x, y)
            screen.blit(self.image, (x, y))

    def interact(self):
        if not self.interacted:
            self.interacted = True