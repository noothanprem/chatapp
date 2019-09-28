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
from .models import Loggeduser

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
            if User.objects.filter(username=username).exists():
                messages.info(request, 'User name is already taken')
                #return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email is already registered')
                #return redirect('register')
            else:
                
                try:
                    user = User.objects.create_user(username=username, password=password1, email=email)
                except ObjectDoesNotExist as e:
                    print(e)

                # user.save()
                # user.is_active = False
                # user.save()

                payload = {
                    'username': user.username,
                    'email': user.email
                }

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
    user_details = jwt.decode(token, 'secret', algorithms='HS256')
    user_name = user_details['username']
    print(user_details,'--------->')
    try:
        user1 = User.objects.get(username=user_name)
        print('user1','--------->user1')
    except ObjectDoesNotExist as e:
        print(e)

    if user1 is not None:
        user1.is_active = True
        user1.save()
        localStorage.setItem('favoriteflavor','vanilla')
        return redirect('login_user')
    else:
        return redirect('register')


def verify(request, Token):
    user_details = jwt.decode(Token, "secret")
    user_name = user_details['username']

    try:
        u = User.objects.get(username=user_name)
    except ObjectDoesNotExist as e:
        print(e)
    if u is not None:
        currentsite = get_current_site(request)
        string = str(currentsite) + 'accounts/resetpassword/' + user_name + '/'
        reset_password(request, string)
        return redirect("resetmail.html")
    else:
        messages.info("Invalid user")
        return redirect('register')
    return render(request, "accounts/resetpassword.html")


def reset_password(request, username):
    if request.method == 'POST':
        password1 = request.POST['password1']
        password2 = request.POST['password2']
    if User.objects.filter(username=username).exists():
        user1 = User.objects.get(username=username)
        user1.set_password(password1)
        
    return render(request, 'accounts/resetpassword.html')


def sendmail(request):
    if request.method == 'POST':
        emailid = request.POST['email']

        try:
            if User.objects.filter(email=emailid).exists():
                u = User.objects.get(email=emailid)

                payload = {
                    'username': u.username,
                    'email': u.email
                }
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
                messages.info(request, "Please Check your mail for Resetting the password")
                return render(request, "accounts/resetmail.html")

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
    loggedusers=Loggeduser.objects.all()
    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name)), 'loggedusers':loggedusers
    })

def home(request):
    return render(request,"accounts/home.html")