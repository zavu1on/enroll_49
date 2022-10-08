from django.core.exceptions import ValidationError
from . import models


def validate_is_true(value: bool):
    if not value:
        raise ValidationError('Вы не дали согласие на обработку данных')


def validate_password_seria(value: int):
    if len(str(value)) != 4:
        raise ValidationError('Введите корректную серию паспорта')


def validate_password_number(value: int):
    if len(str(value)) != 6:
        raise ValidationError('Введите корректный номер паспорта')


def validate_password_exists(value: str):
    seria, number = value.split()

    try:
        models.EnrollApplication.objects.get(passport_seria=seria, passport_number=number)
    except models.EnrollApplication.DoesNotExist:
        raise ValidationError('Заявка не была найдена')


def validate_mark(value: int):
    if not (2 <= value <= 5):
        raise ValidationError('Введите корректную оценку за экзамен')
