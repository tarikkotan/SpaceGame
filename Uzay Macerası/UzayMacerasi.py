import os
import pygame
import pygame_menu
import pygame
import random
import math
from pygame import mixer

pygame.init()
os.environ['SDL_VIDEO_CENTERED'] = '1'
surface = pygame.display.set_mode((800, 600))


def set_difficulty(selected, value):
    """
    Set the difficulty of the game.
    """
    print('Set difficulty to {} ({})'.format(selected[0], value))


def start_the_game():
    screen = pygame.display.set_mode((800,600))

    #Background
    background = pygame.image.load("background.png")

    #Background Sound
    mixer.music.load("background.wav")
    mixer.music.play(-1)

    #Title and Icon
    pygame.display.set_caption("Uzay Macerası")
    icon = pygame.image.load("radiation.png")
    pygame.display.set_icon(icon)


    #Player
    playerImg = pygame.image.load("spaceship.png")
    playerX = 370
    playerY = 480
    playerX_change = 0

    #Enemy 
    enemyImg = []
    enemyX = []
    enemyY = []
    enemyX_change = []
    enemyY_change = []
    num_of_enemies = 8

    for i in range(num_of_enemies):
        enemyImg.append(pygame.image.load("ufo.png"))
        enemyX.append(random.randint(0,735))
        enemyY.append(random.randint(50,150))
        enemyX_change.append(2)
        enemyY_change.append(40)

    # Missile

    # Ready - You can't see the bullet on the screen
    # Fire - The bullet is currently moving
    missileImg = pygame.image.load("missile.png")
    missileX = 0
    missileY = 480
    missileX_change = 0
    missileY_change = 15
    missile_state = "ready"

    # Font
    score_value = 0
    font = pygame.font.Font("game_over.ttf",64)

    textX= 10
    textY = 10

    #Game Over Text
    over_font = pygame.font.Font("game_over.ttf",128)

    def show_score(x,y):
        score = font.render("Score :"+ str(score_value),True,(255,255,255))
        screen.blit(score,(x,y))

    def game_over_text():
        over_text = over_font.render("GAME OVER",True,(255,255,255))
        screen.blit(over_text,(250,250))



    def player(x,y):
        screen.blit(playerImg,(x,y))

    def enemy(x,y,i):
        screen.blit(enemyImg[i],(x,y))

    def fire_missile(x,y):
        nonlocal missile_state
        missile_state = "fire" 
        screen.blit(missileImg,(x+16,y+10))

    def isCollision(enemyX,enemyY,missileX,missileY):
        distance = math.sqrt((math.pow(enemyX-missileX,2))+(math.pow(enemyY-missileY,2)))

        if distance <27:
            return True
        else:
            return False

    # Game Loop
    running = True
    while running:
        #RGB - Red,Green,Blue
        screen.fill((0,0,0))
        #Background Image
        screen.blit(background,(0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # if keystroke is pressed check whether its right or left
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerX_change = -4
                if event.key == pygame.K_RIGHT:
                    playerX_change = 4
                if event.key == pygame.K_SPACE:
                    if missile_state == "ready":
                        missile_Sound = mixer.Sound("fire.wav")
                        missile_Sound.play()
                        missileX = playerX
                        fire_missile(missileX,missileY)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0

        # Spacehip bounds
        playerX += playerX_change

        if playerX <=0:
            playerX = 0
        elif playerX >= 736:
            playerX = 736
        
        # Enemy Movement
        for i in range(num_of_enemies):

            #Game Over
            if enemyY[i] > 400:
                for j  in range(num_of_enemies):
                    enemyY[j] = 2000
                game_over_text()
                break

            enemyX[i] += enemyX_change[i]

            if enemyX[i] <=0:
                enemyX_change[i] = 2
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 736:
                enemyX_change[i] = -2
                enemyY[i] += enemyY_change[i]
            
            
            # Collision
            collision = isCollision(enemyX[i],enemyY[i],missileX,missileY)
            if collision:
                explosion_Sound = mixer.Sound("explosion.wav")
                explosion_Sound.play()
                missileY = 480
                missile_state ="ready"
                score_value += 1
                enemyX[i] = random.randint(0,735)
                enemyY[i] = random.randint(50,150)
            
            enemy(enemyX[i],enemyY[i],i)

        # Missile Movement
        if missileY <=0:
            missileY = 480
            missile_state = "ready"
        if missile_state == "fire":
            fire_missile(missileX,missileY)
            missileY -= missileY_change

            
        player(playerX,playerY)
        show_score(textX,textY)
        pygame.display.update()


menu = pygame_menu.Menu(height=300,
                        width=400,
                        theme=pygame_menu.themes.THEME_BLUE,
                        title='Welcome')


menu.add_button('Play', start_the_game)
menu.add_button('Quit', pygame_menu.events.EXIT)

if __name__ == '__main__':
    menu.mainloop(surface)