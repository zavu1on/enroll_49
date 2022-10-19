from django.contrib import admin

from . import models
from .services import calc_rating
# Register your models here.

admin.site.register(models.Exam)
admin.site.register(models.ProfileClass)
admin.site.register(models.ExtraAchievement)


class RatingListFilter(admin.SimpleListFilter):
    title = 'Рейтинг'
    parameter_name = 'sorting'

    def lookups(self, request, model_admin):
        return (
            ('with_rating', 'С рейтингом'),
            ('clear_rating', 'Обнулить рейтинг'),
        )

    def queryset(self, request, queryset):
        value = self.value()

        if value == 'with_rating':
            profile_id = None
            if 'profile_classes__id__exact' in request.GET:
                profile_id = request.GET['profile_classes__id__exact']

            for app in queryset.all():
                calc_rating(app, profile_id)
        elif value == 'clear_rating':
            for app in queryset.all():
                app.rating_place = 0
                app.save(update_fields=['rating_place'])

        return queryset


class ExtraAchievementInline(admin.StackedInline):
    model = models.ExtraAchievement
    extra = 0


@admin.register(models.EnrollApplication)
class EnrollApplicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'fio', 'get_profile_classes', 'status', 'rating_place')
    list_display_links = ('fio',)
    list_filter = ('profile_classes', 'status', RatingListFilter)
    ordering = ('-rating_place', 'id')
    readonly_fields = (
        'fio',
        'birthday',
        'address',
        'phone',
        'email',
        'passport_seria',
        'passport_number',

        # сведения о родителях
        'father_fio',
        'father_phone',
        'father_address',
        'mothers_fio',
        'mothers_phone',
        'mothers_address',

        # файлы
        'passport_file',
        'certificate_file',
        'marks_file',
        'exams_file',

        # прочие поля, заполняемые учеником
        'is_accepted',
        'notification_method',

        # поля, заполняемые администрацией лицея
        'created_date',
    )
    search_fields = ('fio',)
    search_help_text = 'Поиск по ФИО'
    inlines = (ExtraAchievementInline,)
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
                'father_phone',
                'father_address',
                'mothers_fio',
                'mothers_phone',
                'mothers_address',
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
        ('Выбраные профильные классы', {
            'fields': (
                'profile_classes',
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

    def get_profile_classes(self, application: models.EnrollApplication):
        return ', '.join([cls.name for cls in application.profile_classes.all()])

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        return super(EnrollApplicationAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)

    get_profile_classes.short_description = 'Профильные классы'
