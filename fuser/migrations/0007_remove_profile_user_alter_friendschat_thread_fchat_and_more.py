# Generated by Django 4.1.1 on 2022-12-11 11:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fuser', '0006_profile_bio'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='user',
        ),
        migrations.AlterField(
            model_name='friendschat_thread',
            name='fChat',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='friendschat_thread',
            name='fChatTime',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='friendswith',
            name='a_uid',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='person2', to='fuser.profile'),
        ),
        migrations.AlterField(
            model_name='friendswith',
            name='b_uid',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='person1', to='fuser.profile'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='bio',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='profile',
            name='pic',
            field=models.ImageField(upload_to=''),
        ),
    ]
