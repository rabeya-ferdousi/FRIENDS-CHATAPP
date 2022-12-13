# Generated by Django 4.1.1 on 2022-12-11 11:07

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('fuser', '0007_remove_profile_user_alter_friendschat_thread_fchat_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friendschat_thread',
            name='fChat',
            field=models.TextField(max_length=1000000),
        ),
        migrations.AlterField(
            model_name='friendschat_thread',
            name='fChatTime',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='friendschat_thread',
            name='sender_Id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='fuser.friendsuser'),
        ),
        migrations.AlterField(
            model_name='friendswith',
            name='a_uid',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='person2', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='friendswith',
            name='b_uid',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='profile',
            name='pic',
            field=models.ImageField(default='default.png', null=True, upload_to='picture'),
        ),
    ]