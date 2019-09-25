from django.urls import path
from . import views

app_name='chat'
urlpatterns=[
    path('register',views.register,name='register'),
    path('login',views.login,name='login'),
    path('logout',views.logout,name='logout'),
    path('activate/<Token>/',views.activate,name='activate'),
    path('resetpassword',views.reset_password,name='resetpassword'),
    path('verify/<Token>/',views.verify,name='verify'),
    path('resetmail',views.sendmail,name='resetmail'),
    path('resetpassword/<username>/',views.reset_password,name='resetpassword'),
    #path('index', views.index, name='index')
    path('', views.index, name='index'),
    path('<str:room_name>/', views.room, name='room'),
]