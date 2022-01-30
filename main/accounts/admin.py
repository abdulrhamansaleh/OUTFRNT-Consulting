from django.contrib import admin
from accounts.models import User
from django.contrib.auth.admin import UserAdmin,Group

class AccountAdmin(UserAdmin):
    list_display = ('email','username','date_joined','last_login','is_admin','is_staff','is_coach','is_client','is_newclient','is_prospect','categories_answered')
    search_fields = ('email','username')
    readonly_fields = ('date_joined','last_login')
    
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(User,AccountAdmin)
admin.site.unregister(Group)