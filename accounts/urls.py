from django.urls import path
from . import views

app_name = 'chat'
urlpatterns = [
    # path('register', views.register, name='register_user'),
    path('login', views.login, name='login_user'),
    path('logout', views.logout, name='logout'),
    # path('activate/<token>/', views.activate, name='activate'),
    path('resetpassword', views.reset_password, name='resetpassword'),
    path('verify/<Token>/', views.verify, name='verify'),
    path('resetmail', views.sendmail, name='resetmail'),
    path('resetpassword/<username>/', views.reset_password, name='resetpassword'),
    path('login/index', views.index, name='index_page'),
    path('login/index/<str:room_name>/', views.room, name='room_page'),
    path('', views.home, name='home')
]
