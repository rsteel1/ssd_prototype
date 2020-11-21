import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class ComplexityValidator:
    def validate(self, password, user=None):
        regex = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[-+_!@#$%^&*., ?]).+$"
        pattern = re.compile(regex)

        if not re.search(pattern, password):
            raise ValidationError(
                _(self.get_help_text()), code="password_not_complex_enough"
            )
        else:
            return ValidationError()

    def get_help_text(self):
        chars = list("-+_!@#$%^&*., ?")
        return _(
            f"Your password must contain a mixture of upper and lower-case letters, at least a single number, and a special character from the following list: {chars}."
        )
