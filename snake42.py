import pygame
import time
import random
pygame.init()

#defines colors
white = (255,255,255)
black = (0,0,0)
red   = (255,0,0)
blue = (0,0,255)
green = (0,155,0)
#sets the display
display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Slither')

icon = pygame.image.load('apple.png')
pygame.display.set_icon(icon)

img = pygame.image.load('snakehead.png')
appleimg = pygame.image.load('apple1.png')

#clock for frames per second
clock = pygame.time.Clock()

AppleThickness = 30

#snake size
block_size = 20

#frame per second
FPS = 15

direction = "right"

#font for message
smallfont = pygame.font.SysFont("comicsansms", 25)
medfont = pygame.font.SysFont("comicsansms", 50)
largefont = pygame.font.SysFont("comicsansms", 80)


def pause():

    paused = True
    
    message_to_screen("Paused",
                      black,
                      -100,
                      size="large")
    message_to_screen("Press C to continue or Q to quit.",
                          black,
                          25)
    pygame.display.update()

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        #gameDisplay.fill(white)

        clock.tick(5)
        
                    

def score(score):
    text = smallfont.render("Score: "+ str(score), True, black)
    gameDisplay.blit(text, [0,0])

def randAppleGen():
    randAppleX = round(random.randrange(0, display_width - AppleThickness))#/10.0) * 10.0
    randAppleY = round(random.randrange(0, display_height - AppleThickness)) #/ 10.0) * 10.0

    return randAppleX,randAppleY

def game_intro():
    intro = True

    while intro:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        
        gameDisplay.fill(white)
        message_to_screen('Welcome to Slither',
                          green,
                          -100,
                          "large")
        message_to_screen("The objective is to eat the red apples",
                          black,
                          -30)
        message_to_screen("The more apples you eat, the longer you get",
                          black,
                          10)
        message_to_screen("If you run off the screen or into yourself, you die!",
                          black,
                          50)
        message_to_screen("Press C to play and Q to quit",
                          black,
                          180)
        pygame.display.update()
        clock.tick(5)

    

#create the snake and allows it to get longer by adding to the list
def snake(block_size,snakelist):
    if direction == "right":
        head = pygame.transform.rotate(img, 270)
    if direction == "left":
        head = pygame.transform.rotate(img, 90)
    if direction == "up":
        head = img
    if direction == "down":
        head = pygame.transform.rotate(img, 180)


    gameDisplay.blit(head, (snakelist[-1][0], snakelist[-1][1]))
    
    for XNY in snakelist[:-1]:
        pygame.draw.rect(gameDisplay, green, [XNY[0], XNY[1], block_size,block_size])

def text_objects(text,color,size):
    if size == "small":
        textSurface = smallfont.render(text, True, color)
        return textSurface, textSurface.get_rect()
    elif size == "medium":
        textSurface = medfont.render(text, True, color)
        return textSurface, textSurface.get_rect()
    elif size == "large":
        textSurface = largefont.render(text, True, color)
        return textSurface, textSurface.get_rect()


#game message function
def message_to_screen(msg,color,y_displace=0, size = "small"):
    textSurface, textRect = text_objects(msg,color, size)
    textRect.center = (display_width / 2), (display_height / 2) + y_displace
    gameDisplay.blit(textSurface, textRect)


#game loop
def gameLoop():
    global direction
    direction = 'right'
    gameExit = False
    gameOver = False
     #First Block initial location
    lead_x = display_width/2
    lead_y = display_height/2
     #First Block movement
    lead_x_change = 10
    lead_y_change = 0

    snakeList = []
    snakeLength = 1

    #randomly generates apples, - block_size to keep apple on screen, / 10 & * 10 give apple location multiple of 10
    randAppleX,randAppleY = randAppleGen()

    
    while not gameExit:

        if gameOver == True:
            message_to_screen("Game over",
                              red,
                              -50,
                              size = "large")
            message_to_screen("Press C to play again or Q to quit",
                              black,
                              50,
                              size = "medium")
            pygame.display.update()


        while gameOver == True:
            
            #the you lose screen


            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    #If the user hits q then the game quits, if c it play again
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            #Exits the game
            if event.type == pygame.QUIT:
                gameExit = True
                gameOver = False
            #event handling
            if event.type == pygame.KEYDOWN:
                #If left arrow then move left
                if event.key == pygame.K_LEFT:
                    direction = "left"
                    lead_x_change = -block_size
                    lead_y_change = 0
                #if right arrow then move right
                elif event.key == pygame.K_RIGHT:
                    direction = "right"
                    lead_x_change = block_size
                    lead_y_change = 0
                #If up arrow then move up
                elif event.key == pygame.K_UP:
                    direction = "up"
                    lead_y_change = -block_size
                    lead_x_change = 0 
                #if down arrow then move down
                elif event.key == pygame.K_DOWN:
                    direction = "down"
                    lead_y_change = block_size
                    lead_x_change = 0
                    
                elif event.key == pygame.K_p:
                    pause()
            
            #boundries if position of block is out of screen x or y then game exit
            if lead_x >= display_width or lead_x < 0 or lead_y >= display_height or lead_y < 0:
                gameOver = True
                
                    
        lead_x += lead_x_change            
        lead_y += lead_y_change            

        #Turns screen white        
        gameDisplay.fill(white)
        #draws a red rectangle or apple to the screen and defines position and size
        
        #pygame.draw.rect(gameDisplay, red, [randAppleX, randAppleY, AppleThickness, AppleThickness])
        
        gameDisplay.blit(appleimg, (randAppleX, randAppleY))




        #creates a list for the snake head
        snakeHead = []
        #Appends the head(x) first then y
        snakeHead.append(lead_x)
        snakeHead.append(lead_y)
        snakeList.append(snakeHead)
        #keeps the head at the front
        if len(snakeList) > snakeLength:
            del snakeList[0]
        #If you hit yourself then gameover
        for eachSegment in snakeList[:-1]:
            if eachSegment == snakeHead:
                gameOver = True
            
        
        #calls the snake function to create a snake
        snake(block_size,snakeList)

        score(snakeLength - 1)
        
        pygame.display.update()



        #make the snake eat the apple / collision detection
        if lead_x > randAppleX and lead_x < randAppleX + AppleThickness or lead_x + block_size > randAppleX and lead_x + block_size < randAppleX + AppleThickness:
            if lead_y > randAppleY and lead_y < randAppleY + AppleThickness:
                randAppleX,randAppleY = randAppleGen()

                snakeLength += 1
            elif lead_y + block_size > randAppleY and lead_y + block_size < randAppleY + AppleThickness:              
                randAppleX,randAppleY = randAppleGen()

                snakeLength += 1







        #frame per second
        clock.tick(FPS)
        

    #Exits the game & python
    pygame.quit()

    quit()
#calls the intro
game_intro()
#calls the game loop
gameLoop()
