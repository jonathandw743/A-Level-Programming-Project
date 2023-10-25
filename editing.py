from pickle import dump
from users.user import User

with open("users/users.p", "wb") as f:
    dump([User.example()], f)