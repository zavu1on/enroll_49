# Generated by Django 4.1.1 on 2023-04-16 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admission', '0007_siteconfiguration_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enrollapplication',
            name='rating_place',
            field=models.PositiveIntegerField(default=-1, help_text='Заполняется администрацией', verbose_name='Место в рейтинге'),
        ),
    ]
