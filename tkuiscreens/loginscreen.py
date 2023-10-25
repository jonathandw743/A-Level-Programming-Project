# https://stacktuts.com/tkinter-boiler-plate
# for basic boilerplate
import tkinter as tk
from tkinter import ttk

class LoginScreen(tk.Tk):
    def __init__(self, users, on_login, attempts_allowed):
        super().__init__()

        self.users = users
        self.on_login = on_login
        self.attempts_remaining = attempts_allowed
        self.password = tk.StringVar()
        self.username = tk.StringVar()
        self.message = tk.StringVar()
        self.message.set(
            f'Attempts Remaining: {self.attempts_remaining}')

        self.geometry("480x240")
        self.title("GOAT Login")

        # Create the username entry
        ttk.Label(self, text="Username:").pack()
        ttk.Entry(self, textvariable=self.username).pack()

        # Create the password entry
        ttk.Label(self, text="Password:").pack()
        ttk.Entry(self, textvariable=self.password).pack()

        # Create the submit button
        ttk.Button(self, text="Submit", command=self.on_submit).pack()

        # Message to the user
        ttk.Label(self, textvariable=self.message).pack()

    def set_message_to_attempts_remaining(self):
        self.message.set(
            f'Attemps Remaining: {self.attempts_remaining}')

    def on_submit(self):
        # return early if any of the entries are blank
        if self.username.get() == "" or self.password.get() == "":
            self.message.set("Not all required fields are filled")
            return
        
        # Check through all of the users to see if any of the login information matches
        for user in self.users:
            if user.username == self.username.get() and user.password == self.password.get():
                self.destroy()
                self.on_login(user)
        
        # Reset the username and password entries
        self.username.set("")
        self.password.set("")

        # Update the number of attempts remaining
        self.attempts_remaining -= 1
        self.set_message_to_attempts_remaining()
        if self.attempts_remaining <= 0:
            self.destroy()