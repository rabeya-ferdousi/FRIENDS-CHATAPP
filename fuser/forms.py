from django.contrib.auth.forms import forms
from fuser.models import FriendsUser
from django.forms.widgets import NumberInput
from django.contrib.auth.models import User

class FriendsUserForm(forms.ModelForm):
  genderChoice = [
      ('male', 'Male'),
      ('female', 'Female'),
      ('custom','Custom'),
  ]
  password = forms.CharField(max_length=20, widget=forms.PasswordInput)
  gender = forms.ChoiceField(widget=forms.RadioSelect, choices=genderChoice)
  dOB = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))
  class Meta:
      model = FriendsUser
      fields = [
          'f_name', 'l_name', 'email', 'password', 'gender', 'dOB']