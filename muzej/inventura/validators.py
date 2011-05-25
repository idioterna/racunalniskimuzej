from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

validate_ime = RegexValidator(
		regex=r"\w+, \w+( \w+)*",
		message="Uporabi obliko 'Priimek, Ime'")
