from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse
from django.core.mail import send_mail
import jwt
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.sites.shortcuts import get_current_site
from smtplib import SMTPException
from django.utils.safestring import mark_safe
import json
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from .models import Loggeduser,Chatroom
# Create your views here.

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        payload = {
            'username': username,
        }

        # Used to store the data in SMD(success,message,data) format
        smddata = {
            'success': False,
            'message': '',
            'data': []
        }

        try:
            user = auth.authenticate(username=username, password=password)
        except ValueError as e:
            print(e)
        if user is not None:
        

            auth.login(request, user)
            username=request.user
            print(username)
            

            jwt_token = {"token": jwt.encode(payload, "secret", algorithm="HS256").decode('utf-8')}

            try:
                Token = jwt_token['token']
            except KeyError as e:
                print(e)

            try:
                smddata['success'] = True
                smddata['message'] = "Login Successful"
                smddata['data'] = [Token]
            except KeyError as e:
                print(e)
            Loggeduser.objects.create(username=username)
            return redirect('/login/index')
        else:
            messages.info(request, 'invalid credentials')
            # render(request, 'accounts/login.html')
    return render(request, 'accounts/login.html')


def logout(request):
    username=request.user
    Loggeduser.objects.filter(username=username).delete()
    auth.logout(request)

    return redirect('http://127.0.0.1:8000/login')


def register(request):
    if request.method == 'POST':
        
        username = request.POST['user_name']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']

        if password1 == password2:
            #checking whether the user exists or not
            if User.objects.filter(username=username).exists():
                messages.info(request, 'User name is already taken')
                #return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email is already registered')
                #return redirect('register')
            else:
                
                try:
                    #Inserting a new row into the database
                    user = User.objects.create_user(username=username, password=password1, email=email)
                except ObjectDoesNotExist as e:
                    print(e)

                # user.save()
                # user.is_active = False
                # user.save()

                #storing username and email as payload in dictionary format
                payload = {
                    'username': user.username,
                    'email': user.email
                }
                #creating the token
                key = jwt.encode(payload, "secret", algorithm="HS256").decode('utf-8')

                currentsite = get_current_site(request)
                mail_subject='Link to activate the account'
                mail_message = render_to_string('accounts/activate.html', {
                    'user': user.username,
                    'domain': get_current_site(request).domain,
                    'token': key,
                })
                
                recipient_email=['noothan627@gmail.com']
                email=EmailMessage(mail_subject, mail_message, to=[recipient_email])
                try:
                    email.send()
                    
                except SMTPException as e:
                    print(e)


                return HttpResponse("Please Check your mail for activating")
            
        else:
            messages.info(request, 'Passwords doesnt match')
            return render(request, 'accounts/register.html')
        # return redirect('/')
    # else:
    return render(request, 'accounts/register.html')


def activate(request, token):
    #decoding the token and getting the datas
    user_details = jwt.decode(token, 'secret', algorithms='HS256')
    #getting the user name
    user_name = user_details['username']
    
    try:
        #getting the user object
        user1 = User.objects.get(username=user_name)
        
    except ObjectDoesNotExist as e:
        print(e)

    if user1 is not None:
        #Making is_active flag true
        user1.is_active = True
        #saving the user
        user1.save()
        return redirect('login_user')
    else:
        return redirect('register')


def verify(request, Token):
    #decoding the token and storing it into user_details
    user_details = jwt.decode(Token, "secret")
    #getting the username from token
    user_name = user_details['username']

    try:
        #getting the user object
        u = User.objects.get(username=user_name)
    except ObjectDoesNotExist as e:
        print(e)
    if u is not None:
        currentsite = get_current_site(request)
        string = str(currentsite) + 'accounts/resetpassword/' + user_name + '/'
        #calling the reset_password method
        reset_password(request, string)
        #return redirect("resetmail.html")
    else:
        messages.info("Invalid user")
        return redirect('register')
    return render(request, "accounts/resetpassword.html")


def reset_password(request, username):
    #checking whether the request is post or not
    if request.method == 'POST':
        #Taking the new password two times
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        #checking whether both the passwords match or not
        if(password1 == password2):
            #getting the current user name
            username=request.user
            #checking whether the user wxists in the database or not
            if User.objects.filter(username=username).exists():
                #getting that user object
                user1 = User.objects.get(username=username)
                #setting the password to new password
                user1.set_password(password1)
                #saving the user
                user1.save()
                return redirect('login_page')
        else:
            #If two passwords are not same, display passords doesn't match
            print("Passwords doesn't match")
    return render(request, 'accounts/resetpassword.html')


def sendmail(request):
    #checking whether the request is post or not
    if request.method == 'POST':
        #getting the current user's email id
        emailid = request.POST['email']

        try:
            #checking whether the user exists in the database or not
            if User.objects.filter(email=emailid).exists():
                #getting that user object
                u = User.objects.get(email=emailid)
                #storing the username and email as payload
                payload = {
                    'username': u.username,
                    'email': u.email
                }
                #generating the jwt token
                jwt_token = {"token": jwt.encode(payload, "secret", algorithm="HS256").decode('utf-8')}

                try:
                    Token = jwt_token["token"]
                except KeyError as e:
                    print(e)

                currentsite = get_current_site(request)
                subject = "Link to Reset the password"
                message = str(currentsite) + '/verify/' + Token

                try:
                    send_mail(subject, message, 'noothanprem@gmail.com', ['noothan627@gmail.com'])
                except SMTPException as e:
                    print(e)

                return redirect('http://127.0.0.1:8000/resetmail')
                #return render(request, "accounts/resetmail.html")

            else:
                messages.info(request, 'Invalid Email id.. Try Once again')
                # return redirect('register')
                return render(request, "accounts/register.html")
        except TypeError as e:
            print(e)
    else:
        return render(request, "accounts/resetmail.html")

@login_required(login_url='/login')
def index(request):
    
    return render(request, 'chat/index.html', {})


@login_required(login_url='/room')
def room(request, room_name):
    
    #gets the queryset which contains all the Loggeduser objects in the database
    loggedusers=Loggeduser.objects.all()
    messages=Chatroom.objects.filter(room=room_name).values('message')
    message=list(messages)
    print(message)
    

    #passing the loggedusers,messages while rendering
    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name)), 'loggedusers':loggedusers, 'messages': mark_safe(json.dumps(message))
    })

def home(request):
    return render(request,"accounts/home.html")