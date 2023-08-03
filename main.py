import pygame
from pygame.locals import *
import sys
from random import randint

#biến toàn cục và hằng số (global variables and constants)
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode([SCREEN_WIDTH,SCREEN_HEIGHT])
GAME_IMAGES={}
GAME_SOUNDS={}
FPS = 30

playerX = SCREEN_WIDTH/5
playerY = SCREEN_HEIGHT/2


#Khu chức năng (function area)
def welcomeScreen():
    while True:
        SCREEN.blit(GAME_IMAGES["background"], (0,0))
        SCREEN.blit(GAME_IMAGES["base"], (baseX,baseY))
        SCREEN.blit(GAME_IMAGES["player"], (playerX, playerY))
        SCREEN.blit(GAME_IMAGES["message"],(messageX,messageY))
        pygame.display.update()
        for x in pygame.event.get():
            if x.type == KEYDOWN and x.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if x.type == KEYDOWN and x.key == K_SPACE:
                return

def gameLoop():
    newPipe1 = getRandomPipes()
    newPipe2 = getRandomPipes()
    newPipe3 = getRandomPipes()

    #danh sách các đường ống lên (list of upper pipes)
    upperPipes = [
        {"x":SCREEN_WIDTH, "y":newPipe1[0]["y"]},
        {"x":SCREEN_WIDTH + SCREEN_WIDTH/3, "y":newPipe2[0]["y"]},
        {"x":SCREEN_WIDTH + SCREEN_WIDTH/0.6, "y":newPipe3[0]["y"]},
    ]

    #danh sách các đường ống dưới (list of lower pipes)
    lowerPipes = [
        {"x":SCREEN_WIDTH, "y":newPipe1[1]["y"]},
        {"x":SCREEN_WIDTH + SCREEN_WIDTH/3, "y":newPipe2[1]["y"]},
        {"x":SCREEN_WIDTH + SCREEN_WIDTH/0.6, "y":newPipe3[1]["y"]},
    ]

    score = 0
    high_score = 0
    pipeSpeedX = -7
    playerSpeedX = 10
    playerSpeedY = -9
    playerMaxSpeed = 10
    playerFlyingSpeed = -8
    playerAccY = 1
    playerFlying = False
    pipeHeight = GAME_IMAGES["pipe"][0].get_height()
    playerX = SCREEN_WIDTH/5
    playerY = SCREEN_HEIGHT/2

    while True:
        for x in pygame.event.get():
            if x.type == KEYDOWN and x.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if x.type == KEYDOWN and (x.key == K_SPACE or x.key == K_w):
                if playerY > 0:
                    playerSpeedY = playerFlyingSpeed
                    playerFlying = True
                    #GAME_SOUNDS["fly"].play()

        # di chuyển người chơi lên (moving player up)
        playerY = playerY + playerSpeedY           
        if playerFlying == True:
            playerFlying = False

        # kéo người chơi xuống (pulling player down)
        if playerSpeedY < playerMaxSpeed and not playerFlying:
            playerSpeedY = playerSpeedY + playerAccY

        # di chuyển đường ống (moving the pipes)
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe["x"] = upperPipe["x"] + pipeSpeedX
            lowerPipe["x"] = upperPipe["x"] + pipeSpeedX

        #thêm đường ống mới(adding new pipes)
        if 0 < upperPipes[0]["x"] <= abs(pipeSpeedX):
            newPipe = getRandomPipes()
            upperPipes.append(newPipe[0])
            lowerPipes.append(newPipe[1])
        
        #loại bỏ các đường ống cũ (removing old pipes)
        if upperPipes[0]["x"] < 0:
            upperPipes.pop(0)
            lowerPipes.pop(0)
        
        #thay đổi điểm số (changing the score)
        playerCenterX = playerX + GAME_IMAGES["player"].get_width()/2
        for pipe in upperPipes:
            pipeCenterX = pipe["x"] + GAME_IMAGES["pipe"][0].get_width()/2
            if pipeCenterX <= playerCenterX <pipeCenterX + abs(pipeSpeedX):
                score = score + 1
                GAME_SOUNDS["point"].play()

        # người chơi chết (Player dies)
        if isHit(playerX, playerY, upperPipes, lowerPipes):
            GAME_SOUNDS["die"].play()
            pygame.time.wait(2000)
            #score_surface = game_font.render(f'Score: {int(score)}', True, (255,255,255))
           # score_rect = score_surface.get_rect(center = (216,100))
            #SCREEN.blit(score_surface, score_rect)
            return 

        #blitting up everything
        SCREEN.blit(GAME_IMAGES["background"], (0,0))
        SCREEN.blit(GAME_IMAGES["player"], (playerX, playerY))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(GAME_IMAGES["pipe"][0],(upperPipe["x"], upperPipe["y"]))
            SCREEN.blit(GAME_IMAGES["pipe"][1],(lowerPipe["x"], lowerPipe["y"]))
        SCREEN.blit(GAME_IMAGES["base"], (baseX,baseY))

        #blitting the score
        scoreDigits = [int(x) for x in list(str(score))]
        scoreX = SCREEN_WIDTH/1.2
        scoreY = SCREEN_HEIGHT/1.6
        for digit in scoreDigits:
            SCREEN.blit(GAME_IMAGES["number"][digit], (scoreX, scoreY))
            scoreX += GAME_IMAGES["number"][digit].get_width()
        pygame.display.update()
        pygame.time.Clock().tick(FPS)


def isHit(playerX, playerY, upperPipes, lowerPipes):
    pipeHeight = GAME_IMAGES["pipe"][0].get_height()
    pipeWidth = GAME_IMAGES["pipe"][0].get_width()
    playerHeight = GAME_IMAGES["player"].get_height()
    playerWidth = GAME_IMAGES["player"].get_width()

    #hit with ceiling or base
    if playerY < 0 or playerY + playerHeight > SCREEN_HEIGHT - GAME_IMAGES["base"].get_height():
        return True
    #hit with upperpipes
    for pipe in upperPipes:
        if (playerY < pipe["y"] + pipeHeight) and  (pipe["x"] - playerWidth < playerX < pipe["x"] + pipeWidth):
            return True

    #hit with lowerpipes
    for pipe in lowerPipes:
        if (playerY + playerWidth > pipe["y"]) and  (pipe["x"] - playerWidth < playerX < pipe["x"] + pipeWidth):
            return True

    return False

def getRandomPipes():
    gap = GAME_IMAGES["player"].get_height() * 2
    y2 = randint(gap, SCREEN_HEIGHT - GAME_IMAGES["base"].get_height())
    y1 = y2 - gap -GAME_IMAGES["pipe"][0].get_height()
    pipeX = SCREEN_WIDTH
    pipe = [{"x":pipeX, "y": y1},{"x":pipeX,"y": y2}]
    return pipe
    

#Chương trình chính(main program)
pygame.init()
pygame.display.set_caption("Flappy Bird")
GAME_IMAGES["background"] = pygame.image.load("images/background.png").convert_alpha()
GAME_IMAGES["base"] = pygame.image.load("images/base.png").convert_alpha()
GAME_IMAGES["player"] = pygame.image.load("images/bird.png").convert_alpha()
GAME_IMAGES["message"] = pygame.image.load("images/FlappyBird.png").convert_alpha()
GAME_IMAGES["number"] = (pygame.image.load("images/0.png").convert_alpha(),
    pygame.image.load("images/1.png").convert_alpha(),
    pygame.image.load("images/2.png").convert_alpha(),
    pygame.image.load("images/3.png").convert_alpha(), 
    pygame.image.load("images/4.png").convert_alpha(), 
    pygame.image.load("images/5.png").convert_alpha(), 
    pygame.image.load("images/6.png").convert_alpha(), 
    pygame.image.load("images/7.png").convert_alpha(), 
    pygame.image.load("images/8.png").convert_alpha(), 
    pygame.image.load("images/9.png").convert_alpha())
GAME_IMAGES["pipe"] = (pygame.transform.rotate(pygame.image.load("images/pipe.png").convert_alpha(), 180),
    pygame.image.load("images/pipe.png").convert_alpha())

GAME_SOUNDS["die"] = pygame.mixer.Sound("audio/die.mp3")
GAME_SOUNDS["fly"] = pygame.mixer.Sound("audio/fly.flac")
GAME_SOUNDS["point"] = pygame.mixer.Sound("audio/point.mp3")

baseX = 0
baseY = SCREEN_HEIGHT - GAME_IMAGES["base"].get_height()
messageX = SCREEN_WIDTH/2 - GAME_IMAGES["message"].get_width()/2
messageY = SCREEN_HEIGHT/2 - GAME_IMAGES["message"].get_height()/2

while True:
    welcomeScreen()
    gameLoop()
