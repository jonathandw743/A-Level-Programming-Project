import pygame

from geometry.vector import Vector

from users.user import User

from .button import Button

def game_over(screen):
    WIDTH = screen.get_width()
    HEIGHT = screen.get_height()

    FPS = 60

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)

    clock = pygame.time.Clock()

    my_font = pygame.font.SysFont("Comic Sans MS", 50)
    text_render = my_font.render("game_over", False, WHITE)

    retry_button = Button(
        "retry",
        WIDTH / 2,
        3 * HEIGHT / 10,
        200,
        50,
        lambda: 1,
        my_font,
        WHITE,
    )

    exit_to_level_select_button = Button(
        "exit_to_level_select",
        WIDTH / 2,
        5 * HEIGHT / 10,
        200,
        50,
        lambda: 2,
        my_font,
        WHITE,
    )

    running = True
    while running:
        dt = clock.tick(FPS) * 0.001

        mouse_pos = Vector.from_tuple(pygame.mouse.get_pos())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return -1

            # check all buttons for mouse down
            if event.type == pygame.MOUSEBUTTONDOWN:
                retry_button.check_mouse_down(mouse_pos)
                exit_to_level_select_button.check_mouse_down(mouse_pos)
                #// save_button.check_mouse_down(mouse_pos)

            # check all buttons for mouse up
            if event.type == pygame.MOUSEBUTTONUP:
                screens_to_exit = retry_button.check_mouse_up(mouse_pos)
                if screens_to_exit:
                    return screens_to_exit - 1
                screens_to_exit = exit_to_level_select_button.check_mouse_up(mouse_pos)
                if screens_to_exit:
                    return screens_to_exit - 1
                #// screens_to_exit = save_button.check_mouse_up(mouse_pos)
                #// if screens_to_exit:
                #//     return screens_to_exit - 1

            if event.type == pygame.KEYDOWN:
                # go back if Esc clicked
                if event.key == pygame.K_ESCAPE:
                    return 0

        keys = pygame.key.get_pressed()

        screen.fill(BLACK)

        # draw the game over text
        screen.blit(text_render, (0, 0))

        # draw the buttons
        retry_button.draw(screen)
        exit_to_level_select_button.draw(screen)
        #// save_button.draw(screen)

        pygame.display.flip()