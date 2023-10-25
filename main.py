from picklefuncs import load_obj, save_obj
from tkuiscreens.option import Option
from tkuiscreens.createaccountscreen import CreateAccountScreen
from tkuiscreens.loginscreen import LoginScreen
from tkuiscreens.optionsscreen import OptionsScreen
from users.user import User
from geometry.rectangle import Rectangle
from pygameframes.mainmenu import main_menu
import pygame

USERS_FILE_PATH = r"users/users.p"


#################################################

#################################################


def save_users():
    save_obj(users, USERS_FILE_PATH)


def on_login(user):
    WIDTH = 1000
    HEIGHT = 600

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(f"playing as {user.username}")

    pygame.font.init()
    pygame.mixer.init()

    main_menu(screen, user, save_users)

    pygame.mixer.quit()

    # save progression pop-up
    OptionsScreen([
        Option("Save and exit", save_users),
        Option("Exit but don't save (progress may be lost)", lambda: None)
    ]).mainloop()

    # this will only run when all the screens have finished
    pygame.quit()



def run_login_screen():
    LoginScreen(users, on_login, 3).mainloop()


def password_filter(password):
    return len(password) > 5


def create_account(username, password):
    users.append(User(username, password))
    save_obj(users, USERS_FILE_PATH)
    run_login_screen()


def run_create_account_screen():
    CreateAccountScreen(users, password_filter, create_account).mainloop()


#################################################


users = load_obj(USERS_FILE_PATH)
OptionsScreen(
    [
        Option("Login", run_login_screen),
        Option("Create Account", run_create_account_screen),
    ]
).mainloop()
