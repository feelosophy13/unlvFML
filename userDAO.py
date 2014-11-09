import hmac
import random
import string
import hashlib
import pymongo
import re


# The User Data Access Object handles all interactions with the User collection.
class UserDAO:

    def __init__(self, db):
        self.db = db
        self.users = self.db.users
        self.SECRET = 'verysecret'

    # makes a little salt
    def make_salt(self):
        salt = ""
        for i in range(5):
            salt = salt + random.choice(string.ascii_letters)
        return salt

    # implement the function make_pw_hash(name, pw) that returns a hashed password
    # of the format:
    # HASH(pw + salt),salt
    # use sha256

    def make_pw_hash(self, pw,salt=None):
        if salt == None:
            salt = self.make_salt();
        return hashlib.sha256(pw + salt).hexdigest()+","+ salt

    # Validates a user login. Returns user record or None
    def validate_login(self, email, password, errors):
        if not validate_email(email):
            errors['email_error'] = "Tsk, tsk. That's an invalid email address."
            return None

        user = None
        try:
            user = self.users.find_one({'e': email})
        except:
            pass

        if user is None:  # if user not in database
            errors['match_error'] = "What's happening? Something doesn't match."
            return None

        salt = user['p'].split(',')[1]

        if user['p'] != self.make_pw_hash(password, salt):  # if password doesn't a match
            errors['match_error'] = "What's happening? Something doesn't match."
            return None

        # Looks good
        return user


    # creates a new user in the users collection
    def add_user(self, email, username, password):

        password_hash = self.make_pw_hash(password)
        user = self.users.find_one({'$or': [{'u': username}, {'e': email}]})  # find user case that matches either by username or email ID

        if user is None:  # if no one else has the same username or email ID
            user = {'e': email, 'u': username, 'p': password_hash}  # then store email, user, and hashed password (not the actual password)
            try:
                self.users.insert(user, safe=True)
            except pymongo.errors.OperationFailure:  # mongo error
                return False
            return True
        else:  # if there is another user with that email ID or username, then return False
            return False


def validate_email(email):
    EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")

    if not EMAIL_RE.match(email):
        return False

    return True
