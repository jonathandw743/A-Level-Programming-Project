import pygame

from .button import Button

from geometry.vector import Vector


def a(screen):

    WIDTH = screen.get_width()
    HEIGHT = screen.get_height()

    FPS = 60

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)

    clock = pygame.time.Clock()

    # create a font
    my_font = pygame.font.SysFont("Comic Sans MS", 200)
    # render some text
    text_surface = my_font.render("A", False, WHITE)

    running = True
    while running:

        dt = clock.tick(FPS) * 0.001

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.KEYDOWN:
                # go back if Esc clicked
                if event.key == pygame.K_ESCAPE:
                    running = False

        keys = pygame.key.get_pressed()

        screen.fill(BLACK)

        # draw the text to the screen
        screen.blit(text_surface, (0, 0))

        pygame.display.flip()

def main_menu(screen):

    WIDTH = screen.get_width()
    HEIGHT = screen.get_height()

    FPS = 60

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)

    clock = pygame.time.Clock()

    def a_button_on_click():
        return a(screen)

    a_button = Button(
        "A",
        WIDTH / 2,
        HEIGHT / 2,
        100,
        100,
        a_button_on_click,
        pygame.font.SysFont("Comic Sans MS", 50),
        WHITE,
    )

    running = True
    while running:

        dt = clock.tick(FPS) * 0.001

        mouse_pos = Vector.from_tuple(pygame.mouse.get_pos())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.MOUSEBUTTONDOWN:
                a_button.check_mouse_down(mouse_pos)
            if event.type == pygame.MOUSEBUTTONUP:
                if a_button.check_mouse_up(mouse_pos):
                    return True
            if event.type == pygame.KEYDOWN:
                # go back if Esc clicked
                if event.key == pygame.K_ESCAPE:
                    return

        keys = pygame.key.get_pressed()

        screen.fill(BLACK)

        a_button.draw(screen)

        pygame.display.flip()

def main():

    WIDTH = 1000
    HEIGHT = 600

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    pygame.font.init()

    # go to root, allowing it to use the screen
    main_menu(screen)

    # this will only run when all the loop in the root screen has finished
    pygame.quit()


if __name__ == "__main__":
    main()
