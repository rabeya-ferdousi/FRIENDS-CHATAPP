from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from fuser.forms import FriendsUserForm
from fuser.models import FriendsUser, FriendsWith, FriendsChat_Thread, Profile
from django.contrib import messages
import re
import random
from robo.models import RoboChat_Thread, RoboChat
# Create your views here.
def signup(request):

   if(request.method == 'POST'):
       form = FriendsUserForm(request.POST)
       if form.is_valid():
        #work for user table start
        fname = request.POST['f_name']
        lname = request.POST['l_name']
        passw = request.POST['password']
        em = request.POST['email']
        name = fname+em
        if User.objects.filter(username=name).exists():
            messages.error(request, 'The person with this email is already a member...')
        else:
            user = User(password=passw, username=name, email=em, last_name=lname, first_name=fname)
            user.save()
            #end
            #for friends user table

            gndr = request.POST['gender']
            bd = request.POST['dOB']
            user1 = User.objects.all()
            get_user = user1.get(email=em)
            friendUser = FriendsUser(f_name=fname, l_name=lname, email=em,gender=gndr,password=passw, dOB=bd, f_uid=get_user)
            friendUser.save()
            return redirect('login')
   form = FriendsUserForm()
   context = {'User_form': form, }

   return render(request, 'signup.html', context)

# Create your views here.

def login(request):
    if (request.method == 'POST'):
        user_email = request.POST['email']
        upassword = request.POST['pass-word']
        if User.objects.filter(email=user_email).exists():
            user1 = User.objects.filter(email=user_email)
            for user in user1:
                if user.password == upassword:
                    messages.success(request, 'Sucessfully Logged In.')
                    return redirect('homepage',user_name=user.username)
                else:
                    messages.error(request, 'Incorrect Password !! ')
        else:
            messages.error(request, 'Username does not exist. ')
    return render(request, 'login.html')
def home_screen(request, user_name):
    if (request.method == 'POST'):
        iemail = request.POST['email']
        useri=User.objects.get(username=user_name)
        if User.objects.filter(email=iemail).exists():
            usery = User.objects.get(email=iemail)
            flag=0
            if useri is not None and usery is not None:
                fid1 = FriendsWith.objects.filter(a_uid=useri)
                for fi in fid1:
                    if (fi.b_uid==usery):
                        flag=1
                        friendsid=fi.id
                        break
                fid1 = FriendsWith.objects.filter(b_uid=useri)
                for fi in fid1:
                    if (fi.a_uid == usery):
                        friendsid = fi.id
                        flag = 1
                        break
                if flag==1:
                    return redirect('inbox', friend_name=usery.first_name+' '+usery.last_name,friends_id=str(friendsid),user_name=useri.username)
                else:
                    messages.error(request, 'you are not friends with this person !! ')
        else:
            messages.error(request, 'NO SUCH PERSON EXISTS !!')

    return render(request, 'home.html', { 'user_name': user_name, })


def inbox_page(request, friend_name, friends_id, user_name):
    list= getMessages( request ,friend_id=friends_id)
    user = User.objects.get(username=user_name)
    userid = user.id
    if (request.method == 'POST'):
        message = request.POST['message']
        if message != '':
            fuser = FriendsUser.objects.get(f_uid=userid)
            friends = FriendsWith.objects.get(id=friends_id)
            new_message = FriendsChat_Thread(fChat=message, sender_Id=fuser, threadId=friends)
            new_message.save()
            list = getMessages(request, friend_id=friends_id)
    return render(request, 'inbox.html', {'friend_name':friend_name,
                                          'user_name':user_name,
                                          'friends_id':friends_id,
                                          'messages': list,
                                          'userid':userid})

def add_friend_page(request,user_name):
    if User.objects.filter(username=user_name).exists():
        user=User.objects.get(username=user_name)
        user_email=user.email
        if (request.method == 'POST'):
            yemail = request.POST['yemail']
            if yemail==user_email:
                femail = request.POST['femail']
                value ='T'
                user = FriendsUser.objects.all()
                if( yemail != femail):
                    if(user.filter(email=yemail).exists() and user.filter(email=femail).exists()):
                        us1=User.objects.get(email=yemail)
                        us2=User.objects.get(email=femail)
                        fi1= FriendsWith.objects.filter(a_uid=us1)
                        for fi in fi1:
                            if fi.b_uid == us2:
                                value ='f'
                                break
                        fi1 = FriendsWith.objects.filter(b_uid=us1)
                        for fi in fi1:
                            if fi.a_uid == us2:
                                value = 'f'
                                break
                        if value == 'T':
                            u1 = FriendsWith(a_uid=us1, b_uid=us2)
                            u1.save()
                            return redirect('homepage', user_name=us1)
                        else:
                            messages.error(request, 'ALREARDY A FRIEND !! ')
                    else:
                        messages.error(request, 'THE PERSON DO NOT EXIST!')
                else:
                    messages.error(request, 'INVALID INPUT!')
            else:
                messages.error(request, 'you can add friend to your account only !!!')

    return render(request, 'addfriend.html', { 'user_name': user_name, })


def loadpage(request):
    return render(request,'loadpage.html')
def profile(request,user_name):
    user = User.objects.get(username=user_name)
    fuser = FriendsUser.objects.get(f_uid=user.id)
    if (request.method == 'POST'):
        bioa = request.POST['bio']
        if bioa != '':
        # to check if the profile already exists
            if Profile.objects.filter(f_uid=fuser.id).exists():
                p = Profile.objects.get(f_uid=fuser.id)
                p.bio = bioa
                p.save()
            else:
                pro = Profile(bio=bioa, f_uid=fuser)
                pro.save()
    prof = Profile.objects.filter(f_uid=fuser.id)
    if(prof.exists()):
        p = Profile.objects.get(f_uid=fuser.id)
        Name =str(fuser.f_name+" "+fuser.l_name).upper()
        BOd = fuser.dOB
        bio = p.bio
        email = fuser.email
        gender=str(fuser.gender).upper()
    else:
        Name =str(fuser.f_name+" "+fuser.l_name).upper()
        BOd =fuser.dOB
        bio="USER HAS NOT ADDED ANY BIO OR PIC YET!!!!"#hi i am oishi
        email=fuser.email
        gender=str(fuser.gender).upper()
    return render(request, 'profile.html', { 'user_name': user_name,
                                             'name': Name,
                                             'bod': BOd,
                                             'bio':bio,
                                             'email':email,
                                             'gender':gender})
def profile_show(request,userid,friends_id,friend_name):
    frindship=FriendsWith.objects.get(id=friends_id)
    usera=(frindship.a_uid).id
    userb=(frindship.b_uid).id
    if usera == userid:
        friend = userb
    else:
        friend = usera
    user = User.objects.get(id=friend)
    fuser = FriendsUser.objects.get(f_uid=user.id)
    prof = Profile.objects.filter(f_uid=fuser.id)
    if(prof.exists()):
        p = Profile.objects.get(f_uid=fuser.id)
        Name =str(fuser.f_name+" "+fuser.l_name).upper()
        BOd = fuser.dOB
        bio = p.bio
        email = fuser.email
        gender=str(fuser.gender).upper()
    else:
        Name =str(fuser.f_name+" "+fuser.l_name).upper()
        BOd =fuser.dOB
        bio="USER HAS NOT ADDED ANY BIO OR PIC YET!!!!"#hi i am oishi
        email=fuser.email
        gender=str(fuser.gender).upper()
    return render(request, 'profile_show.html', {
                                             'name': Name,
                                             'bod': BOd,
                                             'bio':bio,
                                             'email':email,
                                             'gender':gender})
def getMessagesRobo(request, user_id):
    list = []
    if RoboChat_Thread.objects.filter(f_uid=user_id).exists():
        chat = RoboChat_Thread.objects.get(f_uid=user_id)
        thread_Id=chat.id
        msgs = RoboChat.objects.filter(threadId=thread_Id)
        list = []
        for messages in msgs:
            userchat = messages.user_chat
            reply=messages.robo_chat
            time = (messages.chatTime).strftime("%m/%d/%Y, %H:%M:%S")
            sendero = FriendsUser.objects.get(id=user_id)
            sender_name = sendero.f_name + " " + sendero.l_name
            history1 = str('YOU  :'+userchat+', TIME :'+time)
            list.append(history1)
            history2 = str('ROBO  :'+reply+'\n'+', TIME :'+time)
            list.append(history2)
    return list

def chat_with_bot_page(request,user_name):
    user = User.objects.get(username=user_name)
    username=user.first_name+' '+user.last_name
    fuser = FriendsUser.objects.get(f_uid=user.id)
    userid = fuser.id
    list = getMessagesRobo(request,user_id=userid)
    if (request.method == 'POST'):
        message = request.POST['message']
        if message!='':
            if RoboChat_Thread.objects.filter(f_uid=userid).exists():
                #get the messege from thread and save gessege
                thread = RoboChat_Thread.objects.get(f_uid=userid)
                new_msg = RoboChat(user_chat=message, robo_chat=get_response(message), threadId=thread)
                new_msg.save()
                list = getMessagesRobo(request, user_id=userid)

            else:
                #save msg and reply from robo for each msg
                r_friend = RoboChat_Thread(f_uid=fuser)
                r_friend.save()
                thread = RoboChat_Thread.objects.get(f_uid=userid)

                new_msg=RoboChat(user_chat=message,robo_chat=get_response(message),threadId=thread)
                new_msg.save()
                list = getMessagesRobo(request,user_id=userid)
        else:
            pass
    return render(request, 'botchat.html', { 'user_full_name': username.upper(),
                                             'user_name':user_name,
                                             'messages': list})
def password_reset(request,user_name):
    user = User.objects.get(username=user_name)
    username = user.first_name + ' ' + user.last_name
    if (request.method == 'POST'):
        passw=request.POST['password']
        if user.password==passw:
            npass = request.POST['new_password']
            cpass = request.POST['confirm_password']
            if npass != '' and cpass != '':
                if npass == cpass :
                    user.password = npass
                    user.save()
                    fuser=FriendsUser.objects.get(f_uid=user.id)
                    fuser.password = npass
                    fuser.save()
                    messages.success(request, 'Password updated.')
                    return redirect('profile', user_name=user_name)
                else:
                    messages.error(request, 'THE PASSWORDS DOES NOT MATCH !!!...')
            else:
                messages.error(request, 'Empty string not allowed as password!!!!')
        else:
            messages.error(request, 'WRONG USER PASSWORD ENTERED!!!!')


    return render(request, 'update_password.html', {'user_name': username})

def getMessages(request, friend_id):
    friends = FriendsWith.objects.get(id=friend_id)
    msgs = FriendsChat_Thread.objects.filter(threadId=friends.id)
    list=[]
    for messages in msgs:
        fchat=messages.fChat
        time=(messages.fChatTime).strftime("%m/%d/%Y, %H:%M:%S")
        sendero=FriendsUser.objects.get(id=messages.sender_Id.id)
        sender_name=sendero.f_name+" "+sendero.l_name
        #history=[sender_name,fchat,time]
        history = str(sender_name.upper()+":"+fchat+"       "+time)
        list.append(history)
    return list

#bottttttt
def message_probability(user_message, recognised_words, single_response=False, required_words=[]):
    message_certainty = 0
    has_required_words = True

    # Counts how many words are present in each predefined message
    for word in user_message:
        if word in recognised_words:
            message_certainty += 1

    # Calculates the percent of recognised words in a user message
    percentage = float(message_certainty) / float(len(recognised_words))

    # Checks that the required words are in the string
    for word in required_words:
        if word not in user_message:
            has_required_words = False
            break

    # Must either have the required words, or be a single response
    if has_required_words or single_response:
        return int(percentage * 100)
    else:
        return 0
def check_all_messages(message):
    highest_prob_list = {}

    # Simplifies response creation / adds it to the dict
    def response(bot_response, list_of_words, single_response=False, required_words=[]):
        nonlocal highest_prob_list
        highest_prob_list[bot_response] = message_probability(message, list_of_words, single_response, required_words)

    # Responses -------------------------------------------------------------------------------------------------------
    response('Hello!', ['hello', 'hi', 'hey', 'Yo'], single_response=True)
    response('See you!', ['bye', 'goodbye'], single_response=True)
    response('I\'m doing fine, and you?', ['how', 'are', 'you', 'doing'], required_words=['how', 'are', 'you'])
    response('Perfectly fine', ['how', 'is', 'your', 'day'], required_words=['how', 'day'])
    response('Robo', ['what', 'is', 'your', 'name'], required_words=['your', 'name'])
    response('My pleasure..', ['thank you', 'thanks'], single_response=True)
    response('You don\'t have to say that!!!Anyway,Thank you!', ['you', 'are', 'nice'], required_words=['you', 'nice'])
    response('Thanks!', ['you', 'are', 'sweet'], required_words=['you', 'sweet'])
    response('I am a bot my origin is processor!!!',['where','are','you','from'] , required_words=['where', 'you', 'from'])
    response('I am as old as the website', ['how', 'old', 'are', 'you'], required_words=['how', 'old'])
    response('My age is the same as the website', ['what', 'is', 'your', 'age'], required_words=['your', 'age'])
    response('I do not have any particular favourite color, but I love BLACK', ['your', 'color'], required_words=['color','black'])
    response('It is a good invention of you humans but for details use the search box please', ['Where','what', 'is', 'internet'], required_words=['internet'])
    '''xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'''
    response('Great!!!', ['i', 'am', 'fine'], required_words=['fine'])
    response('My pleasure..', ['thank you', 'thanks'], single_response=True)
    response('You don\'t have to say that!!!Anyway,Thank you!', ['you', 'are', 'nice'], required_words=['you', 'nice'])
    response('Thanks!', ['you', 'are', 'sweet'], required_words=['you', 'sweet'])
    response('I am a bot my origin is processor!!!', ['where', 'are', 'you', 'from'],
             required_words=['where', 'you', 'from'])
    response('I am as old as the website', ['how', 'old', 'are', 'you'], required_words=['how', 'old'])
    response('My age is the same as the website', ['what', 'is', 'your', 'age'], required_words=['your', 'age'])
    response('I do not have any particular favourite color, but I love BLACK',
             ['what', 'is', 'your', 'favourite', 'color'], required_words=['color', 'favourite'])
    response('It is a good invention of you humans but for details use the search box please',
             ['Where', 'what', 'is', 'internet'], required_words=['internet'])
    response('AAAAhhhh!!! I do not watch TV that much!!!', ['what', 'is', 'your', 'favourite', 'show'],
             required_words=['favourite', 'show'])
    response('You are a human of course and you are a member of friends website!!! Haha!!', ['do', 'you', 'know', 'me'],
             required_words=['you', 'know'])
    response(
        'Facebook is a social networking site that makes it easy for you to connect and share with family and friends online.For more information please got to the query box.',
        ['what', 'is', 'facebook'], required_words=['what', 'facebook'])
    response('Google is a search engine!!!For more information please go to the query box!!', ['what', 'is', 'google'],
             required_words=['what', 'google'])
    response('YouTube is a free video sharing website!! For more information, use query box', ['what', 'is', 'youtube'],
             required_words=['what', 'youtube'])

    def unknown():
        response = ["Could you please re-write that on query-box? ",
                    "Sorry!!I may help you from the query-box",
                    "I can help you through the query-box",
                    "please go to the query-box"][
            random.randrange(4)]
        return response

    # Longer responses
    R_EATING = "I don't like eating anything because I'm a bot obviously!"
    response(R_EATING, ['what', 'you', 'eat'], required_words=['you', 'eat'])
    response(R_EATING, ['what', 'is', 'your', 'food'], required_words=['food'])

    best_match = max(highest_prob_list, key=highest_prob_list.get)

    return unknown() if highest_prob_list[best_match] < 1 else best_match


# Used to get the response
def get_response(user_input):
    split_message = re.split(r'\s+|[,;?!.-]\s*', user_input.lower())
    response = check_all_messages(split_message)
    return response