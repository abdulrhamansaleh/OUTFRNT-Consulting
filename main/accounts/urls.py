from django.urls import path

from . import views

app_name = 'accounts'


urlpatterns = [
    # main home path 
    path('', views.home, name = 'home'),
    
    # user view paths 
    path('signup/', views.SignUpView.as_view(), name = 'signup'),
    path('signin/', views.SignInView.as_view(), name = 'signin'),
    path('signout/', views.signout, name = 'signout'),
    
    # coach view paths 
    path('coachPortal/', views.view_client_tasks, name ='clients-view'),
    path('client-permissions/',views.manage_clients_status, name = 'manage'),
    path('client-update-outfrnt/<str:user>',views.update_status_to_client, name = 'change-to-client'),
    path('newclient-update-outfrnt/<str:client>',views.update_status_to_newclient, name = 'change-to-new-client'),
    path('revoke-questionnaire/<str:client>', views.update_status_to_prospect , name = "change-to-propsect"),
    path('remove-user/<str:client>', views.remove_user , name = 'remove-user'),
]
