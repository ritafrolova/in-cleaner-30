from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm, ProfileSettingsForm, OrderForm
from .models import CustomUser, Profile, Specialty, Order


class OrderAdmin(admin.ModelAdmin):
    form = OrderForm


class ProfileAdmin(admin.ModelAdmin):
    form = ProfileSettingsForm


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'username', ]


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Specialty)
admin.site.register(Order, OrderAdmin)
