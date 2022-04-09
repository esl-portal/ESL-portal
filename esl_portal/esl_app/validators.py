from django.core.exceptions import ValidationError
from django.core.validators import validate_email, RegexValidator, validate_slug


def validate_email_form(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False


def validate_password(password):
    password_validator = RegexValidator(regex=r'^.*(?=.{8,})(?=.*[a-zA-Z])(?=.*\d)(?=.*[!#$%&? "]).*$')
    try:
        password_validator(password)
        return True
    except ValidationError:
        return False


def validate_username(username):
    if len(username) < 3:
        return False
    try:
        validate_slug(username)
        return True
    except ValidationError:
        return False


def validate_firstname(firstname):
    firstname_validator = RegexValidator(r'^[a-zA-Z]$')
    try:
        firstname_validator(firstname)
        return True
    except ValidationError:
        return False
