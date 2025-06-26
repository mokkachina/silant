from django.core.exceptions import PermissionDenied

class ServiceOrgAccessMixin:
    """Миксин для проверки доступа сервисных организаций"""

    def dispatch(self, request, *args, **kwargs):
        if request.user.role == 'service' and not request.user.service_org:
            raise PermissionDenied("Ваш аккаунт не привязан к сервисной организации")
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.role == 'service':
            # Проверяем, есть ли в модели поле serviceorg (для Maintenance)
            if hasattr(self.model, 'serviceorg'):
                return qs.filter(serviceorg=self.request.user.service_org)
            # Иначе проверяем поле servicecompany (для Car)
            elif hasattr(self.model, 'servicecompany'):
                return qs.filter(servicecompany=self.request.user.service_org)
            # Для моделей, где нет прямого поля, но есть связь через car
            elif hasattr(self.model, 'car'):
                return qs.filter(car__servicecompany=self.request.user.service_org)
        return qs

class ManagerRequiredMixin:
    """Проверяет, что пользователь - менеджер"""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_manager:
            raise PermissionDenied("Требуются права менеджера")
        return super().dispatch(request, *args, **kwargs)


class ClientAccessMixin:
    """Ограничивает доступ только клиентам и их данным"""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_client:
            raise PermissionDenied("Доступ только для клиентов")
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)  # Только свои машины