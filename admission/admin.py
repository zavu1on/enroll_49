import logging
import sys
from functools import reduce
import pandas
from time import time
from django.contrib import admin
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import redirect
from solo.admin import SingletonModelAdmin
from . import models
from .models import ExtraAchievement, EnrollApplication, SiteConfiguration

# Register your models here.

admin.site.register(models.Exam)
admin.site.register(models.ProfileClass)
admin.site.register(models.ExtraAchievement)
admin.site.register(models.Teacher)
admin.site.register(models.Statistic)

admin.site.register(models.SiteConfiguration, SingletonModelAdmin)

logger = logging.getLogger(__name__)


class ExtraAchievementInline(admin.StackedInline):
    model = models.ExtraAchievement
    extra = 0


@admin.action(description='Рассчитать рейтинг поступающих для выбранных заявление')
def calculate_rating(modeladmin, request, queryset):
    rating_dict = {}

    for application in queryset.all():
        k1 = application.certificate_average_score
        k2 = sum([
            application.russian_exam_point,
            application.math_exam_point,
            application.first_profile_exam_point,
            application.second_profile_exam_point,
        ]) / 4
        k3_4 = reduce(lambda prev, new: prev + new.point,
                      ExtraAchievement.objects.filter(enroll_application=application), 0)

        exams = map(lambda el: el.name, application.profile_class.profile_exams.all())

        if 'Русский язык' in exams:
            k2 = sum([
                application.russian_exam_point,
                application.russian_exam_point,
                application.math_exam_point,
                application.first_profile_exam_point,
                application.second_profile_exam_point,
            ]) / 5
        elif 'Математика' in exams:
            k2 = sum([
                application.russian_exam_point,
                application.russian_exam_point,
                application.math_exam_point,
                application.first_profile_exam_point,
                application.second_profile_exam_point,
            ]) / 5

        rating_dict[application.id] = k1 + k2 + k3_4
    sorted_rating_list = sorted(rating_dict.items(), key=lambda el: el[1])

    for idx, val in enumerate(sorted_rating_list):
        application = queryset.get(id=val[0])

        application.rating_place = len(sorted_rating_list) - idx
        application.save(update_fields=['rating_place'])


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
        app: EnrollApplication
        status_text = ''

        for s in EnrollApplication.STATUSES:
            if s[0] == app.status:
                status_text = s[1]
                break

        try:
            solo = SiteConfiguration.get_solo()
            message = '' \
f'Текущий статус Вашего заявления в 10 {app.profile_class.name.lower()} класс лицея № 49 - <b>{status_text}</b>'

            if app.status == 'success':
                message = f'' \
f'Вы приняты в 10 {app.profile_class.name.lower()} класс лицея № 49! ' \
f'Подробности Вашего заявления Вы сможете узнать в личном кабинете.<br><br>' \
f'Ждем Вас в лицее по адресу Калининград, ул. Кирова, 28 <b>{solo.get_documents_date.strftime("%d.%m.%Y")} с 9:00 до 15:00</b>!<br><br>' \
f'В личном кабинете Вы сможете найти <b>список ОБЯЗАТЕЛЬНОЙ литературы на 10 класс!</b>'

            elif app.status == 'rejected':
                message = f'' \
f'К сожалению, Вы не прошли рейтинговый отбор в 10 {app.profile_class.name.lower()} класс лицея № 49.' \
f'Подробности Вашего заявления Вы сможете узнать в личном кабинете.<br><br>' \
f'Если у Вас остались вопросы или Вы не согласны с решением приемной комисси, Вы можете обратиться в конфликтную комиссию ' \
f'в лицее по адресу Калининград, ул. Кирова, 28 <b>{solo.conflict_commission_date.strftime("%d.%m.%Y")} с {solo.start_conflict_commission_time.strftime("%H:%M")} до {solo.end_conflict_commission_time.strftime("%H:%M")}</b>!'


            send_mail(
                f'Обработка заявления в 10-й {app.profile_class.name.lower()} класс лицея № 49!',
                '',
                settings.EMAIL_HOST_USER,
                [app.email],
                html_message=message
            )
        except Exception as e:
            print(e)
            logger.error(f'Ошибка во время отправки сообщения на почту {app.email}')


@admin.register(models.EnrollApplication)
class EnrollApplicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'fio', 'profile_class', 'status', 'rating_place')
    list_per_page = sys.maxsize
    list_display_links = ('fio',)
    list_filter = ('profile_class', 'status')
    ordering = ('rating_place', 'fio')
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
