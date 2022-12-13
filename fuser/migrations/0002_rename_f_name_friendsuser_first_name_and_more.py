# Generated by Django 4.1.1 on 2022-11-04 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fuser', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='friendsuser',
            old_name='f_name',
            new_name='first_name',
        ),
        migrations.RenameField(
            model_name='friendsuser',
            old_name='l_name',
            new_name='last_name',
        ),
        migrations.RemoveField(
            model_name='friendsuser',
            name='dOB',
        ),
        migrations.AddField(
            model_name='friendsuser',
            name='birth_date',
            field=models.DateField(null=True),
        ),
    ]