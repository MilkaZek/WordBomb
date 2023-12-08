"""
Authors: Cara Babin, Paige Inoue, Milka Zekarias
Updated as of: 12/07/2023
Description: A hangman inspired word-guessing game where you have five lives to complete a word before a ticking time bomb goes off!
References: Word API sourced from "https://random-word-api.herokuapp.com/"
Screens and game loop framework sourced from racey.py (Lab 15)
Explosion sound sourced from Pixabay
Cheering sound sourced from Gamerboy on Youtube
Background music sourced from Jonny Boyle on Uppbeat.io
Bomb graphics found online and edited by Paige Inoue
Other images and backgrounds sourced online
"""

# Importing libraries
import pygame
import requests

# Initializing Pygame
pygame.init()

# Setting up display
display_width = 800
display_height = 600

# Establishing basic colors
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

# Alphabet list
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

# Background Images
screen_background = pygame.image.load('bomb-blast-clipart-7.jpg')
screen_exploded = pygame.image.load('boom.jpg')

# Bomb Images
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

# Function to generalize text formatting
def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

# Function to close out the game window and stop the game from running
def quitgame():
    pygame.quit()
    quit()

# Funtion to generalize creation and formatting of buttons
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

'''
Game class:
* Attributes initialize a:
- Word class object
- Bomb class object
- 5 lives, empty response string
- empty popup
- custom count of remaining lives message

* Methods involve:
- updating the message of the response and pop-up
- assigning a message for the response and pop-up based on user input
- updating the displayed word, bomb image, and messages at one method call
'''
class Game:
    def __init__(self):
        self.word = Word()
        self.bomb = Bomb()
        self.lives = 5
        self.response = ""
        self.popup = ""
        self.custom_message = "lives"
    
    # Updates correct/incorrect message and remaining life count pop-up
    def update_message(self):
        TextSurf, TextRect = text_objects(self.response, pygame.font.SysFont("comicsansms", 25), black)
        TextRect.center = ((3 * display_width/4),(500))
        screen.blit(TextSurf, TextRect)
       
        TextSurf, TextRect = text_objects(self.popup, pygame.font.SysFont("comicsansms", 25), black)
        TextRect.center = ((3 * display_width/4),(540))
        screen.blit(TextSurf, TextRect)

    # Connects user input to an appropriate response (correct/incorrect) and updates lives remaining pop-up accordingly
    def letter_guessed(self, guess):
        # get keyboard inputs and compare with word
        if guess in alphabet:
            result = self.word.check_word(guess)
            if result == None:
                return
            elif result:
                self.response = "Correct!"
            else:
                self.bomb.burn()
                self.lives -= 1
                self.response = "Wrong!"
                if self.lives == 1:
                    self.custom_message = "life"
            self.popup = f'You have {self.lives} {self.custom_message} left'      

    # Updates the letters of the word displayed on the screen, the image of the bomb and fuse, and the message (response and lives remaining pop-up)    
    def update_screen(self):
        self.word.word_on_screen()
        self.bomb.update_bomb()
        self.update_message()

'''
Bomb class:
* Attributes initialize:
- a list of different bomb images with different fuse lengths
- original full length of bomb fuse: 4 units

* Methods involve:
- updating and displaying the image of the bomb with the corresponding fuse length
- updating the numerical length of the fuse to access the corresponding image in the bomb phase image list
'''
class Bomb:
    def __init__(self):
        self.fuse = [bomb_1, bomb_2, bomb_3, bomb_4, bomb_5]
        self.length_of_fuse = 4

    # Accesses and displays the corresponding image of the bomb from the list of bomb images with different fuse lengths
    def update_bomb(self):
        bomb_phase = self.fuse[self.length_of_fuse]
        screen.blit(bomb_phase, (10, 25))

    # Decreases the numerical length of the fuse to correspondingly access a different image of the bomb phase list
    def burn(self):
        self.length_of_fuse -= 1

'''
Word class:
* Attributes initialize:
- a word from the Random Word API is retrieved
- an empty wordbank of incorrect guessed letters
- an empty list of all user letter guesses, including correct & incorrect guesses
- a list of underscore placeholders displayed on the screen in place of the unguessed letters of the correct word

* Methods involve:
- checking to see if the user guess is a letter in the correct word or not, and updating the wordbank, guesses list, and display of the correct letters accordingly
- displaying the placeholder underscores of the letters in the correct word along with the correct letters guessed in their spots in the word
'''
class Word:
    def __init__(self):
        response = requests.get("https://random-word-api.herokuapp.com/word?length=5")
        data = response.json()
        self.answer = data[0]
        self.wordbank = ""
        self.guesses = []
        self.display = ["_", "_", "_", "_", "_"]
    
    # Function checks to see if the user's guessed letter is in the word
    # if it is, it is added to the display and replaces the corresponding placeholder underscores
    # if not, it is added to the displayed incorrect letter guess wordbank
    def check_word(self, guess):
        correct = False
        if guess not in self.guesses:
            self.guesses.append(guess)
            for i in range(len(self.answer)):
                if guess == self.answer[i]:
                    self.display[i] = guess
                    correct = True
            if not correct:
                self.wordbank += f'{guess} '
        else:
            return
        return correct
    
    # Function displays the current values (either the placeholder underscore or the correctly guessed letter) at each of the 5 spots for the letters of the correct word
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

# Function displays the intro screen with music and buttons to start the game, go to the how to play screen, or quit the game
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

# Function displays the How to Play screen along with a button to go back to the Home/Intro Screen
def how_to_play_screen():
    how_to_play = True
    
    while how_to_play:
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

        textSurf, textRect = text_objects("Guess the word before the fuse burns completely", smallText, black)
        textRect.center = ((display_width/2),(display_height/2))
        screen.blit(textSurf, textRect)
        
        textSurf, textRect = text_objects("or the bomb EXPLODES", smallText, bright_red)
        textRect.center = ((display_width/2),(display_height/1.5))
        screen.blit(textSurf, textRect)

        button("Back To Home",150,500,150,50,green,bright_green,game_intro)

        pygame.display.update()
        clock.tick(15)
    
# Function to have the game run, collecting user input and creating an object of the Game class to accordingly respond to the user input
# Updates the screen accordingly to the keys pressed until all the letters of the correct word are guessed or the user is out of lives, whichever comes first
def game_loop():
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.load('easy-does-it-jonny-boyle-main-version-02-28-20.mp3')
        pygame.mixer.music.play(-1)

    playing = True
    play = Game()
    
    while playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                key = pygame.key.name(event.key)
                play.letter_guessed(key)
        screen.fill(white)
        play.update_screen()
        pygame.display.update()
        clock.tick(60)
        if play.lives == 0:
            lose(play.word.answer)
        if "_" not in play.word.display:
            win(play)

# Function to go to the Game Over screen if the player loses and doesn't guess the word before running out of lives.
# Shows the visuals and audio of the bomb explosion, the correct word, and has buttons to either play again or quit the game
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

# Plays the winner cheering sound effect and shows the defused bomb
# Displays buttons to play again or quit the game
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

# Calls the function to show the intro screen and allow the user to start playing the game and call the game_loop function
game_intro()

