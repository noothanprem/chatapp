from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.http import HttpResponse
from django.core.mail import send_mail
import jwt
from django.contrib.sites.shortcuts import get_current_site
# Create your views here.

def login(request):
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']
        payload={
                    'username': username,
                }
        smddata={
            'success':False,
            'message':'',
            'data':[]
        }
        try:
            user=auth.authenticate(username=username,password=password)
        except ValueError as e:
            print(e)
        if user is not None:
            auth.login(request,user)
              
            jwt_token= {"token": jwt.encode(payload, "secret", algorithm="HS256").decode('utf-8')}
            Token=jwt_token['token']
            smddata['success']=True
            smddata['message']="Login Successful"
            smddata['data']=[Token]
            return render(request,'home.html',{'name':user.username,'message':smddata})
        else:
            messages.info(request,'invalid credentials')
            return redirect('login')
    return render(request,'login.html')

def logout(request):
    auth.logout(request)
    return redirect('/')

def register(request):
    if request.method == 'POST':
        username=request.POST['user_name']
        password1=request.POST['password1']
        password2=request.POST['password2']
        email=request.POST['email']
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,'User name is already taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'Email is already registered')
                return redirect('register')
            else:
                user=User.objects.create_user(username=username,password=password1,email=email)
                user.save()
                user.is_active=False
                user.save()
                payload={
                    'username': user.username,
                    'email': user.email
                }    

                jwt_token= {"token": jwt.encode(payload, "secret", algorithm="HS256").decode('utf-8')}
                Token=jwt_token['token']
                currentsite=get_current_site(request)
                send_mail('Link to activate the account',str(currentsite)+'/accounts/activate/'+Token, 'noothanprem@gmail.com',['noothan627@gmail.com'], fail_silently=False)
                messages.info(request,"Please Check your mail for activating")
                #print("User created")
                #return redirect('login')
        else:
            messages.info(request,'Passwords doesnt match')
            return redirect('register')
        #return redirect('/')
    #else:
    return render(request,'register.html')
    

def activate(request,Token):
    user_details=jwt.decode(Token,'secret',algorithms='HS256')
    user_name=user_details['username']
    u = User.objects.get(username=user_name)
    if u is not None:
        u.is_active=True
        u.save()
        return redirect('login')
    else:
        return redirect('register')

def reset_password(request):
    if request.method == 'POST':
        password1=request.POST['password1']
        password2=request.POST['password2']
        if password1 == password2:
            User.set_password(password1)
            
        else:
            messages.info(request,"Password doesn't match")
            return redirect('resetpassword')
    return render(request,'resetpassword.html')

def sendmail(request):
    if request.method == 'POST':
        emailid=request.POST['email']
        if User.objects.filter(email=emailid).exists():
            
        else:
            messages.info(request,'Invalid Email id.. Try Once again')
            return redirect('register')

