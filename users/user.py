class User:
    def __init__(self, username, password):
        
        self.username = username
        self.password = password
        self.progression = {}

    def __str__(self):
        return f'username: {self.username}, password: {self.password}, progression: {self.progression}'

    @staticmethod
    def example():
        return User("my_username", "very_secure_password")

if __name__ == "__main__":
    from picklefuncs import save_obj, load_obj

    users = load_obj(r"users/users.p")

    print([str(user) for user in users])

    from tkuiscreens.loginscreen import LoginScreen
    from tkuiscreens.optionsscreen import OptionsScreen
    from tkuiscreens.createaccountscreen import CreateAccountScreen
    from tkuiscreens.option import Option

    # logging when the user has logged in
    def on_login(user):
        print("login successful")
        print("user is " + str(user))

    # create and run the login screen, using the login logging function and allowing 3 attempts
    def run_login_screen():
        LoginScreen(users, on_login, attempts_allowed=3).mainloop()

    # creating and saving a new user
    def create_account(username, password):
        users.append(User(username, password))
        save_obj(users, r"./users.p")
        run_login_screen()

    # Create and run the create account screen using the create account logging function
    def run_create_account_screen():
        CreateAccountScreen(users, lambda password : len(password) >= 5, create_account).mainloop()

    OptionsScreen([
        Option("create account", run_create_account_screen),
        Option("login", run_login_screen)
    ]).mainloop()