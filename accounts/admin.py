from django.utils.html import format_html
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account, UserProfile
# Register your models here.

class AccountAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'username', 'last_login', 'date_joined', 'is_active')

    # enter into user information when clicking username
    list_display_links = ('email','first_name','last_name')
    readonly_fields = ('last_login','date_joined')

    ordering = ('-date_joined',) #descending order

    # using custom model so need to add below code
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


class UserProfileAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        return format_html('<img src="{}" width="30" style="border-radius:50%;">'.format(object.profile_picture.url))
    thumbnail.short_description = 'Profile Picture'
    list_display = ('thumbnail', 'user', 'city', 'state', 'country') 

admin.site.register(Account, AccountAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
