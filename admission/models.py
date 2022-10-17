from django.db import models
from . import validators
# Create your models here.


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
        ('successes', 'Вы приняты'),
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
    phone = models.CharField('Контактный телефон', max_length=100, blank=True, unique=True)
    email = models.CharField('Контактный адрес электронной почты', max_length=300, blank=True, unique=True)
    passport_seria = models.PositiveIntegerField('Серия паспорта', validators=[validators.validate_password_seria])
    passport_number = models.PositiveIntegerField('Номер паспорта', validators=[validators.validate_password_number])

    # сведения о родителях
    father_fio = models.CharField('ФИО отца', max_length=300)
    father_phone = models.CharField('Контактный телефон отца', max_length=100)
    father_address = models.CharField('Адрес места жительства отца', max_length=500)
    mothers_fio = models.CharField('ФИО матери', max_length=300)
    mothers_phone = models.CharField('Контактный телефон матери', max_length=100)
    mothers_address = models.CharField('Адрес места жительства матери', max_length=500)

    # данные о результатах обучения ребенка
    certificate_average_score = models.FloatField('Средний балл аттестата')
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
    profile_classes = models.ManyToManyField(ProfileClass, verbose_name='Профильные классы')

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
    rating_place = models.FloatField(
        'Место в общем рейтинге',
        default=-1,
        help_text='Заполняется администрацией'
    )
    created_date = models.DateTimeField('Дата подачи заявки', auto_now=True)

    def __str__(self):
        return self.fio

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
