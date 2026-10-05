import pygame, background, ground, zombie, healthPotionItem, crystalItem, endFlag, random

class StageControl:
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT):
        self.background = background.Background(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.zombies = pygame.sprite.Group()
        self.healthPotions = pygame.sprite.Group()
        self.crystals = pygame.sprite.Group()
        self.flags = pygame.sprite.Group()

    def bgDraw(self, scroll, screen, lScreenEdge):
        self.background.drawbg(scroll, screen, lScreenEdge)

    def bgDrawOverlays(self, screen):
        self.background.drawOverlays(screen)
    
    def fgDraw(self, GAMESCREENX, scroll, screen):
        if not self.background.drawnBTrees:
            self.background.fg.drawTrees(self.background.fg.bTreeImages, GAMESCREENX + 250, "blue")
            self.background.drawnBTrees = True
        if not self.background.drawnTrees:
            self.background.fg.drawTrees(self.background.fg.treeImages, GAMESCREENX + 250, "not close")
            self.background.drawnTrees = True
        if not self.background.drawnCloseTrees:
            self.background.fg.drawTrees(self.background.fg.closeTreeImages, GAMESCREENX + 250, "close")
            self.background.drawnCloseTrees = True
        if not self.background.drawnWalls:
            self.background.fg.drawWalls(5)
            self.background.gd.createPlatforms(self.background.fg.wallColors)
            self.background.drawnWalls = True
        self.background.fg.drawCloseGround(scroll, screen)

    def addPotions(self):
        healthPotion1 = healthPotionItem.HealthPotion(1075, 330)
        healthPotion2 = healthPotionItem.HealthPotion(2250, 240)
        healthPotion3 = healthPotionItem.HealthPotion(3000, 385)
        healthPotion4 = healthPotionItem.HealthPotion(4140, 40)
        healthPotion5 = healthPotionItem.HealthPotion(4810, 240)
        self.healthPotions.add(healthPotion1)
        self.healthPotions.add(healthPotion2)
        self.healthPotions.add(healthPotion3)
        self.healthPotions.add(healthPotion4)
        self.healthPotions.add(healthPotion5)

    def addZombies(self):
        zombie0 = zombie.Zombie((0, 850), 0, 0)
        zombie1 = zombie.Zombie((730, 350), 40, 2)
        zombie2 = zombie.Zombie((2075, 350), 40, 2)
        zombie3 = zombie.Zombie((2325, 270), 40, 2)
        zombie4 = zombie.Zombie((5325, 350), 40, 2)
        zombie5 = zombie.Zombie((5375, 350), 40, 2)
        zombie6 = zombie.Zombie((5425, 350), 40, 2)
        zombie7 = zombie.Zombie((5475, 350), 40, 2)
        zombie8 = zombie.Zombie((5525, 350), 40, 2)
        zombie9 = zombie.Zombie((5575, 350), 40, 2)
        zombie10 = zombie.Zombie((5625, 350), 40, 2)
        self.zombies.add(zombie0)
        self.zombies.add(zombie1)
        self.zombies.add(zombie2)
        self.zombies.add(zombie3)
        self.zombies.add(zombie4)
        self.zombies.add(zombie5)
        self.zombies.add(zombie6)
        self.zombies.add(zombie7)
        self.zombies.add(zombie8)
        self.zombies.add(zombie9)
        self.zombies.add(zombie10)

    def addCrystals(self):
        color = random.randint(1, 3)
        crystal0 = crystalItem.CrystalItem(800, 400, color)
        color = random.randint(1, 3)
        crystal1 = crystalItem.CrystalItem(1700, 400, color)
        color = random.randint(1, 3)
        crystal2 = crystalItem.CrystalItem(2160, 400, color)
        color = random.randint(1, 3)
        crystal3 = crystalItem.CrystalItem(2415, 350, color)
        color = random.randint(1, 3)
        crystal4 = crystalItem.CrystalItem(2745, 400, color)
        color = random.randint(1, 3)
        crystal5 = crystalItem.CrystalItem(3625, 345, color)
        crystal6 = crystalItem.CrystalItem(4260, 365, 4)
        color = random.randint(1, 3)
        crystal7 = crystalItem.CrystalItem(5035, 365, color)
        crystal8 = crystalItem.CrystalItem(5400, 400, 4)
        crystal9 = crystalItem.CrystalItem(5700, 400, 4)
        self.crystals.add(crystal0)
        self.crystals.add(crystal1)
        self.crystals.add(crystal2)
        self.crystals.add(crystal3)
        self.crystals.add(crystal4)
        self.crystals.add(crystal5)
        self.crystals.add(crystal6)
        self.crystals.add(crystal7)
        self.crystals.add(crystal8)
        self.crystals.add(crystal9)
    
    def addFlag(self):
        flag = endFlag.EndFlag(5940, 200)
        self.flags.add(flag)
    
    def updateZombies(self, player, screen, lScreenEdge, SCREEN_WIDTH, SCREEN_HEIGHT):
        for zombie in self.zombies:
            zombie.update(lScreenEdge, player, self.getWalls(), self.getPlatformWalls(), SCREEN_WIDTH)
            zombie.takeDamage(player.outputDamage)
            zombie.gravity(self.getGround(), self.getWallTop(),  lScreenEdge, SCREEN_HEIGHT)
            screen.blit(zombie.image, (zombie.rect.x, zombie.rect.y))

    def updatePotions(self, screen, lScreenEdge):
        for potion in self.healthPotions:
            potion.update()
            potion.draw(screen, lScreenEdge)

    def updateCrystals(self, screen, lScreenEdge):
        for crystal in self.crystals:
            crystal.update()
            crystal.draw(screen, lScreenEdge)

    def updateFlag(self, screen, lScreenEdge):
        for flag in self.flags:
            flag.update()
            flag.draw(screen, lScreenEdge)

    def getGround(self):
        return self.background.gd.getGroundGroup()
    
    def getWalls(self):
        return self.background.gd.walls.getWalls()

    def getPlatforms(self):
        return self.background.gd.platformGroup

    def getPlatformWalls(self):
        return self.background.gd.walls.getPlatformWalls()

    def getWallTop(self):
        return self.background.gd.wallTopGroup

    def getZombies(self):
        return self.zombies

    def getHealthPotions(self):
        return self.healthPotions

    def getCrystals(self):
        return self.crystals

    def getFlags(self):
        return self.flags