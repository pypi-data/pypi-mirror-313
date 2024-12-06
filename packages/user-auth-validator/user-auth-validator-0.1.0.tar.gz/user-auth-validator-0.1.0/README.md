# user-auth-validator

A Python library for validating usernames, emails, and passwords.

## Features
- Validate usernames (at least 6 characters long).
- Validate email addresses using regex.
- Validate passwords with rules:
  - At least one uppercase letter.
  - At least one lowercase letter.
  - At least one digit.
  - At least one special character.

## Installation
Install via pip:
```bash
pip install user-auth-validator
```

## Usage

```python
from user_auth_validator.validators import validate_username, validate_email, validate_password

# Validate username
validate_username("myuser")  # Raises ValueError if invalid

# Validate email
validate_email("test@example.com")  # Raises ValueError if invalid

# Validate password
validate_password("Password@123")  # Raises ValueError if invalid

```