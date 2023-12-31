from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, OtpCode
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserCreationForm,UserChangeForm


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email','phone_number','is_admin')
    list_filter = ('is_admin',)

    fieldsets = (
        ('Custom User Update',{'fields':('email','phone_number','full_name','password')}),
        ('Persmissions',{'fields':('is_active','is_admin','last_login')}),
    )

    add_fieldsets = (
        ('User Create',{'fields':('email','phone_number','full_name','password1','password2')}),
    )

    search_fields = ('email','full_name')
    ordering = ('full_name'),
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)

@admin.register(OtpCode)
class OtpCodeAdmin(admin.ModelAdmin):
    list_display = ('phone_number','code','created')