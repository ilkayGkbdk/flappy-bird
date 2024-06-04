import pygame

import assets
import configs
from objects.background import Background
from objects.bird import Bird
from objects.column import Column
from objects.floor import Floor
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

Background(0, sprites)
Background(1, sprites)
Floor(0, sprites)
Floor(1, sprites)

bird = Bird(sprites)

game_start_message = GameStart(sprites)

pygame.time.set_timer(column_create_event, 1500)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == column_create_event and gameStarted:
            Column(sprites)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                gameStarted = True
                game_start_message.kill()

        bird.handle_event(event)

    screen.fill(0)

    if bird.check_collision(sprites):
        gameOver = True
        gameStarted = False

    if gameStarted and not gameOver:
        sprites.update()

    sprites.draw(screen)

    for sprite in sprites:
        if type(sprite) is Column and sprite.is_passed():
            score += 1

    print(score)

    pygame.display.flip()
    clock.tick(configs.FPS)
pygame.quit()
