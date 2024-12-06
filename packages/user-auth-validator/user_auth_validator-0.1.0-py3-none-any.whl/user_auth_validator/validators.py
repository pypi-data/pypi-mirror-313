import re

def validate_username(username):
    """
    Validates that a username is at least 6 characters long.
    :param username: The username to validate.
    :return: True if valid, raises ValueError if invalid.
    """
    if len(username) < 6:
        raise ValueError("Username must be at least 6 characters long.")
    return True

def validate_email(email):
    """
    Validates an email address.
    :param email: The email to validate.
    :return: True if valid, raises ValueError if invalid.
    """
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(email_regex, email):
        raise ValueError("Invalid email format.")
    return True

def validate_password(password):
    """
    Validates a password with the following rules:
    - At least one uppercase letter.
    - At least one lowercase letter.
    - At least one digit.
    - At least one special character.
    :param password: The password to validate.
    :return: True if valid, raises ValueError if invalid.
    """
    if not any(char.isupper() for char in password):
        raise ValueError("Password must contain at least one uppercase letter.")
    if not any(char.islower() for char in password):
        raise ValueError("Password must contain at least one lowercase letter.")
    if not any(char.isdigit() for char in password):
        raise ValueError("Password must contain at least one digit.")
    if not any(char in "!@#$%^&*()-_+=<>?/|{}[]~`" for char in password):
        raise ValueError("Password must contain at least one special character.")
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters long.")
    return True
