import pygame, time, pHealth, pHealthPotion, pCrystals, pFlags, potionProjectile  # Import the pygame library to use its functionalities for 2D graphics and sound.

class Character(pygame.sprite.Sprite):  # Define a class `Character` that inherits from pygame's `Sprite` class.
    def __init__(self, position):  # Initialize the character object with a starting position.
     
        # Load the image file (spritesheet) into the `sheet` attribute.
        self.sheet = pygame.image.load('Sprites/PlagueKnightSpritesheet.png').convert()
        self.sheet.set_colorkey((0, 255, 0))
        # Define the area of a single sprite within the sheet (first sprite clip).
        self.sheet.set_clip(pygame.Rect(2, 2, 31, 31))
        
        # Get the clipped image (current sprite frame) and set it as the current image of the sprite.
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        scaledSize = (64, 64)
        self.image = pygame.transform.scale(self.image, scaledSize)
        # Get the rectangle of the current sprite image for positioning on the screen.
        self.rect = self.image.get_rect()
        
        # Set the top-left position of the sprite on the screen using the position parameter.
        self.rect.topleft = position
        self.hitbox = self.rect.inflate(-15, -15)
        self.savedX = self.rect.x
        self.savedY = self.rect.y
        self.prevbottom = 0
        self.prevtop = 0
        self.lastFloor = 0
        # Initialize a frame counter for cycling through the frames (animations).
        self.frame = 0
        
        sheetWidth = self.sheet.get_width()
        # Define the coordinates of each animation frame in the spritesheet for different directions.
        self.right_states = {0: (2, 2, 31, 31), 1: (2, 36, 34, 35), 2: (40, 36, 34, 35), 3: (78, 36, 34, 35), 4: (116, 36, 34, 35), 5: (154, 36, 34, 35), 6: (192, 36, 34, 35)}
        self.left_states = {0: (2, 2, 31, 31), 1: (2, 36, 34, 35), 2: (40, 36, 34, 35), 3: (78, 36, 34, 35), 4: (116, 36, 34, 35), 5: (154, 36, 34, 35), 6: (192, 36, 34, 35)} 
        self.jump1_states = {0: (2, 73, 32, 36)}
        self.jump2_states = {0: (2, 188, 35, 34), 1: (2, 152, 20, 34)}
        self.down_states = {0: (2, 111, 47, 39)}
        self.heal_states = {0: (2, 2518, 24, 30)}
        self.standingAttack_states = {0: (2, 327, 45, 37), 1: (49, 327, 45, 37), 2: (96, 327, 45, 37), 3: (143, 327, 45, 37), 4: (190, 327, 45, 37)}
        self.jumpAttack_states = {0: (2, 366, 46, 39), 1: (50, 366, 46, 39), 2: (98, 366, 46, 39), 3: (146, 366, 46, 39), 4: (194, 366, 46, 39)}
        self.damageBoost_states = {0: (2, 1488, 39, 37), 1: (43, 1488, 39, 37), 2: (84, 1488, 39, 37), 3: (125, 1488, 39, 37), 4: (166, 1488, 39, 37), 5: (207, 1488, 39, 37), 6: (248, 1488, 39, 37), 7: (289, 1488, 39, 37), 8: (330, 1488, 39, 37), 9: (371, 1488, 39, 37), 10: (412, 1488, 39, 37), 11: (453, 1488, 39, 37), 12: (494, 1488, 39, 37), 13: (535, 1488, 39, 37), 14: (576, 1488, 39, 37), 15: (617, 1488, 39, 37), 16: (658, 1488, 39, 37), 17: (699, 1488, 39, 37), 18: (740, 1488, 39, 37), 19: (781, 1488, 39, 37),}
        self.getHit_states = {0: (2, 475, 43, 34)}
        self.death_states = {0: (2, 2143, 48, 37), 1: (152, 2143, 48, 37), 2: (52, 2143, 48, 37), 3: (102, 2143, 48, 37)}
        self.win_states = {0: (2, 11, 37, 44), 1: (41, 511, 37, 44), 2: (80, 511, 37, 44), 3: (119, 511, 37, 44), 4: (158, 511, 37, 44), 5: (197, 511, 37, 44), 6: (236, 511, 37, 44), 7: (275, 511, 37, 44), 8: (314, 511, 37, 44), 9: (353, 511, 37, 44), 10: (392, 511, 37, 44), 11: (431, 511, 37, 44)}

        self.health = pHealth.PlayerHealth(5, 10, 10)
        self.potions = pHealthPotion.HealthPotions(3, 60, 45)
        self.crystals = pCrystals.PlayerCrystals(60, 80)
        self.flags = pFlags.PlayerFlag(60, 140)

        self.font = pygame.font.Font(None, 15)
        self.clock = pygame.time.Clock()

        self.lifeState = "alive"
        self.state = "idle"
        self.dx = 0
        self.stateStart = 0
        self.stateDuration = 250
        self.invulnerableDuration = 1000
        self.invulnerable = False
        self.flashStart = 0
        self.flashInterval = 100
        self.flashing = False
        self.maxJumps = 2
        self.currentJump = 0
        self.downVelocity = 1
        self.vy = 0
        self.upVelocity = -10
        self.onGround = True
        self.onPlatform = False
        self.goingUp = False
        self.inAir = False
        self.jumping = False
        self.landed = False
        self.jumpTime = 0
        self.jumpDelay = 50
        self.fallDelay = 200
        self.facingLeft = False
        self.visualFacingLeft = False
        self.worldPos = 0
        self.outputDamage = 1
        self.beenHit = False
        self.deathFrame = 0
        self.deathUpdate = 0
        self.isAttacking = False
        self.attackRelease = False
        self.attackCharging = False
        self.chargeStart = 0
        self.chargeAmt = 0
        self.minCharge = 100
        self.maxCharge = 500
        self.attackStart = 0
        self.attackFrame = 0
        self.betweenAttacks = 500
        self.boosted = False
        self.boosting = False
        self.boostFrame = 0
        self.boostStart = 0
        self.boostFrameTime = 100
        self.boostDurStart = 0
        self.boostDuration = 10000
        self.thrownPotion = False
        self.thrownPotions = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()

    def get_frame(self, frame_set):  # Get the next frame in the given frame set (animation loop).
        # Increment the frame counter.
        self.frame += 1
        
        # Loop back to the first frame if the counter exceeds the number of frames.
        if self.frame > (len(frame_set) - 1):
            self.frame = 0
        
        #print(frame_set[self.frame])  # Debugging: print the current frame's rectangle.
        return frame_set[self.frame]  # Return the rectangle of the current frame.

    def clip(self, clipped_rect):  # Set the clipping region (current frame) based on a provided rectangle.
        if type(clipped_rect) is dict:  # If the clipped rect is a dictionary (animation set), get the next frame.
            self.sheet.set_clip(pygame.Rect(self.get_frame(clipped_rect)))
        else:
            # Set the clipping area directly if it's a specific rectangle.
            self.sheet.set_clip(pygame.Rect(clipped_rect))
        return clipped_rect  # Return the clipped rectangle.

    def update(self, direction):  # Update the character's position and animation based on the direction.
        self.clock.tick(20)
        self.prevbottom = self.rect.bottom
        self.prevtop = self.rect.top
        if self.state in ["hit", "heal", "boost", "dead"]:
            return

        if direction == 'left':  # Move left and play left walking animation.
            self.facingLeft = True
            self.state = "moving"
            if self.onGround:
                self.clip(self.left_states)
            elif self.currentJump < self.maxJumps:
                self.clip(self.jump1_states)
            elif self.currentJump == self.maxJumps:
                self.clip(self.jump2_states[1])
            self.dx = -8
            self.rect.x -= 8 # Move the sprite left by 5 pixels.
            self.worldPos -= 8
        if direction == 'right':  # Move right and play right walking animation.
            self.facingLeft = False
            self.state = "moving"
            if self.onGround:
                self.clip(self.right_states)
            elif self.currentJump < self.maxJumps:
                self.clip(self.jump1_states)
            elif self.currentJump == self.maxJumps:
                self.clip(self.jump2_states[1])
            self.dx = 8
            self.rect.x += 8
            self.worldPos += 8
        if direction == 'up':  # Move up and play up walking animation.
            #self.rect.y -= 7
            self.jump()
        if direction == 'down':  # Move down and play down walking animation.
            self.clip(self.down_states)
            #self.rect.y += 5

        # Standing still animations (no movement, just switching frames to standing).
        if direction == 'stand_left':
            self.facingLeft = True
            self.state = "idle"
            self.clip(self.left_states[0])
        if direction == 'stand_right':
            self.facingLeft = False
            self.state = "idle"
            self.clip(self.right_states[0])
        if direction == 'stand_up':
            self.clip(self.up_states[0])
        if direction == 'stand_down':
            self.clip(self.down_states[0])

        # Update the image with the current clipped frame.
        self.hitbox.center = self.rect.center
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.scaleImages()
        if self.facingLeft:
            self.image = pygame.transform.flip(self.image, True, False)

    def handle_event(self, event):  # Handle keyboard events to move the character or stop movement.
        if event.type == pygame.KEYDOWN:  # If a key is pressed down:
            if event.key == pygame.K_LEFT:  # Move left if the left arrow is pressed.
                self.update('left')
            if event.key == pygame.K_RIGHT:  # Move right if the right arrow is pressed.
                self.update('right')
            if event.key == pygame.K_UP:  # Move up if the up arrow is pressed.
                self.update('up')
            if event.key == pygame.K_DOWN:  # Move down if the down arrow is pressed.
                self.update('down')

        if event.type == pygame.KEYUP:  # If a key is released (stop movement):
            if event.key == pygame.K_LEFT:  # Stop and stand facing left.
                self.update('stand_left')
            if event.key == pygame.K_RIGHT:  # Stop and stand facing right.
                self.update('stand_right')
            if event.key == pygame.K_UP:  # Stop and stand facing up.
                self.update('stand_up')
            if event.key == pygame.K_DOWN:  # Stop and stand facing down.
                self.update('stand_down')

    def updateState(self):
        if self.state == "dead":
            self.updateDeath()
            return

        now = pygame.time.get_ticks()
        if self.state in ["hit", "heal"]:
            if now - self.stateStart > self.stateDuration:
                self.state = "idle"
                self.clip(self.right_states[0])
                self.image = self.sheet.subsurface(self.sheet.get_clip())
                self.scaleImages()
                if self.facingLeft:
                    self.image = pygame.transform.flip(self.image, True, False)

        if self.invulnerable:
            if now - self.flashStart > self.flashInterval:
                self.flashing = not self.flashing
                self.flashStart = now

            if now - self.stateStart > self.invulnerableDuration:
                self.invulnerable = False
                self.flashing = False

    def scaleImages(self):
        w, h = self.image.get_size()
        scaleFactor = 64 / h
        scaledSize = (int(w * scaleFactor), 64)
        self.image = pygame.transform.scale(self.image, scaledSize)

    def jump(self):
        if self.currentJump < self.maxJumps:
            if self.currentJump == 0:
                self.clip(self.jump1_states)
            else:
                self.clip(self.jump2_states[0])
            self.currentJump += 1
            self.vy = self.upVelocity
        self.jumping = True
        self.onGround = False
        self.goingUp = True
        self.inAir = True
        self.landed = False
        if self.facingLeft:
            self.image = pygame.transform.flip(self.image, True, False)

    def jumpLanding(self, walltops, floors, platforms, lScreenEdge):
        if not self.landed:
            for floor in floors:
                shiftedFloor = pygame.Rect(floor.rect.x - lScreenEdge, floor.rect.y, floor.rect.width, floor.rect.height)
                if self.rect.colliderect(shiftedFloor):
                    if self.vy > 0:
                        self.rect.bottom = shiftedFloor.top
                        self.vy = 0
                        self.rect.y += self.downVelocity
                        self.onGround = True
                        self.inAir = False
                        self.jumping = False
                        self.goingUp = False
                        self.landed = True
                        self.currentJump = 0
                        self.clip(self.right_states[0])
                        self.image = self.sheet.subsurface(self.sheet.get_clip())
                        self.scaleImages()
                        if self.facingLeft:
                            self.image = pygame.transform.flip(self.image, True, False)

            for walltop in walltops:
                shiftedWalltop = pygame.Rect(walltop.rect.x - lScreenEdge, walltop.rect.y, walltop.rect.width, walltop.rect.height)
                if self.rect.colliderect(shiftedWalltop):
                    if self.vy > 0:
                        self.rect.bottom = shiftedWalltop.top
                        self.vy = 0
                        self.rect.y += self.downVelocity
                        self.onGround = True
                        self.inAir = False
                        self.jumping = False
                        self.goingUp = False
                        self.landed = True
                        self.currentJump = 0
                        self.clip(self.right_states[0])
                        self.image = self.sheet.subsurface(self.sheet.get_clip())
                        self.scaleImages()
                        if self.facingLeft:
                            self.image = pygame.transform.flip(self.image, True, False)

            for plat in platforms:
                shiftedPlatform = pygame.Rect(plat.rect.x - lScreenEdge, plat.rect.y, plat.rect.width, plat.rect.height)
                if self.rect.colliderect(shiftedPlatform) and self.prevbottom <= shiftedPlatform.top + 1 and self.rect.bottom >= shiftedPlatform.top + 1:
                    if self.vy > 0:
                        self.rect.bottom = shiftedPlatform.top
                        self.vy = 0
                        self.rect.y += self.downVelocity
                        self.onGround = True
                        self.inAir = False
                        self.jumping = False
                        self.goingUp = False
                        self.landed = True
                        self.currentJump = 0
                        self.clip(self.right_states[0])
                        self.image = self.sheet.subsurface(self.sheet.get_clip())
                        self.scaleImages()
                        if self.facingLeft:
                            self.image = pygame.transform.flip(self.image, True, False)
                platList = platforms.sprites()
                if not plat == platList[-1]:
                    if self.rect.colliderect(shiftedPlatform) and self.rect.top <= shiftedPlatform.bottom and self.vy < 0:
                        self.rect.top = shiftedPlatform.bottom
                        self.vy = 0
                        self.goingUp = False

    def checkCollisionFloor(self, walltops, floors, platforms, lScreenEdge):
        self.onGround = False
        for floor in floors:
            shiftedFloor = pygame.Rect(floor.rect.x - lScreenEdge, floor.rect.y, floor.rect.width, floor.rect.height)
            if self.rect.colliderect(shiftedFloor) and self.rect.bottom <= shiftedFloor.top + 1:
                self.onGround = True
                self.lastFloor = floor
                self.savedX = self.lastFloor.rect.centerx
                self.savedY = self.rect.y
            
        for walltop in walltops:
            shiftedWalltop = pygame.Rect(walltop.rect.x - lScreenEdge, walltop.rect.y, walltop.rect.width, walltop.rect.height)
            if self.rect.colliderect(shiftedWalltop) and self.rect.bottom <= shiftedWalltop.top + 1:                
                self.onGround = True
                self.lastFloor = walltop
                self.savedX = self.lastFloor.rect.centerx
                self.savedY = self.rect.y 

        for plat in platforms:
                shiftedPlatform = pygame.Rect(plat.rect.x - lScreenEdge, plat.rect.y, plat.rect.width, plat.rect.height)
                if self.rect.colliderect(shiftedPlatform) and self.rect.bottom <= shiftedPlatform.top + 1:
                    self.onGround = True
                    self.lastFloor = plat
                    self.savedX = self.lastFloor.rect.centerx
                    self.savedY = self.rect.y 

    def checkCollisionWall(self, walls, pwalls, lScreenEdge):
        collidedWall = False

        for wall in walls:
            for tile in wall:
                shiftedWall = pygame.Rect(tile.rect.x - lScreenEdge, tile.rect.y, tile.rect.width, tile.rect.height)
                if not collidedWall:
                    if self.rect.colliderect(shiftedWall):
                        if self.facingLeft and self.dx < 0:
                            self.rect.left = shiftedWall.right
                            self.visualFacingLeft = False
                        elif not self.facingLeft and self.dx > 0:
                            self.rect.right = shiftedWall.left
                            self.visualFacingLeft = True

                        self.clip(self.right_states[0])
                        self.image = self.sheet.subsurface(self.sheet.get_clip())
                        self.scaleImages()
                        if not self.facingLeft:
                            self.image = pygame.transform.flip(self.image, True, False)
                        
                        self.facingLeft = not self.facingLeft
                        collidedWall = True
                        return 

        for wall in pwalls:
            for tile in wall:
                shiftedWall = pygame.Rect(tile.rect.x - lScreenEdge, tile.rect.y, tile.rect.width, tile.rect.height)
                if not collidedWall:
                    if self.rect.colliderect(shiftedWall):
                        if self.hitbox.top < shiftedWall.bottom - 4:
                            if self.facingLeft and self.dx < 0:
                                self.rect.left = shiftedWall.right
                                self.visualFacingLeft = False
                            elif not self.facingLeft and self.dx > 0:
                                self.rect.right = shiftedWall.left
                                self.visualFacingLeft = True

                            self.clip(self.right_states[0])
                            self.image = self.sheet.subsurface(self.sheet.get_clip())
                            self.scaleImages()
                            if not self.facingLeft:
                                self.image = pygame.transform.flip(self.image, True, False)
                            
                            self.facingLeft = not self.facingLeft
                            collidedWall = True
                            return 

        if not collidedWall:
            self.visualFacingLeft = self.facingLeft

    def gravity(self, lScreenEdge, SCREEN_HEIGHT):
        if not self.onGround:
            self.vy += self.downVelocity
            self.rect.y += self.vy
            self.landed = False

        now = pygame.time.get_ticks()

        if self.vy < 0:
            if self.currentJump == 2 and now - self.jumpTime > self.jumpDelay:
                self.clip(self.jump2_states[1])
            else:
                self.clip(self.jump1_states)
        elif self.vy > 0:
            self.clip(self.down_states)

        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.scaleImages()
        if self.facingLeft:
            self.image = pygame.transform.flip(self.image, True, False)

        if self.rect.top > SCREEN_HEIGHT:
            self.takeDamage(1)
            self.rect.centerx = self.savedX - lScreenEdge
            self.rect.y = self.savedY
            self.landed = False
            self.vy = 0

        self.hitbox.center = self.rect.center

    def heal(self, health):
        if self.health.currentHealth < self.health.maxHealth and self.potions.currentPotionCount > 0:
            self.state = "heal"
            self.stateStart = pygame.time.get_ticks()
            self.clip(self.heal_states)
            self.image = self.sheet.subsurface(self.sheet.get_clip())
            self.scaleImages()
            self.health.gainHealth(health)
            self.potions.usePotion()

    def printDamageBoost(self, screen):
        if (self.boostDuration - (pygame.time.get_ticks() - self.boostDurStart)) / 1000 > 0:
            font = pygame.font.Font(None, 40)
            self.boost = self.font.render(f"DamageBoosted time remaining: {((self.boostDuration - (pygame.time.get_ticks() - self.boostDurStart)) / 1000):.2f}s", True, (0, 206, 200))
            screen.blit(self.boost, (250, 10))
        else:
            self.boosted = False
            self.updateDamage("nerf")

    def damageBoost(self):
        if self.crystals.currentCrystalCount >= self.crystals.crystalAmtForBoost:
            self.state = "boost"
            self.boosting = True
            self.updateDamage("boost")
            self.stateStart = pygame.time.get_ticks()
            self.clip(self.damageBoost_states)
            self.image = self.sheet.subsurface(self.sheet.get_clip())
            self.scaleImages()
            if self.facingLeft:
                self.image = pygame.transform.flip(self.image, True, False)
            self.crystals.useCrystals()

    def updateBoost(self):
        if self.boosting:
            frame = self.damageBoost_states
            totalFrames = len(frame)
            now = pygame.time.get_ticks()

            if now - self.boostStart > self.boostFrameTime:
                self.boostFrame += 1
                self.boostStart = now
                if self.boostFrame >= totalFrames:
                    self.boosting = False
                    self.state = "idle"
                    self.boosted = True
                    self.boostDurStart = pygame.time.get_ticks()
                    self.boostFrame = 0
                    self.clip(self.right_states[0])
                    self.image = self.sheet.subsurface(self.sheet.get_clip())
                    self.scaleImages()
                    if self.facingLeft:
                        self.image = pygame.transform.flip(self.image, True, False)
                    return

            self.sheet.set_clip(pygame.Rect(frame[self.boostFrame]))
            self.image = self.sheet.subsurface(self.sheet.get_clip())
            self.scaleImages()
            if self.facingLeft:
                self.image = pygame.transform.flip(self.image, True, False)
    
    def attack(self):
        now = pygame.time.get_ticks()

        if not self.isAttacking and now - self.attackStart > self.betweenAttacks:
            self.isAttacking = True
            self.attackCharging = True
            self.chargeStart = now
            self.attackFrame = 0
            self.attackStart = now

    def updateAttack(self):
        if self.isAttacking:
            if self.onGround:
                frame = self.standingAttack_states
            else:
                frame = self.jumpAttack_states

            totalFrames = len(frame)
            now = pygame.time.get_ticks()

            if now - self.attackStart > 100:
                if self.attackCharging:
                    if self.attackFrame < 1:
                        self.attackFrame += 1
                        self.attackStart = now
                else:
                    self.attackFrame += 1
                    self.attackStart = now
                if self.attackFrame >= totalFrames:
                    self.isAttacking = False
                    self.attackFrame = 0
                    self.thrownPotion = False
                    self.clip(self.right_states[0])
                    self.image = self.sheet.subsurface(self.sheet.get_clip())
                    self.scaleImages()
                    if self.facingLeft:
                        self.image = pygame.transform.flip(self.image, True, False)
                    return

            self.sheet.set_clip(pygame.Rect(frame[self.attackFrame]))
            self.image = self.sheet.subsurface(self.sheet.get_clip())
            self.scaleImages()
            if self.facingLeft:
                self.image = pygame.transform.flip(self.image, True, False)

            facingL = False

            if self.attackFrame == 3 and self.attackRelease and not self.thrownPotion:
                if self.visualFacingLeft == self.facingLeft:
                    facingL = self.facingLeft
                    if self.facingLeft:
                        potionX = self.rect.x 
                    else:
                        potionX = self.rect.x + self.rect.width
                else:
                    facingL = self.visualFacingLeft
                    if not self.facingLeft:
                        potionX = self.rect.x 
                    else:
                        potionX = self.rect.x + self.rect.width
                
                charge = max(self.minCharge, min(self.chargeAmt, self.maxCharge))
                power = charge/self.maxCharge
                    
                potionY = self.rect.centery
                potion = potionProjectile.ThrowPotion(potionX, potionY, facingL, power)
                if self.thrownPotion == False:
                    self.thrownPotions.add(potion)
                    self.thrownPotion = True         

    def interactableItems(self, screen, potions, crystals, flags, scroll):
        for potion in potions:
            if not potion.interacted:
                if (self.rect.colliderect(potion.hitbox)):
                    self.potionInteract = self.font.render(f"C", True, (0, 255, 0))
                    screen.blit(self.potionInteract, ((potion.rect.centerx), potion.y - (15)))

        for crystal in crystals:
            if not crystal.interacted:
                if (self.rect.colliderect(crystal.rect)):
                    self.crystalInteract = self.font.render(f"C", True, (0, 255, 0))
                    screen.blit(self.crystalInteract, ((crystal.rect.centerx), crystal.y - (15)))

        for flag in flags:
            if not flag.interacted:
                if (self.rect.colliderect(flag.rect)):
                    self.flagInteract = self.font.render(f"C", True, (0, 255, 0))
                    screen.blit(self.flagInteract, ((flag.rect.centerx), flag.y - (15)))
    
    def interactItems(self, potions, crystals, flags, scroll):
        if self.potions.currentPotionCount < self.potions.maxPotionCount:
            for potion in potions:
                if not potion.interacted:
                    if (self.rect.colliderect(potion.hitbox)):
                        potion.interact()
                        self.potions.gainPotion()

        for crystal in crystals:
            if not crystal.interacted:
                if (self.rect.colliderect(crystal.rect)):
                    crystal.interact()
                    color = crystal.color
                    self.crystals.gainCrystal(color)

        for flag in flags:
            if not flag.interacted:
                if (self.rect.colliderect(flag.rect)):
                    flag.interact()
                    self.flags.gainFlag()

    def updateDamage(self, modification):
        if modification == "boost":
            self.outputDamage *= 2
        elif modification == "nerf":
            self.outputDamage /= 2

    def takeDamage(self, damage):
        if self.health.currentHealth > self.health.minHealth:
            if not self.invulnerable:
                self.health.loseHealth(damage)
                self.invulnerable = True
                self.state = "hit"
                self.stateStart = pygame.time.get_ticks()
                self.clip(self.getHit_states)
                self.image = self.sheet.subsurface(self.sheet.get_clip())
                self.scaleImages()
                if self.facingLeft:
                    self.image = pygame.transform.flip(self.image, True, False)
        else:
            if not self.invulnerable:
                self.beenHit = True
                self.death()

    def death(self):
        if self.beenHit:
            self.state = "dead"


    def updateDeath(self):
        if self.state != "dead":
            return 

        frame = self.death_states
        totalFrames = len(frame)
        now = pygame.time.get_ticks()

        if now - self.deathUpdate > 100:
            self.deathFrame += 1
            self.deathUpdate = pygame.time.get_ticks()
            if self.deathFrame >= totalFrames:
                self.beenHit = False
                self.deathFrame = 0
                self.lifeState = "dead"
                return

            self.sheet.set_clip(pygame.Rect(frame[self.deathFrame]))
            self.image = self.sheet.subsurface(self.sheet.get_clip())
            self.scaleImages()
            if self.facingLeft:
                self.image = pygame.transform.flip(self.image, True, False)