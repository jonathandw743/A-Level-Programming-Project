import pygame

from users.user import User

from levels.levelprogression import LevelProgression

from geometry.rectangle import Rectangle
from geometry.vector import Vector

from game.player import Player
from game.camera import Camera
#// from game.gamestate import GameState

from .pausemenu import pause_menu
from .gameover import game_over
from .levelcomplete import level_complete


def gameplay(screen, level, user, on_save):

    WIDTH = screen.get_width()
    HEIGHT = screen.get_height()

    FPS = 60

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)

    jump_sound = pygame.mixer.Sound("assets/jumpsound.wav")

    # create a new level progression object for this user in this level, if one doesn't already exist
    if level.level_id not in user.progression:
        user.progression[level.level_id] = LevelProgression(level)
    
    # load some game state from the user's current progression
    player = user.progression[level.level_id].game_state.get()
    # update clock so time isn't saved from the previous load
    clock = pygame.time.Clock()

    def respawn_player():
        user.progression[level.level_id].game_state.respawn(level)
        return user.progression[level.level_id].game_state.get()

    camera = Camera(
        0, 0, WIDTH, HEIGHT, game_space_visible_height=20
    )

    has_completed = False

    def before_exit():
        if not user.progression[level.level_id].completed:
            user.progression[level.level_id].completed = has_completed
        
        user.progression[level.level_id].game_state.update(player)

    running = True

    while running:
        dt = clock.tick(FPS) * 0.001

        should_continue_due_to_event = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                before_exit()
                return -1

            if event.type == pygame.KEYDOWN:
                # go to the pause menu if Esc pressed
                if event.key == pygame.K_ESCAPE:
                    before_exit()
                    print(user.progression[level.level_id].game_state.player.rect.pos.x)
                    screens_to_exit = pause_menu(screen, on_save)
                    if screens_to_exit:
                        return screens_to_exit - 1
                    
                    should_continue_due_to_event = True
        
        if should_continue_due_to_event:
            clock = pygame.time.Clock()
            continue
                    
                    

        keys = pygame.key.get_pressed()

        screen.fill(BLACK)

        player.reset_acc()

        # acceleration
        player.gravity(100)
        player.move_horizontal(
            left_input=keys[pygame.K_a],
            right_input=keys[pygame.K_d],
            grounded_speed=150,
            ungrounded_speed=10,
        )
        player.jump(
            jump_input=keys[pygame.K_SPACE],
            power=35,
            dt=dt,
            play_jump_sound=jump_sound.play,
        )
        # player.air_resistance(power=0.5)
        player.ground_friction(power=10)

        # update displacement and velocity
        player.update_displacement_and_velocity(dt)

        player.reset_grounded()

        # collisions
        for p in level.platforms:
            player.collide_with_rectangle(p)

        # check whether the player has hit a kill box
        hit_kill_box = False
        for k in level.kill_boxes:
            if player.rectangle_collision_detection(k):
                hit_kill_box = True

        # go to game over screen if it has hit a kill box
        if hit_kill_box:
            before_exit()
            screens_to_exit = game_over(screen)
            if screens_to_exit:
                return screens_to_exit - 1

            # reset the level
            player = respawn_player()
            clock = pygame.time.Clock()

            continue

        if player.rectangle_collision_detection(level.target):
            # // print("level completed")
            has_completed = True

            before_exit()
            screens_to_exit = level_complete(screen)
            if screens_to_exit:
                return screens_to_exit - 1

            # reset the level
            player = respawn_player()
            clock = pygame.time.Clock()

            continue

        if not player.is_in_bounds(level.bounds):
            before_exit()
            screens_to_exit = game_over(screen)
            if screens_to_exit:
                return screens_to_exit - 1

            # reset the level
            player = respawn_player()
            clock = pygame.time.Clock()

            continue

        # update position
        player.update_position()

        camera.pos = player.rect.pos

        # draw the platforms
        for p in level.platforms:
            pygame.draw.rect(
                screen,
                BLUE,
                camera.game_space_to_screen_space_corner_rect_tuple(
                    p.corner_rect_tuple()
                ),
            )

        # draw the kill boxes
        for k in level.kill_boxes:
            pygame.draw.rect(
                screen,
                RED,
                camera.game_space_to_screen_space_corner_rect_tuple(
                    k.corner_rect_tuple()
                ),
            )

        pygame.draw.rect(
            screen,
            GREEN,
            camera.game_space_to_screen_space_corner_rect_tuple(
                level.target.corner_rect_tuple()
            ),
        )

        pygame.draw.rect(
            screen,
            WHITE,
            camera.game_space_to_screen_space_corner_rect_tuple(
                player.rect.corner_rect_tuple()
            ),
        )

        pygame.display.flip()


#####################################################################################

###################################################################################

if __name__ == "__main__":
    from levels.loadlevels import load_levels

    WIDTH = 1000
    HEIGHT = 600

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    pygame.font.init()

    gameplay(
        screen,
        load_levels(r"levels/levels.json", r"levels/levelsorder.json")[0],
        User.example(),
        lambda: None,
    )

    # this will only run when all the screens have finished
    pygame.quit()
