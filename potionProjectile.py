import pygame, projectileExplosion

class ThrowPotion(pygame.sprite.Sprite):
    def __init__(self, x, y, facingLeft, power):
        super().__init__()
        self.x = x
        self.y = y

        scaledSize = (32, 32)
        self.sheetImage = pygame.image.load('Health/alchemySprites.png').convert()
        potionRect = pygame.Rect(22, 22, 12, 12)
        self.potionImage = self.sheetImage.subsurface(potionRect)
        self.potionImage.set_colorkey((255, 0, 255))
        self.image = pygame.transform.scale(self.potionImage, scaledSize)
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

        if facingLeft:
            self.vx = -20 * power
        else:
            self.vx = 20 * power
        self.vy = -5 * power
        self.gravity = .5

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self):
        self.vy += self.gravity
        self.rect.x += self.vx
        self.rect.y += self.vy

    def checkHit(self, lScreenEdge, groundGroup, enemyGroup, wallGroup, wallTopGroup, explosionGroup):
        for ground in groundGroup:
            shiftedGround = pygame.Rect(ground.rect.x - lScreenEdge, ground.rect.y, ground.rect.width, ground.rect.height)
            if self.rect.colliderect(shiftedGround):
                self.kill()
                explosion = projectileExplosion.Explosion(self.rect.x, self.rect.y)
                explosion.trigger()
                explosionGroup.add(explosion)
                return

        for enemy in enemyGroup:
            if self.rect.colliderect(enemy.hitbox):
                enemy.damaged = True
                enemy.projectileHit = True
                self.kill()
                if self.vx > 0:
                    if enemy.facingLeft:
                        x = enemy.rect.left + 25
                    else:
                        x = enemy.rect.centerx - 10
                elif self.vx < 0:
                    if enemy.facingLeft:
                        x = enemy.rect.centerx + 10
                    else:
                        x = enemy.rect.right - 25

                explosion = projectileExplosion.Explosion(x, enemy.rect.centery + 20)
                explosion.trigger()
                explosionGroup.add(explosion)
                return

        for wall in wallGroup:
            for tile in wall:
                shiftedWall = pygame.Rect(tile.rect.x - lScreenEdge, tile.rect.y, tile.rect.width, tile.rect.height)
                if self.rect.colliderect(shiftedWall):
                    self.kill()
                    explosion = projectileExplosion.Explosion(self.rect.x, self.rect.y)
                    explosion.trigger()
                    explosionGroup.add(explosion)
                    return
        
        for walltop in wallTopGroup:
            shiftedWalltop = pygame.Rect(walltop.rect.x - lScreenEdge, walltop.rect.y, walltop.rect.width, walltop.rect.height)
            if self.rect.colliderect(shiftedWalltop):
                self.kill()
                explosion = projectileExplosion.Explosion(self.rect.x, self.rect.y)
                explosion.trigger()
                explosionGroup.add(explosion)
                return

