# Generated by Django 3.2.8 on 2022-01-23 00:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_user_is_staff'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='completed_P1',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='completed_P2',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='completed_P3',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='completed_P4',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='completed_P5',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='completed_P6',
            field=models.BooleanField(default=False),
        ),
    ]