from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'is_active')
    list_filter = ('role', 'is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Персональные данные', {
            'fields': ('first_name', 'last_name')
        }),
        ('Права доступа', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Дополнительная информация', {
            'fields': ('role', 'service_org')  # Исправлено на service_org
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'role', 'service_org'),
        }),
    )

admin.site.register(User, CustomUserAdmin)

# class UserAdmin(UserAdmin):
#     def get_readonly_fields(self, request, obj=None):
#         readonly_fields = super().get_readonly_fields(request, obj)
#         if obj and not request.user.has_perm('accounts.can_change_credentials'):
#             return list(readonly_fields) + ['username', 'password']
#         return readonly_fields
# admin.site.register(User, UserAdmin)

