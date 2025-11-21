import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class ComplexPasswordValidator:
    """
    Require uppercase, lowercase, digit, and symbol characters in passwords.
    """

    def validate(self, password, user=None):
        if not re.search(r"[A-Z]", password or ""):
            raise ValidationError(_("Password must include at least one uppercase letter."), code="password_no_upper")
        if not re.search(r"[a-z]", password or ""):
            raise ValidationError(_("Password must include at least one lowercase letter."), code="password_no_lower")
        if not re.search(r"\d", password or ""):
            raise ValidationError(_("Password must include at least one digit."), code="password_no_digit")
        if not re.search(r"[^\w\s]", password or ""):
            raise ValidationError(_("Password must include at least one symbol."), code="password_no_symbol")

    def get_help_text(self):
        return _(
            "Your password must include at least one uppercase letter, one lowercase letter, one digit, and one symbol."
        )
