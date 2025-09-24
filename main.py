import pygame
import random

pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((400, 800))
pygame.display.set_caption('Flappy Whale')

my_font = pygame.font.SysFont('Comic Sans MS', 50, bold=True)
my_font2 = pygame.font.SysFont('Comic Sans MS', 30, bold=True)
my_font3 = pygame.font.SysFont('Comic Sans MS', 20, bold=True)

# ---IMAGES

# Enviroment
sky_surf = pygame.image.load('assets/environment/sky.png')
sky_surf = pygame.transform.scale(sky_surf, (800, 700))

ground_surf = pygame.image.load('assets/environment/ground.png')
ground_surf = pygame.transform.scale(ground_surf, (600, 100))

pipe_surf = pygame.image.load('assets/environment/pipe.png')
pipe_surf = pygame.transform.scale(pipe_surf, (100, 625))

whale_img = [
    pygame.transform.scale(pygame.image.load('assets/whale/whale1.png'), (120, 120)),
    pygame.transform.scale(pygame.image.load('assets/whale/whale2.png'), (120, 120)),
    pygame.transform.scale(pygame.image.load('assets/whale/whale3.png'), (120, 120)),
    pygame.transform.scale(pygame.image.load('assets/whale/whale4.png'), (120, 120))
]
whale_rect = whale_img[0].get_rect()


clock = pygame.time.Clock()

scroll_bg = 0
scroll_ground = 0

whale_ani_speed = 0
whale_frameIndex = 0

whaley = 400

gravity = 4
whale_velocity = 0

Running = True
game_active = True
game_over_cooldown = 60

pipey = -1
pipex = -50

score = 0

def reset():
    global scroll_bg, scroll_ground
    global whale_ani_speed, whale_frameIndex
    global whaley, gravity, whale_velocity
    global pipex, pipey, game_active, score, game_over_cooldown

    scroll_bg = 0
    scroll_ground = 0

    whale_ani_speed = 0
    whale_frameIndex = 0

    score = 0

    whaley = 400

    gravity = 4
    whale_velocity = 0

    game_active = True
    game_over_cooldown = 60

    pipey = -1
    pipex = -50

while Running:
    Keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Running = False
        if game_active:
            if Keys[pygame.K_SPACE]:
                whale_velocity = -9
                print("Jumped")

    if game_active:
        screen.blit(sky_surf, (scroll_bg + 800, 0))
        screen.blit(sky_surf, (scroll_bg, 0))
        screen.blit(ground_surf, (scroll_ground, 700))
        screen.blit(ground_surf, (scroll_ground + 600, 700))

        whale_rect = whale_img[0].get_rect(center=(100, whaley))
        screen.blit(whale_img[whale_frameIndex], whale_rect)

        #   --Pipes--
        pipe_rect = pipe_surf.get_rect(midtop=(pipex, pipey + 75))
        screen.blit(pipe_surf, pipe_rect)
        flipped_pipe = pygame.transform.flip(pipe_surf, False, True)
        flipped_pipe_rect = flipped_pipe.get_rect(midbottom=(pipex, pipey - 75))
        screen.blit(flipped_pipe, flipped_pipe_rect)
        print(pipey)

    #   --ANIMATIONS--
        whale_ani_speed += 0.1
        if whale_ani_speed > 1:
            whale_frameIndex += 1
            whale_frameIndex %= len(whale_img)
            whale_ani_speed -= 1

    #Environment Scroll
        scroll_bg -= 1
        if scroll_bg <= -800:
            scroll_bg = 0

        scroll_ground -= 1
        if scroll_ground <= -600:
            scroll_ground = 0

        pipex -= 2
        if pipex < -50:
            pipey = random.randint(100, 600)
            pipex = 450


    #   --Physics--
        if whale_velocity < 0:
            whale_velocity += 0.225
        whaley += whale_velocity + gravity

        if whaley > 675:
            game_active = False

        if whaley < 0:
            whaley = 0

    #   --  Pipe Collision
    if 20 < pipex < 185:
        if whaley < pipey-75 or whaley > pipey + 50:
            game_active = False

    if pipex == 60:
        score += 1

    scoreUI = my_font.render("Score: " + str(score), False, (0, 0, 0))
    screen.blit(scoreUI, (0, 0))

    if not game_active:
        game_over_font = my_font.render('Game Over', False, (0, 0, 0))
        game_over_rect = game_over_font.get_rect(center=(200,400))
        screen.blit(game_over_font, game_over_rect)
        game_over_font = my_font2.render('Press Space to reset', False, (0, 0, 0))
        game_over_rect = game_over_font.get_rect(center=(200,450))
        screen.blit(game_over_font, game_over_rect)

        if Keys[pygame.K_SPACE] and game_over_cooldown < 0:
            reset()
            game_active = True
        else:
            game_over_cooldown -= 1

    pygame.display.update()
    clock.tick(60)



pygame.quit()

