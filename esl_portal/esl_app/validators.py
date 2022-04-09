from django.core.exceptions import ValidationError
from django.core.validators import validate_email, RegexValidator, validate_slug
from django.utils.translation import gettext_lazy as _


def validate_email_form(email):
    try:
        validate_email(email)
    except ValidationError:
        raise ValidationError(
            message=_('Invalid email: %(value)s'),
            code='email',
            params={'email': email}
        )


def validate_password(password):
    password_validator = RegexValidator(regex=r'^.*(?=.{8,})(?=.*[a-zA-Z])(?=.*\d)(?=.*[!#$%&? "]).*$')
    try:
        password_validator(password)
    except ValidationError:
        raise ValidationError(
            message=_('Invalid password format'),
            code='password',
        )


def validate_username(username):
    if len(username) < 3:
        raise ValidationError(
            message=_('Invalid username format: %(username)s'),
            code='username',
            params={'username': username}
        )
    try:
        validate_slug(username)
    except ValidationError:
        raise ValidationError(
            message=_('Invalid username format: %(username)s'),
            code='username',
            params={'username': username}
        )


def validate_firstname(firstname):
    firstname_validator = RegexValidator(r'^[a-zA-Z]$')
    try:
        firstname_validator(firstname)
    except ValidationError:
        raise ValidationError(
            message=_('Invalid firstname format: %(firstname)s'),
            code='username',
            params={'firstname': firstname}
        )
