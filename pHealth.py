import pygame

class PlayerHealth:
    def __init__(self, healthCount, x, y):
        self.maxHealth = healthCount
        self.currentHealth = healthCount
        self.minHealth = 1
        self.x = x
        self.y = y

        scaledSize = (32, 32)
        self.grimFull = pygame.image.load('Health/Grimhealth.jpg')
        self.grimFull = pygame.transform.scale(self.grimFull, scaledSize)
        self.grimFull = pygame.transform.flip(self.grimFull, True, False)
        self.grimEmpty = pygame.image.load('Health/GrimhealthEmpty.png').convert_alpha()
        self.grimEmpty = pygame.transform.scale(self.grimEmpty, scaledSize)
        self.grimEmpty = pygame.transform.flip(self.grimEmpty, True, False)


    def draw(self, screen):
        for i in range(self.maxHealth):
            if i < self.currentHealth:
                screen.blit(self.grimFull, (self.x + (i * 30), self.y))

    def gainHealth(self, health):
        self.currentHealth += health
        
    def loseHealth(self, health):
        self.currentHealth -= health

    def isDead(self):
        return self.currentHealth <= 0