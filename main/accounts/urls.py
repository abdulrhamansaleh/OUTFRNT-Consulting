from django.urls import path
from . import views 

urlpatterns = [
    # main outfrntlanding page 
    path('',views.home,name='home'),
    # paths for client views 
    path('register/', views.registerClient,name='register'),
    path('profile/',views.profileView,name = 'profile'),
    # universal view for account models 
    path('logout/',views.logoutUser,name='logout'),
    path('login/',views.loginUser,name='login'),
]
