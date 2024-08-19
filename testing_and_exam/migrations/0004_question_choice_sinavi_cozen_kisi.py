# Generated by Django 5.0 on 2024-06-16 23:03

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testing_and_exam', '0003_alter_ayt_choice_options_alter_ayt_result_options_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='question_choice',
            name='sinavi_cozen_kisi',
            field=models.ManyToManyField(blank=True, default=None, max_length=100, null=True, related_name='sinavi_cozen_kisi', to=settings.AUTH_USER_MODEL, verbose_name='SINAV ADI'),
        ),
    ]
