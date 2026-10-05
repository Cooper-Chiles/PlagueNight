import pygame

class EnemyHealth:
    def __init__(self, healthCount):
        self.maxHealth = healthCount
        self.currentHealth = healthCount
        self.x = 0
        self.y = 0

        scaledSize = (16, 16)
        self.sheet = pygame.image.load('Health/hearts.jpg')
        enemyFullRect = pygame.Rect(20, 110, 120, 115)
        self.enemyFull = self.sheet.subsurface(enemyFullRect)
        self.enemyFull.set_colorkey((0, 0, 0))
        self.enemyFull = pygame.transform.scale(self.enemyFull, scaledSize)
        enemyEmptyRect = pygame.Rect(490, 110, 120, 115)
        self.enemyEmpty = self.sheet.subsurface(enemyEmptyRect)
        self.enemyEmpty.set_colorkey((0, 0, 0))
        self.enemyEmpty = pygame.transform.scale(self.enemyEmpty, scaledSize)

    def loseHealth(self, health):
        self.currentHealth -= health

    def isDead(self):
        return self.currentHealth <= 0