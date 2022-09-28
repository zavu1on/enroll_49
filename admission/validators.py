from django.core.exceptions import ValidationError


def validate_is_true(value: bool):
    if not value:
        raise ValidationError('Вы не дали согласие на обработку данных')
