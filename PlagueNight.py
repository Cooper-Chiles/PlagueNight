import os, pygame, stageController, playerController, menu
os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()

# Master timing
clock = pygame.time.Clock()
FPS = 60  # target frames per second

# Logical render size
SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 500

MENU_WIDTH = 800
MENU_HEIGHT = 400

GAMESCREENX = SCREEN_WIDTH * 4
GAMESCREENY = SCREEN_HEIGHT * 2

VERTICAL_MARGIN = 150
HORIZONTAL_MARGIN = 400

lScreenEdge = 0
rScreenEdge = SCREEN_WIDTH

menu = menu.Menu(MENU_WIDTH, MENU_HEIGHT)
runMenu = True
screen = pygame.display.set_mode((MENU_WIDTH, MENU_HEIGHT))
while runMenu:
    pygame.display.set_caption("Plague Night")
    choice = menu.menuLoop(screen, "menu")
    runGame = True
    if choice == "Quit":
        runGame = False
        runMenu = False
    lScreenEdge = 0
    rScreenEdge = SCREEN_WIDTH

    stageCon = stageController.StageControl(SCREEN_WIDTH, SCREEN_HEIGHT)
    playerCon = playerController.PlayerControl(0, 385)
    stageCon.addZombies()
    stageCon.addPotions()
    stageCon.addCrystals()
    stageCon.addFlag()

    stage = 0
    scroll = 0
    pScrollSpeed = 8

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    while runGame:
        
        clock.tick(FPS)

        screen.fill((0, 0, 0))
        if playerCon.player.lifeState == "alive":
            winRequirements = playerCon.checkWin()
            if not winRequirements: 
                stageCon.bgDraw(scroll, screen, lScreenEdge)
 
                healthPotions = stageCon.getHealthPotions()
                zombieGroup = stageCon.getZombies()
                crystalGroup = stageCon.getCrystals()
                flagGroup = stageCon.getFlags()
                groundGroup = stageCon.getGround()
                wallGroup = stageCon.getWalls()
                wallTopGroup = stageCon.getWallTop()
                platformGroup = stageCon.getPlatforms()
                platformWallGroup = stageCon.getPlatformWalls()
              
                key = pygame.key.get_pressed()
                scroll, lScreenEdge, rScreenEdge = playerCon.playerMovement(key, scroll, pScrollSpeed, lScreenEdge, rScreenEdge, SCREEN_WIDTH, GAMESCREENX, HORIZONTAL_MARGIN)
                playerCon.playerActions(screen, lScreenEdge, SCREEN_WIDTH, healthPotions, crystalGroup, flagGroup, groundGroup, zombieGroup, wallGroup, wallTopGroup)

                playerCon.checkCollisions(wallTopGroup, wallGroup, groundGroup, platformWallGroup, platformGroup, screen, healthPotions, crystalGroup, flagGroup, lScreenEdge, SCREEN_WIDTH, SCREEN_HEIGHT)

                stageCon.updateZombies(playerCon.player, screen, lScreenEdge, SCREEN_WIDTH, SCREEN_HEIGHT)
                playerCon.checkExplosions(screen)
                stageCon.bgDrawOverlays(screen)
                stageCon.updatePotions(screen, lScreenEdge)
                stageCon.updateCrystals(screen, lScreenEdge)
                stageCon.updateFlag(screen, lScreenEdge)
                stageCon.fgDraw(GAMESCREENX, scroll, screen)
                playerCon.drawPlayerInfo(screen)
            else:
                runGame = False
                screen = pygame.display.set_mode((MENU_WIDTH, MENU_HEIGHT))
                pygame.display.set_caption("Plague Night")
                choice = menu.menuLoop(screen, "win")
                if choice == "Quit":
                    runMenu = False
        else:
            runGame = False
            screen = pygame.display.set_mode((MENU_WIDTH, MENU_HEIGHT))
            pygame.display.set_caption("Plague Night")
            choice = menu.menuLoop(screen, "loss")
            if choice == "Quit":
                runMenu = False


        pygame.display.update()

pygame.quit()