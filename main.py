import pygame
import sys
import random
from time import sleep

BLACK = (0,0,0)
padWidth = 480
padHeight = 640
explosionSound = [r'./assets/explosion01.wav',r'./assets/explosion02.wav',r'./assets/explosion03.wav',r'./assets/explosion04.wav']

def writeMessage(text):
    global gamePad
    textfont = pygame.font.SysFont('gulim.ttc', 60)
    text = textfont.render(text, True, (255, 0 , 0))
    textpos = text.get_rect()
    textpos.center = (padWidth/2, padHeight/2)
    gamePad.blit(text, textpos)
    pygame.display.update()
    sleep(2)
    runGame()

def crash():
    global gamePad
    writeMessage("Crashed")

def gameOver():
    global gamePad
    writeMessage("GameOver")

def rockImageStringMaker():
    rocknumber = random.randint(1,30)
    rockString = str(rocknumber)
    if rocknumber < 10:
        rockString = '0' + str(rocknumber)
    rockImageString = r'.\assets\rock' + rockString + '.png'
    print(rockImageString)
    return rockImageString

def writeScore(count):
    global gamePad
    font = pygame.font.SysFont('gulim.ttc', 30)
    text = font.render('Rock Hit' + str(count), True, (255,255,255))
    gamePad.blit(text, (10, 0))

def writePassed(count):
    global gamePad
    font = pygame.font.SysFont('gulim.ttc', 30)
    text = font.render('Rock Passed' + str(count), True, (255,0,0))
    gamePad.blit(text, (300, 0))

def drawObject(obj, x, y):
    global gamePad
    gamePad.blit(obj, (x,y))

def initGame():
    global gamePad, clock, background, fighter, missile, explosion, \
        missileSound, gameOverSound
    pygame.init()
    gamePad = pygame.display.set_mode((padWidth,padHeight))
    pygame.display.set_caption("PyShooting")
    background = pygame.image.load(r'.\assets\background.png') 
    fighter = pygame.image.load(r'.\assets\fighter.png')
    missile = pygame.image.load(r'.\assets\missile.png')
    clock = pygame.time.Clock()
    explosion = pygame.image.load(r'.\assets\explosion.png')
    pygame.mixer.music.load(r'.\assets\music.wav')
    pygame.mixer.music.play(-1)
    missileSound = pygame.mixer.Sound(r'.\assets\missile.wav')
    gameOverSound = pygame.mixer.Sound(r'.\assets\gameover.wav')
    

def runGame():
    global gamePad, clock, background, fighter, missile, explosion, \
        missileSound, gameOverSound
    fighterSize = fighter.get_rect().size
    fighterWidth = fighterSize[0]
    fighterHeight = fighterSize[1]
    
    x = padWidth * 0.45
    y = padHeight * 0.9
    fighterX = 0

    missileXY = []

    rock = pygame.image.load(rockImageStringMaker())
    rockSize = rock.get_rect().size
    rockWidth = rockSize[0]
    rockHeight = rockSize[1]

    rockX = random.randrange(0, padWidth - rockWidth)
    rockY = 0
    rockSpeed = 2

    isShot = False
    shotCount = 0
    rockPassed = 0


    onGame = False
    while not onGame:
        for event in pygame.event.get():
            if event.type in [pygame.QUIT]:
                pygame.quit()
                sys.exit()

            if event.type in [pygame.KEYDOWN]:
                if event.key == pygame.K_LEFT:
                    fighterX -= 5
                elif event.key == pygame.K_RIGHT:
                    fighterX += 5
                elif event.key == pygame.K_SPACE:
                    missileSound.play()
                    missileX = x + fighterWidth/2
                    missileY = y - fighterHeight
                    missileXY.append([missileX, missileY])

            if event.type in [pygame.KEYUP]:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    fighterX = 0

        drawObject(background, 0, 0)

        x += fighterX
        if x < 0:
            x = 0
        elif x > padWidth - fighterWidth:
            x = padWidth - fighterWidth
        
        if y < rockY + rockHeight:
            if (rockX > x and rockX < x + fighterWidth) or \
            (rockX + rockWidth > x) and (rockX + rockWidth < x + fighterWidth):
                crash()
            

        drawObject(fighter, x, y)

        if len(missileXY) != 0:
            for i, bxy in enumerate(missileXY):
                bxy[1] -= 10
                missileXY[i][1] = bxy[1]

                if bxy[1] < rockY:
                    if bxy[0] > rockX and bxy[0] < rockX + rockWidth:
                        missileXY.remove(bxy)
                        isShot = True
                        shotCount += 1

                if bxy[1] <= 0:
                    try:
                        missileXY.remove(bxy)
                    except:
                        pass
        
        if len(missileXY) != 0:
            for bx, by in missileXY:
                drawObject(missile, bx, by)

        writeScore(shotCount)


        rockY += rockSpeed

        if rockY > padHeight:
            rock = pygame.image.load(rockImageStringMaker())
            rockSize = rock.get_rect().size
            rockWidth = rockSize[0]
            rockHeight = rockSize[1]

            rockX = random.randrange(0, padWidth - rockWidth)
            rockY = 0
            rockPassed += 1

        if rockPassed == 3:
            gameOverSound.play()
            gameOver()
            

        writePassed(rockPassed)

        if isShot:
            drawObject(explosion, rockX, rockY)
            rock = pygame.image.load(rockImageStringMaker())
            rockSize = rock.get_rect().size
            rockWidth = rockSize[0]
            rockHeight = rockSize[1]

            rockX = random.randrange(0, padWidth - rockWidth)
            rockY = 0
            isShot = False

            rockSpeed += 0.2
            if rockSpeed >= 10:
                rockSpeed = 10

        drawObject(rock, rockX, rockY)

        pygame.display.update()
        clock.tick(60)
    
    pygame.quit()

initGame()
runGame()