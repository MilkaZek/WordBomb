"""
Authors: Cara Babin, Paige Inoue, Milka Zekarias
Updated as of: 11/30/2023
Description: A hangman inspired word-guessing game where you have five lives to complete a word before a ticking time bomb goes off!
References: Word API sourced from "https://random-word-api.herokuapp.com/"
Screens and game loop framework sourced from racey.py (Lab 15)
Explosion sound sourced from Pixabay
Cheering sound sourced from Gamerboy on Youtube
Background music sourced from Jonny Boyle on Uppbeat.io
Other images and backgrounds sourced online
"""

import pygame
import time
import random
import requests

pygame.init()

display_width = 800
display_height = 600

black = (0,0,0)
white = (246,246,246)

red = (200,0,0)
green = (0,200,0)
highlighter_yellow = (255, 255, 0)

bright_red = (255,0,0)
bright_green = (0,255,0)
dark_red = (77, 0, 0)
blue = (0, 172, 230)
bright_blue = (26, 198, 255)

block_color = (53,115,255)

screen_background = pygame.image.load('bomb-blast-clipart-7.jpg')
screen_exploded = pygame.image.load('boom.jpg')

bomb_5 = pygame.transform.scale(pygame.image.load('bomb_5.png'), (400, 400))
bomb_4 = pygame.transform.scale(pygame.image.load('bomb_4.png'), (400, 400))
bomb_3 = pygame.transform.scale(pygame.image.load('bomb_3.png'), (400, 400))
bomb_2 = pygame.transform.scale(pygame.image.load('bomb_2.png'), (400, 400))
bomb_1 = pygame.transform.scale(pygame.image.load('bomb_1.png'), (400, 400))
bomb_defuse = pygame.transform.scale(pygame.image.load('bomb_defuse.png'), (400, 400))

## create game window
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Wordbomb')
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
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.load('easy-does-it-jonny-boyle-main-version-02-28-20.mp3')
        pygame.mixer.music.play(-1)
    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.fill(white)
        screen.blit(pygame.transform.scale(screen_background, (800, 600)), (0, 0))
        largeText = pygame.font.SysFont("comicsansms",115)
        
        TextSurf, TextRect = text_objects("Wordbomb!", largeText, dark_red)
        TextRect.center = ((display_width/2),(260))
        screen.blit(TextSurf, TextRect)
        button("Start!",150,450,100,50,green,bright_green,game_loop)
        button("How to Play",338,450,124,50,blue,bright_blue,how_to_play_screen)
        button("Quit",550,450,100,50,red,bright_red,quitgame)

        pygame.display.update()
        clock.tick(15)
    
def game_loop():
    playing = True
    play = Game()
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.load('easy-does-it-jonny-boyle-main-version-02-28-20.mp3')
        pygame.mixer.music.play(-1)
    
    while playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                key = pygame.key.name(event.key)
                play.compare_guess(key)
        play.mainscreen()
        clock.tick(60)
        if play.lives == 0:
            lose(play.word)
        if "_" not in play.display:
            win(play)





class Game:
    def __init__(self):
        response = requests.get("https://random-word-api.herokuapp.com/word?length=5")
        data = response.json()
        self.word = data[0]
        # self.word = "arbor"
        self.display = ["_", "_", "_", "_", "_"]
        self.guesses = []
        self.lives = 5
        self.bomb = Bomb()
        self.wordbank = ""
        self.result = ""
        self.popup = ""
        self.custom_message = "lives"

    def word_on_screen(self):
            TextSurf, TextRect = text_objects(self.display[0], pygame.font.SysFont("comicsansms",75), black)
            TextRect.center = ((300),(260))
            screen.blit(TextSurf, TextRect)

            TextSurf, TextRect = text_objects(self.display[1], pygame.font.SysFont("comicsansms",75), black)
            TextRect.center = ((400),(260))
            screen.blit(TextSurf, TextRect)

            TextSurf, TextRect = text_objects(self.display[2], pygame.font.SysFont("comicsansms",75), black)
            TextRect.center = ((500),(260))
            screen.blit(TextSurf, TextRect)

            TextSurf, TextRect = text_objects(self.display[3], pygame.font.SysFont("comicsansms",75), black)
            TextRect.center = ((600),(260))
            screen.blit(TextSurf, TextRect)

            TextSurf, TextRect = text_objects(self.display[4], pygame.font.SysFont("comicsansms",75), black)
            TextRect.center = ((700),(260))
            screen.blit(TextSurf, TextRect)

            TextSurf, TextRect = text_objects(self.wordbank, pygame.font.SysFont("comicsansms",75), black)
            TextRect.center = ((150),(500))
            screen.blit(TextSurf, TextRect)
    
    
    def update_message(self):
        TextSurf, TextRect = text_objects(self.result, pygame.font.SysFont("comicsansms", 25), black)
        TextRect.center = ((3 * display_width/4),(500))
        screen.blit(TextSurf, TextRect)
       
        TextSurf, TextRect = text_objects(self.popup, pygame.font.SysFont("comicsansms", 25), black)
        TextRect.center = ((3 * display_width/4),(540))
        screen.blit(TextSurf, TextRect)

    def compare_guess(self, guess):
        # get keyboard inputs and compare with word
        correct = False
        if guess in self.guesses:
            return
        else:
            self.guesses.append(guess)
        for i in range(len(self.word)):
            if guess == self.word[i]:
                self.display[i] = guess
                self.result = "Correct!"
                correct = True
                
        if not correct:
            self.bomb.burn()
            self.lives -= 1
            self.result = "Wrong!"
            if self.lives == 1:
                self.custom_message = "life"
            self.wordbank += f'{guess} '
        self.popup = f'You have {self.lives} {self.custom_message} left'
                
        
    # this is main game
    def mainscreen(self):
        screen.fill(white)
        self.word_on_screen()
        self.bomb.update_bomb()
        self.update_message()
        pygame.display.update()

class Bomb:
    def __init__(self):
        self.fuse = [bomb_1, bomb_2, bomb_3, bomb_4, bomb_5]
        self.length_of_fuse = 4

    def update_bomb(self):
        bomb_phase = self.fuse[self.length_of_fuse]
        screen.blit(bomb_phase, (10, 25))

    def burn(self):
        self.length_of_fuse -= 1

        
def how_to_play_screen():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.fill(white)
        largeText = pygame.font.SysFont("comicsansms",115)
        TextSurf, TextRect = text_objects("How To Play", largeText, black)
        TextRect.center = ((display_width/2),(display_height/5))
        screen.blit(TextSurf, TextRect)

        smallText = pygame.font.SysFont("comicsansms",20)
        textSurf, textRect = text_objects("You have 5 lives per word", smallText, black)
        textRect.center = ((display_width/2),(display_height/3))
        screen.blit(textSurf, textRect)

        ttextSurf, ttextRect = text_objects("Guess the word before the fuse burns completely", smallText, black)
        ttextRect.center = ((display_width/2),(display_height/2))
        screen.blit(ttextSurf, ttextRect)
        
        textSSurf, textRRect = text_objects("or the bomb EXPLODES", smallText, bright_red)
        textRRect.center = ((display_width/2),(display_height/1.5))
        screen.blit(textSSurf, textRRect)

        button("Back To Home",150,500,150,50,green,bright_green,game_intro)

        pygame.display.update()
        clock.tick(15)

def lose(word):
    pygame.mixer.music.load('explosion-42132.mp3')
    pygame.mixer.music.play(1)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.fill(white)
        screen.blit(pygame.transform.scale(screen_exploded, (800, 600)), (0, 0))
        largeText = pygame.font.SysFont("comicsansms", 75)
        
        TextSurf, TextRect = text_objects("YOU EXPLODED!!!", largeText, highlighter_yellow)
        TextRect.center = ((display_width/2),(175))
        screen.blit(TextSurf, TextRect)
        TextSurf, TextRect = text_objects("OH NO......", largeText, highlighter_yellow)
        TextRect.center = ((display_width/2),(300))
        screen.blit(TextSurf, TextRect)
        TextSurf, TextRect = text_objects(f'The correct word was: {word}', pygame.font.SysFont("comicsansms", 20), highlighter_yellow)
        TextRect.center = ((display_width/2),(380))
        screen.blit(TextSurf, TextRect)
        button("Try Again",150,450,100,50,green,bright_green,game_loop)
        button("Quit",550,450,100,50,red,bright_red,quitgame)

        pygame.display.update()
        clock.tick(15)


def win(game):
    pygame.mixer.music.load('yay!!!.mp3')
    pygame.mixer.music.play(1)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        screen.blit(bomb_defuse, (10, 25))
        button("Play Again!",150,400,100,50,green,bright_green,game_loop)
        button("Quit",550,400,100,50,red,bright_red,quitgame)
        pygame.display.update()
        clock.tick(15)

game_intro()

