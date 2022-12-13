from django.db import models
from fuser.models import FriendsUser
from datetime import datetime
# Create your models here.
# class RoboFriend(models.Model):
#     nickName = models.CharField(max_length=40)

class RoboChat_Thread(models.Model):
    f_uid = models.ForeignKey(FriendsUser, on_delete=models.CASCADE, null=True)
    #r_id = models.ForeignKey(RoboFriend, on_delete=models.CASCADE, null=True)

class RoboChat(models.Model):
    user_chat = models.TextField(max_length=10000000,default=None)
    robo_chat = models.TextField(max_length=10000000,default=None)
    chatTime = models.DateTimeField(default=datetime.now, blank=True)
    threadId = models.ForeignKey(RoboChat_Thread, on_delete=models.CASCADE, null=True,related_name='thread')
