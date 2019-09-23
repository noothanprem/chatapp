from django.urls import path
from . import views

urlpatterns=[
    path('register',views.register,name='register'),
    path('login',views.login,name='login'),
    path('logout',views.logout,name='logout'),
    path('activate/<Token>/',views.activate,name='activate'),
    path('resetpassword',views.reset_password,name='resetpassword')
]