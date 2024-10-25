import pygame
from constants import *
from player import Player
from asteroids import Asteroid
from asteroidfield import AsteroidField
from shot import Shot


def main():
    pygame.init()
    pygame.mixer.init()
    asteroid_hit_sound = pygame.mixer.Sound('/home/myrm/workspace/github.com/myrm1/lidl_asteroid/sounds/destroying_asteroid.wav')
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    def init_game():
        updatable = pygame.sprite.Group()
        drawable = pygame.sprite.Group()
        asteroids = pygame.sprite.Group()
        shots = pygame.sprite.Group()

        Shot.containers = (shots, updatable, drawable)
        Asteroid.containers = (asteroids, updatable, drawable)
        AsteroidField.containers = updatable
        asteroid_field = AsteroidField()

        Player.containers = (updatable, drawable)
        player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        score = 0

        return updatable, drawable, asteroids, shots, player, asteroid_field, score

    updatable, drawable, asteroids, shots, player, asteroid_field, score = init_game()
    game_over = False
    dt = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN and game_over:
                if event.key == pygame.K_SPACE:
                    game_over = False
                    updatable, drawable, asteroids, shots, player, asteroid_field, score = init_game()

        if not game_over:
            for obj in updatable:
                obj.update(dt)

            for asteroid in asteroids:
                if asteroid.collides_with(player):
                    game_over = True
                
                for shot in shots:
                    if asteroid.collides_with(shot):
                        shot.kill()
                        asteroid.split()
                        score += 10
                        asteroid_hit_sound.play()

            screen.fill("black")

            for obj in drawable:
                obj.draw(screen)

            font_score = pygame.font.Font(None, 36)
            score_text = font_score.render(f'Score: {score}', True, 'white')
            score_rect = score_text.get_rect(topleft=(10, 10))
            screen.blit(score_text, score_rect)

            if game_over:
                font_big = pygame.font.Font(None, 74)
                game_over_text = font_big.render('Good job you fucking IDIOT.', True, 'white')
                game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 50))
                screen.blit(game_over_text, game_over_rect)

                font_small = pygame.font.Font(None, 36)
                restart_text = font_small.render('Press SPACE to restart', True, 'white')
                restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 +50))
                screen.blit(restart_text, restart_rect)

            pygame.display.flip()

            # limit the framerate to 100 FPS
            dt = clock.tick(100) / 1000


if __name__ == "__main__":
    main()
