# Generated by Django 3.2.8 on 2022-01-12 23:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('calendarapp', '0003_archivedevents'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='archivedevents',
            name='outfrnt_task',
        ),
    ]
