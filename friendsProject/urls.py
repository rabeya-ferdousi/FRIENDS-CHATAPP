
"""pythonProject URL Configuration

The urlpatterns list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import home.views as hv

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',hv.loadpage,name='load'),
    path('loadout/',hv.loadpage,name='loadout'),
    path('login/', hv.login, name='login'),#
    path('signup/', hv.signup, name='signup'),#done
    path('homepage/<str:user_name>/profile/', hv.profile, name='profile'),#done
    path('homepage/<str:user_name>/', hv.home_screen, name='homepage'),
    path('homepage/<str:user_name>/addfriend/', hv.add_friend_page, name='addfriend'),#done
    path('homepage/<str:user_name>/<str:friend_name>/<str:friends_id>/inbox/', hv.inbox_page, name='inbox'),
    path('homepage/<str:user_name>/botchat/', hv.chat_with_bot_page, name='botchat'),
    path('homepage/<int:userid>/<int:friends_id>/profile/<str:friend_name>', hv.profile_show, name='profile_show'),#done
    path('homepage/<str:user_name>/ResetPassword', hv.password_reset, name='password'),  #done
]

