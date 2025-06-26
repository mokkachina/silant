from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings

class NoNewUsersAccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request):
        # Разрешаем регистрацию только для суперпользователей (администраторов)
        if request.user.is_superuser:
            return True
        return False