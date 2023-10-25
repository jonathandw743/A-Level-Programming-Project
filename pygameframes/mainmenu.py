import pygame

from geometry.vector import Vector

from users.user import User

from .button import Button

from .levelselect import level_select
from .options import options

def main_menu(screen, user, on_save):

    WIDTH = screen.get_width()
    HEIGHT = screen.get_height()

    FPS = 60

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)

    clock = pygame.time.Clock()

    my_font = pygame.font.SysFont("Comic Sans MS", 20)

    logo_image = pygame.image.load("assets/logosmall.png")

    level_select_button = Button(
        "level_select",
        WIDTH / 2,
        6 * HEIGHT / 10,
        100,
        20,
        lambda : level_select(screen, user, on_save),
        my_font,
        WHITE,
    )

    options_button = Button(
        "options",
        WIDTH / 2,
        7 * HEIGHT / 10,
        100,
        20,
        lambda : options(screen, user),
        my_font,
        WHITE,
    )

    def save_button_on_click():
        on_save()
        return 0

    save_button = Button(
        "save",
        WIDTH / 2,
        8 * HEIGHT / 10,
        100,
        20,
        save_button_on_click,
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
                level_select_button.check_mouse_down(mouse_pos)
                options_button.check_mouse_down(mouse_pos)
                save_button.check_mouse_down(mouse_pos)
            
            # check all buttons for mouse up
            if event.type == pygame.MOUSEBUTTONUP:
                screens_to_exit = level_select_button.check_mouse_up(mouse_pos)
                if screens_to_exit:
                    return screens_to_exit - 1
                screens_to_exit = options_button.check_mouse_up(mouse_pos)
                if screens_to_exit:
                    return screens_to_exit - 1
                screens_to_exit = save_button.check_mouse_up(mouse_pos)
                if screens_to_exit:
                    return screens_to_exit - 1
            
            if event.type == pygame.KEYDOWN:
                # go back if Esc clicked
                if event.key == pygame.K_ESCAPE:
                    return 0

        keys = pygame.key.get_pressed()

        screen.fill(BLACK)

        screen.blit(logo_image, (WIDTH / 2 - logo_image.get_width() / 2, 25))

        level_select_button.draw(screen)
        options_button.draw(screen)
        save_button.draw(screen)

        pygame.display.flip()

if __name__ == "__main__":

    WIDTH = 1000
    HEIGHT = 600

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    pygame.font.init()

    main_menu(screen, User.example(), lambda: None)

    # this will only run when all the screens have finished
    pygame.quit()