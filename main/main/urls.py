from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as authViews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('accounts.urls')),

    #password urls 
    path('password_change/done/'
    ,authViews.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html')
    ,name='password_change_done'),

    path('password_change/',
    authViews.PasswordChangeView.as_view(template_name='registration/password_change.html')
    ,name='password_change'
    ),

    path('password_reset_done/done/'
    ,authViews.PasswordResetCompleteView.as_view(template_name='registration/password_reset_done.html')
    ,name='password_reset_done'),

    path('reset/<uidb64>/<token>/'
    ,authViews.PasswordResetConfirmView.as_view()
    ,name='password_reset_confirm'),

    path('password_reset/'
    ,authViews.PasswordResetView.as_view()
    ,name = 'password_reset'),

    path('reset/done/'
    ,authViews.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html')
    ,name ='password_reset_complete'),

]
