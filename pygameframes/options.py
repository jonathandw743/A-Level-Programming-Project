import pygame

from geometry.vector import Vector

def options(screen, user):
    WIDTH = screen.get_width()
    HEIGHT = screen.get_height()

    FPS = 60

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)

    clock = pygame.time.Clock()

    # create some text to whow which screen it is
    my_font = pygame.font.SysFont("Comic Sans MS", 50)
    text_render = my_font.render("options", False, WHITE)

    running = True
    while running:

        dt = clock.tick(FPS) * 0.001

        mouse_pos = Vector.from_tuple(pygame.mouse.get_pos())

        for event in pygame.event.get():
            # go all the way back if cross clicked
            if event.type == pygame.QUIT:
                return -1
            if event.type == pygame.KEYDOWN:
                # go back if Esc pressed
                if event.key == pygame.K_ESCAPE:
                    return 0

        keys = pygame.key.get_pressed()

        screen.fill(BLACK)

        screen.blit(text_render, (0, 0))

        pygame.display.flip()