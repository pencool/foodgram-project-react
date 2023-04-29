from django.contrib import admin

from users.models import User


class UsersModelAdmin(admin.ModelAdmin):
    list_display = ['username', 'id']
    list_filter = ['email', 'username']


admin.site.register(User, UsersModelAdmin)
