# Generated by Django 5.0.6 on 2024-08-10 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_usersubscribeedit_created_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersubscribeedit',
            name='subscriber_for',
            field=models.IntegerField(default=580, verbose_name='12 Aylık Ödeme Planı'),
        ),
        migrations.AlterField(
            model_name='usersubscribeedit',
            name='subscriber_one',
            field=models.IntegerField(default=50, verbose_name='Aylık Ödeme Planı'),
        ),
        migrations.AlterField(
            model_name='usersubscribeedit',
            name='subscriber_three',
            field=models.IntegerField(default=280, verbose_name='6 Aylık Ödeme Planı'),
        ),
        migrations.AlterField(
            model_name='usersubscribeedit',
            name='subscriber_two',
            field=models.IntegerField(default=140, verbose_name='Üç Aylık Planı'),
        ),
    ]
