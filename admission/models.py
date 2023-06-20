import logging
from colorfield.fields import ColorField
from django.db import models
from django.conf import settings
from django.core.mail import send_mail
from solo.models import SingletonModel
from . import validators
# Create your models here.

logger = logging.getLogger(__name__)


class Exam(models.Model):
    """ Экзамен """

    name = models.CharField('Название экзамена', max_length=300)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Экзамен'
        verbose_name_plural = 'Экзамены'


class ProfileClass(models.Model):
    """ Профильный класс """

    name = models.CharField('Название', max_length=300)
    profile_exams = models.ManyToManyField(
        Exam,
        verbose_name='Профильные экзамены',
    )
    color = ColorField('Цвет карточки на сайте', default='#d9d9d9')
    competitive_places = models.PositiveIntegerField('Количество мест')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Профильный класс'
        verbose_name_plural = 'Профильные классы'


class EnrollApplication(models.Model):
    """ Заявление на поступление в лицей """
    STATUSES = (
        ('verification', 'В процессе верификации заявки'),
        ('processed', 'В процессе обработки заявки'),
        ('resolved', 'Определенно место в рейтинге'),
        ('success', 'Вы приняты'),
        ('rejected', 'Вы не приняты'),
    )
    NOTIFICATION_METHOD = (
        ('phone', 'По номеру телефона'),
        ('email', 'На электронную почту'),
    )

    # сведения о ребенке
    fio = models.CharField('ФИО', max_length=300)
    birthday = models.DateField('Дата рождения')
    address = models.CharField('Адрес места жительства', max_length=500)
    phone = models.CharField('Контактный номер телефона', max_length=100, unique=True)
    email = models.CharField('Контактный адрес электронной почты', max_length=300, unique=True)
    passport_seria = models.PositiveIntegerField('Серия паспорта', validators=[validators.validate_password_seria])
    passport_number = models.PositiveIntegerField('Номер паспорта', validators=[validators.validate_password_number])

    # сведения о родителях
    father_fio = models.CharField('ФИО отца', max_length=300, null=True, blank=True)
    father_phone = models.CharField('Контактный номер телефона отца', max_length=100, null=True, blank=True)
    father_address = models.CharField('Адрес места жительства отца', max_length=500, null=True, blank=True)
    mother_fio = models.CharField('ФИО матери', max_length=300, null=True, blank=True)
    mother_phone = models.CharField('Контактный номер телефона матери', max_length=100, null=True, blank=True)
    mother_address = models.CharField('Адрес места жительства матери', max_length=500, null=True, blank=True)

    # данные о результатах обучения ребенка
    certificate_average_score = models.FloatField('Средний балл аттестата', validators=[validators.validate_mark])
    russian_exam_point = models.PositiveIntegerField('Баллы за экзамен по русскому языку', help_text='Первичные')
    russian_exam_mark = models.PositiveIntegerField(
        'Оценка за экзамен по русскому языку',
        validators=[validators.validate_mark]
    )
    math_exam_point = models.PositiveIntegerField('Баллы за экзамен по математике', help_text='Первичные')
    math_exam_mark = models.PositiveIntegerField(
        'Оценка за экзамен по математике',
        validators=[validators.validate_mark]
    )
    profile_class = models.ForeignKey(ProfileClass, models.SET_NULL, verbose_name='Профильный класс', null=True)
    first_profile_exam = models.ForeignKey(
        Exam,
        models.SET_NULL,
        verbose_name='Экзамен по выбору № 1',
        null=True,
        related_name='first_profile_exam'
    )
    first_profile_exam_point = models.PositiveIntegerField('Баллы за экзамен по выбору № 1')
    first_profile_exam_mark = models.PositiveIntegerField(
        'Оценка за экзамен по выбору № 1',
        validators=[validators.validate_mark]
    )
    second_profile_exam = models.ForeignKey(
        Exam,
        models.SET_NULL,
        verbose_name='Экзамен по выбору № 2',
        null=True,
        related_name='second_profile_exam'
    )
    second_profile_exam_point = models.PositiveIntegerField('Баллы за экзамен по выбору № 2')
    second_profile_exam_mark = models.PositiveIntegerField(
        'Оценка за экзамен по выбору № 2',
        validators=[validators.validate_mark]
    )

    # файлы
    passport_file = models.FileField('Паспорт', upload_to='passport/')
    certificate_file = models.FileField('Аттестат', upload_to='certificate/')
    marks_file = models.FileField('Оценки', upload_to='marks/')
    exams_file = models.FileField('Результаты ОГЭ', upload_to='exams/')

    # прочие поля, заполняемые учеником
    is_accepted = models.BooleanField(
        'Согласие на обработку персональных данных',
        default=False,
        validators=[validators.validate_is_true]
    )
    notification_method = models.CharField(
        'Метод оповещения о результатах',
        max_length=100,
        choices=NOTIFICATION_METHOD
    )

    # поля, заполняемые администрацией лицея
    status = models.CharField(
        'Статус заявки',
        max_length=100,
        choices=STATUSES,
        default='verification',
        help_text='Заполняется администрацией'
    )
    message = models.TextField('Сообщение для учеников', default='', blank=True)
    rating_place = models.PositiveIntegerField(
        'Место в рейтинге',
        default=0,
        help_text='Заполняется системой'
    )
    created_date = models.DateTimeField('Дата подачи заявки', auto_now=True)

    def __str__(self):
        return self.fio

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        try:
            prev_app = EnrollApplication.objects.get(pk=self.id)
        except Exception as e:
            return super().save(force_insert, force_update, using, update_fields)

        if self.message.strip() and prev_app.message != self.message:
            try:
                message = f'' \
f'Приёмная комиссия написал Вам сообщение, по поводу Вашей заявки. ' \
f'Также посмотреть сообщение можно в личном кабинете.<br><br>' \
f'"{self.message}"'

                send_mail(
                    'Поступление в 10 класс лицея № 49. Новое сообщение от приемной комиссии',
                    '',
                    settings.EMAIL_HOST_USER,
                    [self.email],
                    html_message=message
                )
            except:
                logger.error(f'Ошибка во время отправки сообщения на почту {self.email}')

        return super().save(force_insert, force_update, using, update_fields)

    class Meta:
        verbose_name = 'Заявление на поступление в лицей'
        verbose_name_plural = 'Заявления на поступление в лицей'


class ExtraAchievement(models.Model):
    """ Дополнительные достижения """

    file = models.FileField('Файл', upload_to='achievements/')
    point = models.PositiveIntegerField('Баллы за достижение', default=0)
    enroll_application = models.ForeignKey(EnrollApplication, models.CASCADE, verbose_name='Заявление на поступление в лицей')

    def __str__(self):
        return self.file.name

    class Meta:
        verbose_name = 'Дополнительное достижение'
        verbose_name_plural = 'Дополнительные достижения'


class Teacher(models.Model):
    fio = models.CharField('ФИО учителя', max_length=300, help_text='В формате: "Фамилия И.О."')
    lesson = models.CharField('Предмет', max_length=300)
    photo = models.ImageField('Фотография', upload_to='teachers/')

    def __str__(self):
        return self.fio

    class Meta:
        verbose_name = 'Учитель'
        verbose_name_plural = 'Учителя'


class Statistic(models.Model):
    name = models.CharField('Название профильного класса', max_length=300)
    number_of_received = models.PositiveIntegerField('Количество поступивших')
    number_of_graduates = models.PositiveIntegerField('Количество выпустившихся')
    number_of_medalists = models.PositiveIntegerField('Количество выпустившихся медалистов')
    number_of_state_employees = models.PositiveIntegerField('Количество выпустившихся бюджетников')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Статистика'
        verbose_name_plural = 'Статистики'


class SiteConfiguration(SingletonModel):
    can_make_applications = models.BooleanField(
        'Могут ли дети подавать заявки',
        help_text='Если НЕТ, функицонал личного кабинета и формы поступления будет не доступен',
        default=False
    )
    get_documents_date = models.DateField(
        'Дата приема документов, предварительно поступивших учеников',
        help_text='Отображается в email-е',
        null=True,
        blank=True
    )
    conflict_commission_date = models.DateField(
        'Дата сбора конфликтной комиссии',
        help_text='Отображается в email-е',
        null=True,
        blank=True
    )
    start_conflict_commission_time = models.TimeField(
        'Время начала конфликтной комисси',
        help_text='Отображается в email-е',
        null=True,
        blank=True
    )
    end_conflict_commission_time = models.TimeField(
        'Время окончания конфликтной комисси',
        help_text='Отображается в email-е',
        null=True,
        blank=True
    )

    def __str__(self):
        return 'Да' if self.can_make_applications else 'Нет'

    class Meta:
        verbose_name = verbose_name_plural = 'Конфигурация'
