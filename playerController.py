import pygame, player

class PlayerControl:
    def __init__(self, x, y):
        self.player = player.Character((x, y))
        self.showBPreMessage = None
        self.showHPreMessage = None
        self.preBMessageStart = 0
        self.preHMessageStart = 0
        self.preMessageDuration = 2500
        self.bshown = False
        self.hshown = False
        self.font = pygame.font.SysFont(None, 24)

    def drawPlayerInfo(self, screen):
        self.player.health.draw(screen)
        self.player.potions.draw(screen)
        self.player.crystals.draw(screen)
        self.player.flags.draw(screen)
        if self.player.boosted:
            self.player.printDamageBoost(screen)

    def playerMovement(self, key, scroll, pScrollSpeed, lScreenEdge, rScreenEdge, SCREEN_WIDTH, GAMESCREENX, HORIZONTAL_MARGIN):
        if key[pygame.K_LEFT]:
            if self.player.rect.x > HORIZONTAL_MARGIN:
                self.player.update('left')
        
            elif lScreenEdge > 0:
                lScreenEdge -= pScrollSpeed
                rScreenEdge -= pScrollSpeed
                scroll -= pScrollSpeed
                self.player.update('left')
                self.player.rect.x += pScrollSpeed

            elif self.player.rect.x > 0:
                self.player.update('left')
    
        if key[pygame.K_RIGHT]:
            if self.player.rect.x < SCREEN_WIDTH - HORIZONTAL_MARGIN:
                self.player.update('right')

            elif rScreenEdge >= GAMESCREENX and self.player.rect.x + self.player.rect.width <= SCREEN_WIDTH:
                self.player.update('right')

            else:
                if rScreenEdge < GAMESCREENX:
                    lScreenEdge += pScrollSpeed
                    rScreenEdge += pScrollSpeed
                    scroll += pScrollSpeed
                    self.player.update('right')
                    self.player.rect.x -= pScrollSpeed

        return scroll, lScreenEdge, rScreenEdge

    def playerActions(self, screen, lScreenEdge, SCREEN_WIDTH, healthPotions, crystals, flags, groundGroup, enemyGroup, wallGroup, wallTopGroup):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not self.player.isAttacking:
                        self.player.attackRelease = False
                        self.player.attack()
                elif event.key == pygame.K_b:
                    if not self.bshown:
                        self.showBPreMessage = "boost"
                        self.preBMessageStart = pygame.time.get_ticks()
                elif event.key == pygame.K_v:
                    if not self.hshown:
                        self.showHPreMessage = "heal"
                        self.preHMessageStart = pygame.time.get_ticks()
            
            if event.type == pygame.KEYUP:   
                if event.key == pygame.K_LEFT:
                    if self.player.rect.x > 0:
                        self.player.update('stand_left')
                    else:
                        self.player.update('stand_right')
                elif event.key == pygame.K_RIGHT:
                    if self.player.rect.x < SCREEN_WIDTH - self.player.rect.width:
                        self.player.update('stand_right')
                    else:
                        self.player.update('stand_left')
                elif event.key == pygame.K_b:
                    self.player.damageBoost()
                elif event.key == pygame.K_v:
                    self.player.heal(1)
                elif event.key == pygame.K_SPACE:
                    self.player.attackRelease = True
                    self.player.attackCharging = False

                    now = pygame.time.get_ticks()
                    self.player.chargeAmt = now - self.player.chargeStart
                elif event.key == pygame.K_c:
                    self.player.interactItems(healthPotions, crystals, flags, lScreenEdge)
                elif event.key == pygame.K_UP:
                    self.player.update('up')

        self.player.updateAttack()
        self.player.updateBoost()
        self.player.thrownPotions.draw(screen)
        for potion in self.player.thrownPotions:
            potion.update()
            potion.checkHit(lScreenEdge, groundGroup, enemyGroup, wallGroup, wallTopGroup, self.player.explosions)

    def checkCollisions(self, wtgroup, wgroup, ggroup, pwgroup, pgroup, screen, healthPotions, crystals, flags, lScreenEdge, SCREEN_WIDTH, SCREEN_HEIGHT):
        self.player.checkCollisionWall(wgroup, pwgroup, lScreenEdge)
        if not self.player.onGround:
            self.player.gravity(lScreenEdge, SCREEN_HEIGHT) 
        self.player.jumpLanding(wtgroup, ggroup, pgroup, lScreenEdge)
        self.player.checkCollisionFloor(wtgroup, ggroup, pgroup, lScreenEdge)
        self.player.updateState()
        if not self.player.flashing:
            screen.blit(self.player.image, self.player.rect)
        if self.showBPreMessage:
            if pygame.time.get_ticks() - self.preBMessageStart > self.preMessageDuration:
                self.showBPreMessage = None
        if self.showHPreMessage:
            if pygame.time.get_ticks() - self.preHMessageStart > self.preMessageDuration:
                self.showHPreMessage = None
        
        if self.showBPreMessage == 'boost' and self.showHPreMessage == 'heal':
            text = self.font.render(f"Boost will use 5 Crystals", True, (0, 206, 200))
            screen.blit(text, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10))
            text = self.font.render(f"Heal will use 1 Potion", True, (255, 0, 0))
            screen.blit(text, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 10))
            self.bshown = True
            self.hshown = True
        elif self.showBPreMessage == 'boost':
            text = self.font.render(f"Boost will use 5 Crystals", True, (0, 206, 200))
            screen.blit(text, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.bshown = True
        elif self.showHPreMessage == 'heal':
            text = self.font.render(f"Heal will use 1 Potion", True, (255, 0, 0))
            screen.blit(text, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.hshown = True
        self.player.interactableItems(screen, healthPotions, crystals, flags, lScreenEdge)

    def checkExplosions(self, screen):
        for explosion in self.player.explosions:
            explosion.updateExplosion()
            explosion.draw(screen)

    def checkWin(self):
        fCount = self.player.flags.currentFlagCount
        cCount = self.player.crystals.currentPinkCrystalCount 

        winConditions = False
        if fCount == 1 and cCount == 3:
            winConditions = True

        return winConditions