# Generated by Django 4.2.3 on 2023-07-21 09:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0002_alter_todo_date_completed'),
    ]

    operations = [
        migrations.RenameField(
            model_name='todo',
            old_name='date',
            new_name='date_created',
        ),
    ]
