from django.contrib import admin
from app.models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["get_username", "account_number", "balance"]

    def get_username(self, obj):
        return obj.user.username

    get_username.short_description = "Username"