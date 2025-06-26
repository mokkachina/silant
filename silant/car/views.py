from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.shortcuts import redirect

from accounts.forms import MaintenanceForm, MaintenanceCreateForm
from accounts.mixins import ClientAccessMixin
from car.models import Car
from car.utils import TitleMixin
from maintenance.models import Maintenance, Complaints


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")


class CarSearchView(ListView):
    model = Car
    template_name = 'car/index.html'
    context_object_name = 'homepage'


    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # Перенаправляем в зависимости от роли пользователя
            if request.user.is_manager:
                return redirect('admin_car')  # Для менеджеров
            elif request.user.is_service:
                return redirect('serv_car')  # Для сервисных организаций
            elif request.user.is_client:
                return redirect('client_car')  # Для клиентов
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        search_query = self.request.GET.get('carnumber', '').strip()

        # Для неавторизованных - только поиск по номеру
        if search_query:
            return Car.objects.filter(
                Q(carnumber__iexact=search_query) |
                Q(carnumber__icontains=search_query)
            )
        return Car.objects.none()  # Пустой queryset, если поиск не выполнен

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем параметры для корректной работы пагинации
        context['search_performed'] = bool(self.request.GET.get('carnumber'))
        context['order'] = self.request.GET.get('order', '')
        return context

class ClientCarListView(ClientAccessMixin, ListView):
    """Список машин только текущего клиента"""
    model = Car
    template_name = 'car/clientview.html'
    context_object_name = 'cars'
    ordering = ['-datashipfactory']

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user).select_related(
            'carmodel',
            'enginemodel',
            'servicecompany'
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_tab'] = 'cars'  # Ключевое здесь!
        return context


class ClientMaintenanceListView(ClientAccessMixin, ListView):
    """ТО только для машин клиента"""
    model = Maintenance
    template_name = 'car/maintenview.html'
    context_object_name = 'cars'
    ordering = ['-datamainten']

    def get_queryset(self):
        return Maintenance.objects.filter(car__user=self.request.user).select_related('car', 'car__carmodel')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_tab'] = 'maintenance'  # Ключевое здесь!
        return context


class ClientCompListView(ClientAccessMixin, ListView):
    """ТО только для машин клиента"""
    model = Complaints
    template_name = 'car/complview.html'
    context_object_name = 'cars'
    ordering = ['-databroke']

    def get_queryset(self):
        return Complaints.objects.filter(car__user=self.request.user).select_related('car', 'car__carmodel')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_tab'] = 'complaints'  # Ключевое здесь!
        return context

class MaintenanceUpdateView(UpdateView):  # Переименовано из CarUpdateView
    model = Maintenance
    form_class = MaintenanceForm
    template_name = 'car/edit_form.html'
    success_url = '/client/maintenance/'

    def dispatch(self, request, *args, **kwargs):

        if request.user.is_client:
            return super().dispatch(request, *args, **kwargs)


class ClientCarCreateView(CreateView):
    model = Maintenance
    form_class = MaintenanceCreateForm  # Используем нашу форму
    template_name = 'car/admin_mainten_create.html'
    success_url = reverse_lazy('client_mainten')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_client:
            raise PermissionDenied("Доступ разрешён только клиентам")
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Передаём пользователя в форму
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_tab'] = 'mainten_add'
        return context

class ClientMaintenDeleteView(LoginRequiredMixin, DeleteView):
    model = Maintenance
    success_url = reverse_lazy('client_mainten')  # URL для перенаправления после удаления

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        # Проверка прав (аналогично UpdateView)
        if not (request.user.is_staff or
                (request.user.is_service and obj.serviceorg == request.user.service_org) or
                (request.user.is_client and obj.car.user == request.user)):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)