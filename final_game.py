import pygame

pygame.init()

## create game window
screen = pygame.display.set_mode((500, 300))

def game_intro():

    intro = True

    while intro:
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        window.fill(white)
        largeText = pygame.font.SysFont("comicsansms",115)
        TextSurf, TextRect = text_objects("A bit Racey", largeText)
        TextRect.center = ((display_width/2),(display_height/2))
        window.blit(TextSurf, TextRect)

        button("GO!",150,450,100,50,green,bright_green,game_loop)
        button("Quit",550,450,100,50,red,bright_red,quitgame)
        # TODO (Optional): You may implement three different difficulty levels.
        # For example, level 1 is the default start speed and incrementing by 1.
        # Levels 2 and 3 would have a higher start speed and larger increments.

        pygame.display.update()
        clock.tick(15)