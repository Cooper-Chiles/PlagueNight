Milestone 2

Cooper Chiles
    - Created the PlagueNight module which runs the main game loop for PlagueNight
        - The module establishes all information necessary for the screen
        - It runs the game loop using the playerController and stageController to manage the player and the stage 

    - Created the playerController module which handles player input to control the movement and actions that a player can do
        - The playerController draws the players health and their potions
        - The playerController also checks for player collisions

    - Created the stageController module which handles creating and updating the stages entities and environment
        - The stageController can draw the stage and update it 
        - The stageController can add enemies and potions to the environment

    - Created the background module for creating the stage background and ground
        - The background creates and adjusts the scenes
        - The background draws the background and ground and makes the background scroll

    - Created the ground module for creating and storing the ground tiles
        - It contains the ground and groundTile classes in the module
        - The ground can be drawn and can scroll with the screen

    - Created the player module for creating, updating and handling player movement and actions
        - The module handles checking player collisions with floors, walls and platforms
        - The module handles all player actions such as healing, jumping, moving, attacking, and interacting

    - Created the pHealth module to store and manage the health for the player character
        - The health can be drawn in the top left corner
        - The health can be gained and removed

    - Created the pHealthPotion module to store and manage the healthPotions held by the player character
        - The healthPotions can be drawn in the top left corner under the health
        - The healthPotions can increase when picked up and decrease when used

    - Created the potionProjectile module to create and manage the potions that are thrown
        - The potionProjectile can be draw and updated
        - The potionProjectile can check if its hit the ground or an enemy

    - Created the healthPotionItem module to create and manage the healthPotions that are placed in the environment
        - The healthPotion can be draw and updated
        - The player can interact with the healthPotion

    - Created the zombie module for creating and updating zombie movement and actions
        - The zombies can have different colors and can be on the ground
        - The zombies can chase a player that enters a certain range around them this can reactivate even while returning
        - The zombies can patrol an area and return to patrolling after chasing a player
        - The zombies can take damage from a player and die 

    - Created the eHealth module to store and manage the health for the enemy character
        - The health can be removed and the enemy can die

    - Created the platforms module
    - Created the walls module

milestone 3

Cooper Chiles
    - Created the menu module

    - Created the foreground module
        - Added the ability to randomly draw different trees at different levels of foreground
        - Added the ability to draw the trees across the screen

    - Created the projectileExplosion module
        - Update the ability to create explosions when the potion projectiles break
        - Update the explosion when projectiles land against the ground or a zombie

    - Updated the player module
        - Updated the handling of player interacting with walls, floors, and platforms
        - Updated the player healing and taking damage animations
        - Updated the player death animation
        - Updated the player throwing potion projectiles

    - Updated the zombie module
        - Updated the handling of the zombie interacting with walls and floors
        - Updated the use of the update, detectplayer and checkwallcollision functions

    - Updated the platforms module
        - Updated the ability to create a platform
        - Updated the ability to draw a platform

    - Updated the walls module
        - Updated the ability to create walls 
        - Updated the ability to draw walls

    - Updated the stageController module
        - Added the draw foreground function to draw everything in the foreground and move them

    - Updated the playerController module
        - Updated the player actions and the check collisions functions
        - Added player flashes while invulnerable after taking damage

    - Updated the ground module
        - Updated the ability to create rocks, dirt, ground and walls
        - Updated the ability to draw rocks, dirt, and ground