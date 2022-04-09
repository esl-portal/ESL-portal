from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, validate_slug, EmailValidator


def validate_email(email):
    email_validator = EmailValidator(message="Некорректный формат email")
    try:
        email_validator(email)
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
