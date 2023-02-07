import logging
import sys
import pandas
from time import time
from django.contrib import admin
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import redirect
from . import models
from .services import calc_rating
# Register your models here.

admin.site.register(models.Exam)
admin.site.register(models.ProfileClass)
admin.site.register(models.ExtraAchievement)
admin.site.register(models.Teacher)
admin.site.register(models.Statistic)

logger = logging.getLogger(__name__)


class ExtraAchievementInline(admin.StackedInline):
    model = models.ExtraAchievement
    extra = 0


@admin.action(description='Рассчитать рейтинг поступающих для выбранных заявление')
def calculate_rating(modeladmin, request, queryset):
    for app in queryset.all():
        calc_rating(app)


@admin.action(description='Обнулить рейтинг поступающих для выбранных заявление')
def zeroize_rating(modeladmin, request, queryset):
    for app in queryset.all():
        app.rating_place = 0
        app.save(update_fields=['rating_place'])


@admin.action(description='Сформировать Exel протокол для выбранных заявление')
def make_exel(modeladmin, request, queryset):
    data_frame = []

    for app in queryset.all():
        data_frame.append({
            'ФИО': app.fio,
            'Дата рождения': app.birthday,
            'Контактный номер телефона': app.phone,
            'Контактный адрес электронной почты': app.email,
            'Серия паспорта': app.passport_seria,
            'Номер паспорта': app.passport_number,
            'ФИО матери': app.mother_fio,
            'ФИО отца': app.father_fio,

            'Средний балл аттестата': app.certificate_average_score,
            'Баллы за экзамен по русскому языку': app.russian_exam_point,
            'Баллы за экзамен по математике': app.math_exam_point,
            'Экзамен по выбору № 1': app.first_profile_exam.name,
            'Баллы за экзамен по выбору № 1': app.first_profile_exam_point,
            'Экзамен по выбору № 2': app.second_profile_exam.name,
            'Баллы за экзамен по выбору № 2': app.second_profile_exam_point,
            'Рейтинг': app.rating_place
        })

    name = f'рейтинг.{time()}.csv'
    pandas.DataFrame(data_frame).to_csv(settings.CSV_PATH / name, index=False, encoding='utf16', sep='\t')

    return redirect(settings.MEDIA_URL + name)


@admin.action(description='Оповестить поступающих о результатах отбора (для выбранных заявление)')
def notify_applicants(modeladmin, request, queryset):
    for app in queryset.all():
        app: models.EnrollApplication

        try:
            send_mail(
                f'Результаты отбора в 10-й {app.profile_class.name} класс лицея № 49!',
                '',  # todo написать текст
                settings.EMAIL_HOST_USER,
                [app.email],
            )
        except:
            logger.error(f'Ошибка во время отправки сообщения на почту {app.email}')


@admin.register(models.EnrollApplication)
class EnrollApplicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'fio', 'profile_class', 'status', 'rating_place')
    list_per_page = sys.maxsize
    list_display_links = ('fio',)
    list_filter = ('profile_class', 'status')
    ordering = ('-rating_place', 'id')
    readonly_fields = ('created_date',)
    search_fields = ('fio',)
    search_help_text = 'Поиск по ФИО'
    inlines = (ExtraAchievementInline,)
    actions = [calculate_rating, zeroize_rating, make_exel, notify_applicants]
    fieldsets = (
        ('Сведения о ребёнке', {
            'fields': (
                'fio',
                'birthday',
                'address',
                'phone',
                'email',
                'passport_seria',
                'passport_number',
                'created_date',
            )
        }),
        ('Cведения о родителях ребёнка', {
            'fields': (
                'father_fio',
                'father_phone', 'father_address',
                'mother_fio',
                'mother_phone',
                'mother_address',
            )
        }),
        ('Cведения об результатах обучения ребёнка', {
            'fields': (
                'certificate_average_score',
                'russian_exam_point',
                'russian_exam_mark',
                'math_exam_point',
                'math_exam_mark',
                'first_profile_exam',
                'first_profile_exam_point',
                'first_profile_exam_mark',
                'second_profile_exam',
                'second_profile_exam_point',
                'second_profile_exam_mark',
            )
        }),
        ('Выбранный профильный класс', {
            'fields': (
                'profile_class',
            )
        }),
        ('Файлы', {
            'fields': (
                'passport_file',
                'certificate_file',
                'marks_file',
                'exams_file',
            )
        }),
        ('Прочие поля, заполняемые учеником', {
            'fields': (
                'is_accepted',
                'notification_method',
            )
        }),
        ('Поля, заполняемые администрацией лицея', {
            'fields': (
                'status',
                'rating_place',
                'message',
            )
        }),
    )

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        return super(EnrollApplicationAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)
