import pygame
import time
import random

pygame.init()

display_width = 800
display_height = 600

black = (0,0,0)
white = (246,246,246)

red = (200,0,0)
green = (0,200,0)

bright_red = (255,0,0)
bright_green = (0,255,0)
dark_red = (77, 0, 0)
blue = (0, 172, 230)
bright_blue = (26, 198, 255)

block_color = (53,115,255)

screen_background = pygame.image.load('bomb-blast-clipart-7.jpg')

## create game window
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Bomb')
clock = pygame.time.Clock()


def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def quitgame():
    pygame.quit()
    quit()

def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(screen, ac,(x,y,w,h))
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(screen, ic,(x,y,w,h))
    smallText = pygame.font.SysFont("comicsansms",20)
    textSurf, textRect = text_objects(msg, smallText, black)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    screen.blit(textSurf, textRect)


def game_intro():
    pygame.mixer.music.load('easy-does-it-jonny-boyle-main-version-02-28-20.mp3')
    pygame.mixer.music.play(-1)
    intro = True

    while intro:
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.fill(white)
        screen.blit(screen_background, (65, -20))
        largeText = pygame.font.SysFont("comicsansms",115)
        
        TextSurf, TextRect = text_objects("Wordbomb!", largeText, dark_red)
        TextRect.center = ((display_width/2),(260))
        screen.blit(TextSurf, TextRect)
        button("Start!",150,450,100,50,green,bright_green,game_loop)
        button("How to Play",338,450,124,50,blue,bright_blue,how_to_play_screen)
        button("Quit",550,450,100,50,red,bright_red,quitgame)

        pygame.display.update()
        clock.tick(15)

def how_to_play_screen():
    while True:
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.fill(white)
        largeText = pygame.font.SysFont("comicsansms",115)
        TextSurf, TextRect = text_objects("How To Play", largeText, dark_red)
        TextRect.center = ((display_width/2),(display_height/5))
        screen.blit(TextSurf, TextRect)

        smallText = pygame.font.SysFont("comicsansms",20)
        textSurf, textRect = text_objects("You have 3 letter guesses per word", smallText, black)
        textRect.center = ((display_width/2),(display_height/3))
        screen.blit(textSurf, textRect)

        ttextSurf, ttextRect = text_objects("Guess the word before the fuse burns", smallText, black)
        ttextRect.center = ((display_width/2),(display_height/2))
        screen.blit(ttextSurf, ttextRect)
        
        textSSurf, textRRect = text_objects("or the bomb EXPLODES", smallText, bright_red)
        textRRect.center = ((display_width/2),(display_height/1.5))
        screen.blit(textSSurf, textRRect)

        button("Back To Home",150,450,100,50,green,bright_green,game_intro)

        pygame.display.update()
        clock.tick(15)

    
def game_loop():
    pass

game_intro()

