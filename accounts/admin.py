from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    
    # Display the fields in the admin list view
    list_display = ["username", "email", "is_dean", "is_teacher", "is_student", "is_admin", "is_staff"]
    
    # Add filter options for boolean fields in the admin interface
    list_filter = ("is_dean", "is_teacher", "is_student", "is_admin", "is_staff")
    
    # Customize the fields shown in the admin detail/edit page
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "email")}),
        ("Permissions", {"fields": ("is_dean", "is_teacher", "is_student", "is_admin", "is_staff", "is_superuser")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    
    # Fields to be shown when creating a new user
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "password1", "password2", "is_dean", "is_teacher", "is_student", "is_admin", "is_staff"),
        }),
    )
    
    search_fields = ("username", "email")
    ordering = ("username",)

admin.site.register(CustomUser, CustomUserAdmin)


# Register your models here.
