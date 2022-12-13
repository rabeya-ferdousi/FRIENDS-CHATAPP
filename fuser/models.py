from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
class FriendsUser(models.Model):#thik korte hbe user table theke ja ja already ase inherit kore ante hbe
   f_name = models.CharField(max_length=50)
   l_name = models.CharField(max_length=50)
   email = models.CharField(max_length=50)
   gender = models.CharField(max_length=10)
   password = models.CharField(max_length=50)
   dOB = models.DateField(null=True)
   f_uid = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
class Profile(models.Model):
   #name= models.ForeignKey(FriendsUser,on_delete=models.CASCADE,null=True)
   pic = models.ImageField(default='default.png',upload_to='picture', null=True)
   bio = models.CharField(max_length=50)
   f_uid = models.ForeignKey(FriendsUser, on_delete=models.CASCADE, null=True)
class FriendsWith(models.Model):
   a_uid = models.ForeignKey(User, on_delete=models.CASCADE, null=True,default= None, related_name='person2')
   b_uid = models.ForeignKey(User, on_delete=models.CASCADE, null=True,default= None)

class FriendsChat_Thread(models.Model):
   fChat = models.TextField(max_length=1000000)
   fChatTime = models.DateTimeField(default=datetime.now, blank=True)
   sender_Id = models.ForeignKey(FriendsUser, on_delete=models.CASCADE, null=True) # unclear
   threadId = models.ForeignKey(FriendsWith, on_delete=models.CASCADE, null=True, related_name='Thread')