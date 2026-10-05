import pygame, eHealth

class Zombie(pygame.sprite.Sprite):
    def __init__(self, position, areaSize, colorNum):
        super().__init__()
        self.sheet = pygame.image.load(f"Sprites/Zombies/Zombie v{colorNum}.png").convert_alpha()  
        self.sheet.set_colorkey((0, 0, 0))

        self.sheet.set_clip(pygame.Rect(1, 1, 64, 64))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        scaledSize = (100, 100)
        self.image = pygame.transform.scale(self.image, scaledSize)
        self.rect = self.image.get_rect()
        self.rect.topleft = position

        trim_top = 30
        self.trim_sides = 40
        new_width = self.rect.width - self.trim_sides
        new_height = self.rect.height - trim_top

        self.hitbox = pygame.Rect(
            self.rect.x + self.trim_sides // 2,   
            self.rect.y + trim_top,
            new_width,
            new_height
        )

        self.startingX = position[0]
        self.startingY = position[1]
        self.currX = position[0]
        self.areaSize = areaSize
        self.leftBarrier = self.startingX - self.areaSize
        self.rightBarrier = self.startingX + self.areaSize + self.rect.width

        self.facingLeft = True

        self.frame = 0
        self.idle_states = {0: (1, 1, 64, 64), 1: (64, 1, 64, 64), 2: (128, 1, 64, 64), 3: (192, 1, 64, 64), 4: (256, 1, 64, 64), 5: (384, 1, 64, 64), 6: (412, 1, 64, 64)}
        self.right_states = {0: (448, 1, 64, 64), 1: (512, 1, 64, 64), 2: (576, 1, 64, 64), 3: (1, 64, 64, 64), 4: (64, 64, 64, 64), 5: (128, 64, 64, 64), 6: (192, 64, 64, 64), 7: (256, 64, 64, 64), 8: (448, 1, 64, 64)}
        self.left_states = {0: (448, 1, 64, 64), 1: (512, 1, 64, 64), 2: (576, 1, 64, 64), 3: (1, 64, 64, 64), 4: (64, 64, 64, 64), 5: (128, 64, 64, 64), 6: (192, 64, 64, 64), 7: (256, 64, 64, 64), 8: (448, 1, 64, 64)}
        self.slash_states = {0: (384, 64, 64, 64), 1: (448, 64, 64, 64), 2: (512, 64, 64, 64), 3: (576, 64, 64, 64), 4: (1, 128, 64, 64), 5: (64, 128, 64, 64), 6: (128, 128, 64, 64)}
        self.biting_states = {0: (192, 128, 64, 64), 1: (256, 128, 64, 64), 2: (320, 128, 64, 64), 3: (384, 128, 64, 64), 4: (448, 128, 64, 64)}
        self.movingSlash_states = {0: (512, 128, 64, 64), 1: (576, 128, 64, 64), 2: (1, 192, 64, 64), 3: (64, 192, 64, 64), 4: (128, 192, 64, 64), 5: (192, 192, 64, 64), 6: (256, 192, 64, 64), 7: (320, 192, 64, 64), 8: (384, 192, 64, 64)}
        self.getHit_states = {0: (448, 192, 64, 64), 1: (512, 192, 64, 64), 2: (576, 192, 64, 64), 3: (1, 256, 64, 64)}
        self.death_states = {0: (64, 256, 64, 64), 1: (128, 256, 64, 64), 2: (192, 256, 64, 64), 3: (256, 256, 64, 64), 4: (320, 256, 64, 64), 5: (384, 256, 64, 64), 6: (448, 256, 64, 64), 7: (512, 256, 64, 64), 8: (576, 256, 64, 64), 9: (1, 320, 64, 64), 10: (64, 320, 64, 64), 11: (128, 320, 64, 64), 12: (192, 320, 64, 64), 13: (256, 320, 64, 64)}
        self.health = eHealth.EnemyHealth(3)

        self.clock = pygame.time.Clock()
        self.isChasing = False
        self.isAttacking = False
        self.isReturning = False
        self.buffer = 200
        self.lastAttackTime = 0
        self.attackDelay = 300
        self.biteHit1 = 1
        self.biteHit2 = 3
        self.slashHit = 3
        self.movingSlashHit = 4
        self.barrierRange = 200
        self.scrollSpeed = 5
        self.tooFar = False
        self.centerX = self.currX + (self.rect.width // 2)
        self.hitUpdate = 0
        self.hitFrame = 0
        self.deathUpdate = 0
        self.deathFrame = 0
        self.hit = False
        self.beenHit = False
        self.damaged = False
        self.projectileHit = False
        self.vy = 0
        self.dx = 0
        self.downVelocity = 1
        self.onGround = True
        self.collidedWall = False

    def get_frame(self, frame_set):  # Get the next frame in the given frame set (animation loop).
        # Increment the frame counter.
        self.frame += 1
        
        # Loop back to the first frame if the counter exceeds the number of frames.
        if self.frame > (len(frame_set) - 1):
            self.frame = 0
        
        #print(frame_set[self.frame])  # Debugging: print the current frame's rectangle.
        return frame_set[self.frame] 

    def clip(self, clipped_rect):  # Set the clipping region (current frame) based on a provided rectangle.
        if type(clipped_rect) is dict:  # If the clipped rect is a dictionary (animation set), get the next frame.
            self.sheet.set_clip(pygame.Rect(self.get_frame(clipped_rect)))
        else:
            # Set the clipping area directly if it's a specific rectangle.
            self.sheet.set_clip(pygame.Rect(clipped_rect))
        return clipped_rect 

    def update(self, scroll, player, walls, pwalls, SCREEN_WIDTH):
        self.clock.tick(20)

        if self.beenHit:
            return

        self.detectPlayer(player, walls, pwalls, scroll, SCREEN_WIDTH)

        if not self.isAttacking:
            direction = None

            if self.isReturning:
                if abs(self.currX - self.startingX) <= 6:
                    self.currX = self.startingX
                    self.isReturning = False
                    direction = 'stand_left' if self.facingLeft else 'stand_right'
                else:
                    direction = 'left' if self.currX > self.startingX else 'right'
                    self.facingLeft = direction == 'left'

            elif not self.isChasing:
                if self.facingLeft:
                    if self.currX > self.leftBarrier:
                        direction = 'left'
                    else:
                        direction = 'right'
                        self.facingLeft = False
                else:
                    if self.currX < self.rightBarrier:
                        direction = 'right'
                    else:
                        direction = 'left'
                        self.facingLeft = True

            speed = 5
            if direction in ['left', 'right']:
                if direction == 'left':
                    self.clip(self.left_states)
                else:
                    self.clip(self.right_states)

                if not self.collidedWall:
                    self.dx = -speed if direction == 'left' else speed
                    self.currX += self.dx
                else:
                    self.dx = 0
            elif direction in ['stand_left', 'stand_right']:
                self.dx = 0
                self.clip(self.left_states[0] if direction == 'stand_left' else self.right_states[0])
            else:
                self.dx = 0

        self.checkCollisionWall(walls, pwalls, scroll)

        self.rect.x = self.currX - scroll
        self.hitbox.midbottom = self.rect.midbottom
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        scaledSize = (100, 100)
        self.image = pygame.transform.scale(self.image, scaledSize)
        if not self.facingLeft:
            self.image = pygame.transform.flip(self.image, True, False)

    def checkCollisionWall(self, walls, pwalls, scroll):
        self.collidedWall = False

        for wall in walls:
            for tile in wall:
                shiftedWall = pygame.Rect(tile.rect.x - scroll, tile.rect.y, tile.rect.width, tile.rect.height)

                if self.hitbox.colliderect(shiftedWall):
                    
                    if self.dx < 0 and self.hitbox.left >= shiftedWall.right - (self.trim_sides // 2):
                        self.currX = self.currX
                        self.dx = 0
                        self.collidedWall = True
                        
                    elif self.dx > 0 and self.hitbox.right <= shiftedWall.left + (self.trim_sides // 2):
                        self.currX = self.currX
                        self.dx = 0
                        self.collidedWall = True

                    self.hitbox.midbottom = self.rect.midbottom
                    return

        for wall in pwalls:
            for tile in wall:
                shiftedWall = pygame.Rect(tile.rect.x - scroll, tile.rect.y, tile.rect.width, tile.rect.height)

                if self.hitbox.colliderect(shiftedWall):
                    
                    if self.dx < 0 and self.hitbox.left >= shiftedWall.right - (self.trim_sides // 2):
                        self.currX = self.currX
                        self.dx = 0
                        self.collidedWall = True
                        
                    elif self.dx > 0 and self.hitbox.right <= shiftedWall.left + (self.trim_sides // 2):
                        self.currX = self.currX
                        self.dx = 0
                        self.collidedWall = True

                    self.hitbox.midbottom = self.rect.midbottom
                    return
   
    def detectPlayer(self, player, walls, pwalls, scroll, SCREEN_WIDTH):
        if not self.beenHit:
            playerDistance = abs(self.currX - (player.rect.x + scroll))
            playerTooHigh = player.rect.bottom > self.rect.top

            detectRange = 200 
            if playerDistance <= detectRange:
                self.facingLeft = player.rect.centerx < self.rect.centerx
                self.isChasing = True
                if playerDistance >= 30:
                    if self.facingLeft:
                        self.clip(self.left_states)
                        self.dx = -5
                    else:
                        self.clip(self.right_states)
                        self.dx = 5
                    self.checkCollisionWall(walls, pwalls, scroll)
                    if not self.collidedWall:
                        self.currX += self.dx
                elif self.hitbox.colliderect(player.hitbox) and playerTooHigh and (playerDistance <= 60 and playerDistance > 10):
                    self.clip(self.movingSlash_states)
                    if self.frame == self.movingSlashHit:
                        player.takeDamage(1)
                    self.isAttacking = True
                    if self.facingLeft:
                        self.dx = -6
                    else:
                        self.dx = 6
                    self.checkCollisionWall(walls, pwalls, scroll)
                    if not self.collidedWall:
                        self.currX += self.dx
                elif self.hitbox.colliderect(player.hitbox) and playerTooHigh and playerDistance <= 10:
                    self.clip(self.biting_states)
                    if (self.frame == self.biteHit1 or self.frame == self.biteHit2):
                        player.takeDamage(1)
                        self.isAttacking = True
            else:
                if self.isChasing:
                    self.isChasing = False
                    self.isAttacking = False
                    self.isReturning = True

    def gravity(self, floorGroup, wallTopGroup, lScreenEdge, SCREEN_HEIGHT):
        if self.startingY < SCREEN_HEIGHT:
            self.onGround = False
            for floor in floorGroup:
                shiftedFloor = pygame.Rect(floor.rect.x - lScreenEdge, floor.rect.y, floor.rect.width, floor.rect.height)
                if self.rect.colliderect(shiftedFloor):
                    self.onGround = True
            
            for walltop in wallTopGroup:
                shiftedWalltop = pygame.Rect(walltop.rect.x - lScreenEdge, walltop.rect.y, walltop.rect.width, walltop.rect.height)
                if self.rect.colliderect(shiftedWalltop): 
                    self.onGround = True

            if not self.onGround:
                self.vy += self.downVelocity
                self.rect.y += self.vy 
                if self.rect.top > SCREEN_HEIGHT:
                    self.kill()            

    def takeDamage(self, damage):
        if self.damaged == True:
            if not self.health.isDead():
                self.beenHit = True
                self.getHit()
                if self.projectileHit:
                    self.health.loseHealth(damage)
                    self.projectileHit = False
            else:
                self.beenHit = True
                self.death()

    def getHit(self):
        if self.beenHit: 
            frame = self.getHit_states

            totalFrames = len(frame)
            now = pygame.time.get_ticks()

            if now - self.hitUpdate > 150:
                self.hitFrame += 1
                self.hitUpdate = pygame.time.get_ticks()
                if self.hitFrame >= totalFrames:
                    self.beenHit = False
                    self.damaged = False
                    self.hitFrame = 0
                    self.clip(self.right_states[0])
                    self.image = self.sheet.subsurface(self.sheet.get_clip())
                    scaledSize = (100, 100)
                    self.image = pygame.transform.scale(self.image, scaledSize)
                    if not self.facingLeft:
                        self.image = pygame.transform.flip(self.image, True, False)
                    return

            self.sheet.set_clip(pygame.Rect(frame[self.hitFrame]))
            self.image = self.sheet.subsurface(self.sheet.get_clip())
            scaledSize = (100, 100)
            self.image = pygame.transform.scale(self.image, scaledSize)
            if not self.facingLeft:
                self.image = pygame.transform.flip(self.image, True, False)

    def death(self):
        if self.beenHit: 
            frame = self.death_states

            totalFrames = len(frame)
            now = pygame.time.get_ticks()

            if now - self.deathUpdate > 100:
                self.deathFrame += 1
                self.deathUpdate = pygame.time.get_ticks()
                if self.deathFrame >= totalFrames:
                    self.beenHit = False
                    self.damaged = False
                    self.deathFrame = 0
                    self.kill()
                    return

            self.sheet.set_clip(pygame.Rect(frame[self.deathFrame]))
            self.image = self.sheet.subsurface(self.sheet.get_clip())
            scaledSize = (100, 100)
            self.image = pygame.transform.scale(self.image, scaledSize)
            if not self.facingLeft:
                self.image = pygame.transform.flip(self.image, True, False)