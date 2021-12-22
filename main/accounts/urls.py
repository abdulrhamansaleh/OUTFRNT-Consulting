from django.urls import path

from . import views

app_name = 'accounts'


urlpatterns = [
    path('',views.home,name='home'),
    path('profile/',views.profileView,name = 'profile'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('signin/', views.SignInView.as_view(), name='signin'),
    path('signout/', views.signout, name='signout'),
    path('coachPortal/', views.coachView, name='coach'),
]
