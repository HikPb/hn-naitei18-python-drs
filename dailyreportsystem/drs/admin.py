from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User, Form, Division, Position, Notification, Skill, Timeline, Report, Profile, Plan


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('email', 'is_staff', 'is_active', 'is_manager', 'manager', 'name', 'dob', 'division')
    list_filter = ('email', 'is_staff', 'is_manager', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'manager', 'name', 'dob', 'division', 'sex', 'phone', 'position', 'skill')}),
        ('Permissions', {'fields': ('is_staff', 'is_manager', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_manager', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

admin.site.register(User, CustomUserAdmin)
admin.site.register(Skill)
admin.site.register(Position)
admin.site.register(Division)
admin.site.register(Plan)
admin.site.register(Timeline)
admin.site.register(Notification)
admin.site.register(Report)
admin.site.register(Profile)

class FormView(admin.ModelAdmin):
    """Defines format of inline book insertion (used in AuthorAdmin)"""
    model = Form
    list_display = ('id', 'title', 'created_at', 'content','sender')
    list_filter = ('id', 'title', 'created_at', 'content',)

admin.site.register(Form, FormView)
