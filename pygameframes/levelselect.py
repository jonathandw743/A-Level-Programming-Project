import pygame

from users.user import User

from geometry.vector import Vector

from levels.level import Level
from levels.loadlevels import load_levels

from .button import Button
from .gameplay import gameplay


def level_select(screen, user, on_save):
    WIDTH = screen.get_width()
    HEIGHT = screen.get_height()

    FPS = 60

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)

    clock = pygame.time.Clock()

    # some big font to use (for testing)
    my_font = pygame.font.SysFont("Comic Sans MS", 50)

    # load levels from the json file
    levels = load_levels(r"levels/levels.json", r"levels/levelsorder.json")

    # a wrapper function to preserve the state of the level variable
    # so the level function doesn't change as the succeeding level buttons are being created
    def create_level_function(level):
        def level_function():
            return gameplay(screen, level, user, on_save)

        return level_function

    # function to create the level buttons

    def create_level_buttons():
        completed_text = "completed!"
        not_completed_text = "not completed"
        return [
            Button(
                f"Level {i + 1}, {not_completed_text if level.level_id not in user.progression or not user.progression[level.level_id].completed else completed_text}",
                400,
                200 + 100 * i,
                300,
                40,
                create_level_function(level),
                # (lambda level: lambda: gameplay(screen, level))(level),
                my_font,
                WHITE,
            ) for i, level in enumerate(levels)
        ]

    # create the level buttons
    level_buttons = create_level_buttons()


    # create some text to show what screen this is
    text_render = my_font.render("level_select", False, WHITE)

    running = True
    while running:
        dt = clock.tick(FPS) * 0.001

        # get the position of the mouse as a vector
        mouse_pos = Vector.from_tuple(pygame.mouse.get_pos())

        for event in pygame.event.get():
            # go all the way back if cross clicked
            if event.type == pygame.QUIT:
                return -1
            # check all buttons for mouse down
            if event.type == pygame.MOUSEBUTTONDOWN:
                for level_button in level_buttons:
                    level_button.check_mouse_down(mouse_pos)

            # check all buttons for mouse up
            if event.type == pygame.MOUSEBUTTONUP:
                for level_button in level_buttons:
                    # this will run the game code if the button is clicked
                    # and pass down the exit command if the cross is clicked
                    screens_to_exit = level_button.check_mouse_up(mouse_pos)
                    print(screens_to_exit)
                    if screens_to_exit:
                        return screens_to_exit - 1
                    # reload the buttons to show the progression when this screen is returned to from the gameplay
                    if screens_to_exit is not None:
                        level_buttons = create_level_buttons()

            if event.type == pygame.KEYDOWN:
                # go back if Esc clicked
                if event.key == pygame.K_ESCAPE:
                    return 0

        keys = pygame.key.get_pressed()

        screen.fill(BLACK)

        # display the screen identification text
        screen.blit(text_render, (0, 0))

        # draw all the level buttons
        for level_button in level_buttons:
            level_button.draw(screen)

        pygame.display.flip()


if __name__ == "__main__":
    WIDTH = 1000
    HEIGHT = 600

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    pygame.font.init()

    level_select(screen, User.example(), lambda: None)

    # this will only run when all the screens have finished
    pygame.quit()
