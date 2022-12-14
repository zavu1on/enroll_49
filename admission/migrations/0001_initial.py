# Generated by Django 4.1.1 on 2022-10-28 11:40

import admission.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EnrollApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fio', models.CharField(max_length=300, verbose_name='ФИО')),
                ('birthday', models.DateField(verbose_name='Дата рождения')),
                ('address', models.CharField(max_length=500, verbose_name='Адрес места жительства')),
                ('phone', models.CharField(max_length=100, unique=True, verbose_name='Контактный телефон')),
                ('email', models.CharField(max_length=300, unique=True, verbose_name='Контактный адрес электронной почты')),
                ('passport_seria', models.PositiveIntegerField(validators=[admission.validators.validate_password_seria], verbose_name='Серия паспорта')),
                ('passport_number', models.PositiveIntegerField(validators=[admission.validators.validate_password_number], verbose_name='Номер паспорта')),
                ('father_fio', models.CharField(blank=True, max_length=300, null=True, verbose_name='ФИО отца')),
                ('father_phone', models.CharField(blank=True, max_length=100, null=True, verbose_name='Контактный телефон отца')),
                ('father_address', models.CharField(blank=True, max_length=500, null=True, verbose_name='Адрес места жительства отца')),
                ('mother_fio', models.CharField(blank=True, max_length=300, null=True, verbose_name='ФИО матери')),
                ('mother_phone', models.CharField(blank=True, max_length=100, null=True, verbose_name='Контактный телефон матери')),
                ('mother_address', models.CharField(blank=True, max_length=500, null=True, verbose_name='Адрес места жительства матери')),
                ('certificate_average_score', models.FloatField(validators=[admission.validators.validate_mark], verbose_name='Средний балл аттестата')),
                ('russian_exam_point', models.PositiveIntegerField(help_text='Первичные', verbose_name='Баллы за экзамен по русскому языку')),
                ('russian_exam_mark', models.PositiveIntegerField(validators=[admission.validators.validate_mark], verbose_name='Оценка за экзамен по русскому языку')),
                ('math_exam_point', models.PositiveIntegerField(help_text='Первичные', verbose_name='Баллы за экзамен по математике')),
                ('math_exam_mark', models.PositiveIntegerField(validators=[admission.validators.validate_mark], verbose_name='Оценка за экзамен по математике')),
                ('first_profile_exam_point', models.PositiveIntegerField(verbose_name='Баллы за экзамен по выбору № 1')),
                ('first_profile_exam_mark', models.PositiveIntegerField(validators=[admission.validators.validate_mark], verbose_name='Оценка за экзамен по выбору № 1')),
                ('second_profile_exam_point', models.PositiveIntegerField(verbose_name='Баллы за экзамен по выбору № 2')),
                ('second_profile_exam_mark', models.PositiveIntegerField(validators=[admission.validators.validate_mark], verbose_name='Оценка за экзамен по выбору № 2')),
                ('passport_file', models.FileField(upload_to='passport/', verbose_name='Паспорт')),
                ('certificate_file', models.FileField(upload_to='certificate/', verbose_name='Аттестат')),
                ('marks_file', models.FileField(upload_to='marks/', verbose_name='Оценки')),
                ('exams_file', models.FileField(upload_to='exams/', verbose_name='Результаты ОГЭ')),
                ('is_accepted', models.BooleanField(default=False, validators=[admission.validators.validate_is_true], verbose_name='Согласие на обработку персональных данных')),
                ('notification_method', models.CharField(choices=[('phone', 'По номеру телефона'), ('email', 'На электронную почту')], max_length=100, verbose_name='Метод оповещения о результатах')),
                ('status', models.CharField(choices=[('verification', 'В процессе верификации заявки'), ('processed', 'В процессе обработки заявки'), ('successes', 'Вы приняты'), ('rejected', 'Вы не приняты')], default='verification', help_text='Заполняется администрацией', max_length=100, verbose_name='Статус заявки')),
                ('message', models.TextField(blank=True, default='', verbose_name='Сообщение для учеников')),
                ('rating_place', models.FloatField(default=-1, help_text='Заполняется администрацией', verbose_name='Место в общем рейтинге')),
                ('created_date', models.DateTimeField(auto_now=True, verbose_name='Дата подачи заявки')),
            ],
            options={
                'verbose_name': 'Заявление на поступление в лицей',
                'verbose_name_plural': 'Заявления на поступление в лицей',
            },
        ),
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300, verbose_name='Название экзамена')),
            ],
            options={
                'verbose_name': 'Экзамен',
                'verbose_name_plural': 'Экзамены',
            },
        ),
        migrations.CreateModel(
            name='ProfileClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300, verbose_name='Название')),
                ('profile_exams', models.ManyToManyField(to='admission.exam', verbose_name='Профильные экзамены')),
            ],
            options={
                'verbose_name': 'Профильный класс',
                'verbose_name_plural': 'Профильные классы',
            },
        ),
        migrations.CreateModel(
            name='ExtraAchievement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='achievements/', verbose_name='Файл')),
                ('point', models.PositiveIntegerField(default=0, verbose_name='Баллы за достижение')),
                ('enroll_application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admission.enrollapplication', verbose_name='Заявление на поступление в лицей')),
            ],
            options={
                'verbose_name': 'Дополнительное достижение',
                'verbose_name_plural': 'Дополнительные достижения',
            },
        ),
        migrations.AddField(
            model_name='enrollapplication',
            name='first_profile_exam',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='first_profile_exam', to='admission.exam', verbose_name='Экзамен по выбору № 1'),
        ),
        migrations.AddField(
            model_name='enrollapplication',
            name='profile_class',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='admission.profileclass', verbose_name='Профильные классы'),
        ),
        migrations.AddField(
            model_name='enrollapplication',
            name='second_profile_exam',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='second_profile_exam', to='admission.exam', verbose_name='Экзамен по выбору № 2'),
        ),
    ]
