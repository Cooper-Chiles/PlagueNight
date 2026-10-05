import pygame

class Menu:
    def __init__(self, MENU_WIDTH, MENU_HEIGHT):
        self.menuOptions = ["Start Game", "Quit"]
        self.excessOptions = ["Return to Menu", "Quit"]
        self.selected = 0
        
        self.font = pygame.font.Font(None, 50)
        self.bigFont = pygame.font.Font(None, 70) 
        self.highlight = (0, 255, 0)
        self.default = (255, 255, 255)

        self.width = MENU_WIDTH
        self.height = MENU_HEIGHT
        self.runMenu = True

    def menuLoop(self, screen, position):
        if position == "menu":
            img = pygame.image.load(f"Images/menuScreen.png").convert_alpha()
            self.background = pygame.transform.scale(img, (self.width, self.height))
        elif position == "win":
            img = pygame.image.load(f"Images/winScreen.jpg").convert_alpha()
            self.background = pygame.transform.scale(img, (self.width, self.height))
        elif position == "loss":
            img = pygame.image.load(f"Images/lossScreen.jpg").convert_alpha()
            self.background = pygame.transform.scale(img, (self.width, self.height))

        while self.runMenu:
            screen.fill((0, 0, 0))
            if position == "menu":
                self.displayMenu(screen)
            elif position == "win":
                self.displayWinScreen(screen)
            elif position == "loss":
                self.displayLoseScreen(screen)
            pygame.display.flip()

            selectedChoice = self.menuActions()
            if selectedChoice:
                return selectedChoice

    def displayMenu(self, screen):
        screen.blit(self.background, (0, 0))

        gameName = self.bigFont.render("Plague Night", True, (0, 255, 0))
        gameNameRect = gameName.get_rect(center=(self.width // 2, self.height // 2 - 80))
        screen.blit(gameName, gameNameRect)

        for i, option in enumerate(self.menuOptions):
            if i == self.selected:
                color = self.highlight
            else:
                color = self.default
            menuOption = self.font.render(option, True, color)
            optionRect = menuOption.get_rect(center=(self.width // 2, self.height // 2 + (i * 40)))
            screen.blit(menuOption, optionRect)

    def displayWinScreen(self, screen):
        screen.blit(self.background, (0, 0))
        plagueText = f"You have cleared the plague..."
        newDayText = f"A new day is breaking"
        plaguetext = self.bigFont.render(plagueText, True, (0, 255, 0))
        plaguetextRect = plaguetext.get_rect(center=(self.width // 2, self.height // 2 - 100))
        screen.blit(plaguetext, plaguetextRect)
        newdaytext = self.bigFont.render(newDayText, True, (0, 255, 0))
        newdaytextRect = newdaytext.get_rect(center=(self.width // 2, self.height // 2 - 55))
        screen.blit(newdaytext, newdaytextRect)

        for i, option in enumerate(self.excessOptions):
            if i == self.selected:
                color = self.highlight
            else:
                color = self.default
            winOption = self.font.render(option, True, color)
            optionRect = winOption.get_rect(center=(self.width // 2, self.height // 2 + (i * 40)))
            screen.blit(winOption, optionRect)

    def displayLoseScreen(self, screen):
        screen.blit(self.background, (0, 0))
        plagueText = f"The Plague has won..."
        nightText = f"NIGHT SHALL REIGN"
        plaguetext = self.bigFont.render(plagueText, True, (0, 255, 0))
        plaguetextRect = plaguetext.get_rect(center=(self.width // 2, self.height // 2 - 100))
        screen.blit(plaguetext, plaguetextRect)
        nighttext = self.bigFont.render(nightText, True, (0, 255, 0))
        nighttextRect = nighttext.get_rect(center=(self.width // 2, self.height // 2 - 55))
        screen.blit(nighttext, nighttextRect)
        
        for i, option in enumerate(self.excessOptions):
            if i == self.selected:
                color = self.highlight
            else:
                color = self.default
            loseOption = self.font.render(option, True, color)
            optionRect = loseOption.get_rect(center=(self.width // 2, self.height // 2 + (i * 40)))
            screen.blit(loseOption, optionRect)

    def menuActions(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.runMenu = False
                return "Quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.moveSelection("up")
                elif event.key == pygame.K_DOWN:
                    self.moveSelection("down")
                elif event.key == pygame.K_RETURN:
                    selection = self.getSelection()
                    self.selected = 0
                    return selection

    def moveSelection(self, direction):
        if direction == "up":
            self.selected = (self.selected - 1) % len(self.menuOptions)
        elif direction == "down":
            self.selected = (self.selected + 1) % len(self.menuOptions)

    def getSelection(self):
        return self.menuOptions[self.selected]