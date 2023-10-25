# https://stacktuts.com/tkinter-boiler-plate
# for basic boilerplate

# A simple object oriented tkinter window
import tkinter as tk
from tkinter import ttk

class CreateAccountScreen(tk.Tk):
    def __init__(self, users, password_filter, on_done):
        super().__init__()

        # A list of disallowed usernames
        self.username_blacklist = [user.username for user in users]

        # A function that only returns true is the password is allowed
        self.password_filter = password_filter

        # What happens when the account is created
        self.on_done = on_done
        # Variables that can be used to control the contents of the screen
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.message = tk.StringVar()

        self.geometry("480x240")
        self.title("GOAT Create Account")

        # Username entry
        ttk.Label(self, text="Username:").pack()
        ttk.Entry(self, textvariable=self.username).pack()

        # Password entry
        ttk.Label(self, text="Password:").pack()
        ttk.Entry(self, textvariable=self.password).pack()

        # Submit button
        ttk.Button(self, text="Submit", command=self.on_submit).pack()

        # Any message to the user
        ttk.Label(self, textvariable=self.message).pack()

    def on_submit(self):
        # Disallow submit / account creation when the username entered already exists
        if self.username.get() in self.username_blacklist:
            self.message.set("Username taken")
            return
        # No spaces allowed
        if " " in self.username.get():
            self.message.set("Username cannot contain a space character")
            return
        if " " in self.password.get():
            self.message.set("Password cannot contain a space character.")
            return
        # Check the password using the password filter
        if not self.password_filter(self.password.get()):
            self.message.set("Password invalid. May be too short or doesn't contain certain characters.")
            return
        # Get rid of this screen and call the given function
        self.destroy()
        self.on_done(self.username.get(), self.password.get())