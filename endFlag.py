import pygame

class EndFlag(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y

        self.sheet = pygame.image.load('Images/flag.png').convert()
        self.sheet.set_colorkey((255, 255, 255))

        self.sheet.set_clip(pygame.Rect(4, 7, 34, 52))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

        self.flag_states= {0: (4, 7, 34, 52), 1: (64, 7, 34, 52), 2: (124, 7, 34, 52), 3: (244, 7, 34, 52), 4: (4, 7, 34, 52)}

        self.interacted = False
        self.frame = 0
        self.counter = 0

    def get_frame(self, frame_set):  # Get the next frame in the given frame set (animation loop).
        # Increment the frame counter.
        self.frame += 1
        
        # Loop back to the first frame if the counter exceeds the number of frames.
        if self.frame > (len(frame_set) - 1):
            self.frame = 0
        
        #print(frame_set[self.frame])  # Debugging: print the current frame's rectangle.
        return frame_set[self.frame]  #
    
    def clip(self, clipped_rect):  # Set the clipping region (current frame) based on a provided rectangle.
        if type(clipped_rect) is dict:  # If the clipped rect is a dictionary (animation set), get the next frame.
            self.sheet.set_clip(pygame.Rect(self.get_frame(clipped_rect)))
        else:
            # Set the clipping area directly if it's a specific rectangle.
            self.sheet.set_clip(pygame.Rect(clipped_rect))
        return clipped_rect  # R

    def update(self):
        self.counter += 1
        if self.counter >= 4:
            self.counter = 0
            self.clip(self.flag_states)
            self.image = self.sheet.subsurface(self.sheet.get_clip())

    def draw(self, screen, scroll):
        if not self.interacted:
            x = self.x - scroll 
            self.rect.topleft = (x, self.y)
            screen.blit(self.image, (x, self.y))
    
    def interact(self):
        if not self.interacted:
            self.interacted = True