from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from auser.forms import UserChangeForm, UserCreationForm
from auser.models import UserRole, User, RecommendUserEmail, InviteUserEmail, Worker


@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ['type']


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'phone_number', 'is_admin', 'is_company_admin', 'is_online', 'user_type')
    list_filter = ('is_admin', 'is_company_admin', 'is_first_login')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': (
            'phone_number', 'first_name', 'last_name', 'role'
        )}),
        ('Permissions', {'fields': ('is_admin', 'is_company_admin', 'is_first_login', 'is_online')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone_number', 'password1', 'password2'),
        }),
    )
    readonly_fields = ['is_online']
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.unregister(Group)


@admin.register(RecommendUserEmail)
class RecommendUserEmailAdmin(admin.ModelAdmin):
    list_display = ['email', 'is_active']
    readonly_fields = ['token', 'is_invite_by_our_admin']


@admin.register(InviteUserEmail)
class InviteUserEmailAdmin(admin.ModelAdmin):
    list_display = ['email', 'is_active']
    readonly_fields = ['token', 'is_invite_by_our_admin']


@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_display = ['whose_employee', 'employee']
