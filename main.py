import pygame

import assets
import configs
from objects.background import Background
from objects.bird import Bird
from objects.column import Column
from objects.floor import Floor
from objects.game_over import GameOver
from objects.game_start import GameStart

pygame.init()

screen = pygame.display.set_mode((configs.SCREEN_WIDTH, configs.SCREEN_HEIGHT))
clock = pygame.time.Clock()
column_create_event = pygame.USEREVENT
running = True
gameOver = False
gameStarted = False
score = 0

assets.load_sprites()

sprites = pygame.sprite.LayeredUpdates()


def create_sprites():
    Background(0, sprites)
    Background(1, sprites)
    Floor(0, sprites)
    Floor(1, sprites)

    return Bird(sprites), GameStart(sprites)


bird, game_start_message = create_sprites()

while running:
    for event in pygame.event.get():
        # if user press quit
        if event.type == pygame.QUIT:
            running = False
        # start draw pipes when the gamestart
        if event.type == column_create_event and gameStarted:
            Column(sprites)
        # check if user press space
        if event.type == pygame.KEYDOWN:
            # check if not gameStarted and not gameOver when pressed space and start game
            if event.key == pygame.K_SPACE and not gameStarted and not gameOver:
                gameStarted = True
                game_start_message.kill()
                pygame.time.set_timer(column_create_event, 1500)
            # check if gameOver and user press ESCAPE so restart the game
            if event.key == pygame.K_ESCAPE and gameOver:
                gameOver = False
                gameStarted = False
                sprites.empty()
                bird, game_start_message = create_sprites()
        # when pressed space do bird's move
        bird.handle_event(event)

    screen.fill(0)

    # check bird's collision with pipe
    if bird.check_collision(sprites):
        gameOver = True
        gameStarted = False
        GameOver(sprites)
        pygame.time.set_timer(column_create_event, 0)

    # update the screen if it's not gameOver
    if gameStarted and not gameOver:
        sprites.update()

    # draw the updated screen
    sprites.draw(screen)

    # increase the score if the bird pass the pipe
    for sprite in sprites:
        if type(sprite) is Column and sprite.is_passed():
            score += 1

    print(score)

    pygame.display.flip()
    clock.tick(configs.FPS)

pygame.quit()
