from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db import models
from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, CreateView, DeleteView

from accounts.forms import MaintenanceForm, ComplaintsForm, ServComplaintsCreateForm, ServMaintenanceCreateForm
from accounts.mixins import ServiceOrgAccessMixin
from car.models import Car
from maintenance.models import Maintenance, Complaints

class ServCarListView(ServiceOrgAccessMixin, ListView):
    model = Car
    template_name = 'serv_car.html'
    context_object_name = 'scars'
    paginate_by = 5
    ordering = ['-datashipfactory']

    def get_queryset(self):
        qs = super().get_queryset().select_related(
            'carmodel',
            'enginemodel',
            'servicecompany'
        )

        # Для клиентов фильтруем по user, для остальных ролей не добавляем этот фильтр
        if self.request.user.role == 'client':
            qs = qs.filter(user=self.request.user)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_tab'] = 'cars'
        return context

class ServMaintenanceListView(ServiceOrgAccessMixin, ListView):
    model = Maintenance
    template_name = 'serv_maint.html'
    context_object_name = 'smain'
    paginate_by = 5
    ordering = ['-datamainten']

    def get_queryset(self):
        return super().get_queryset().select_related('car', 'serviceorg')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_tab'] = 'maintenance'  # Ключевое здесь!
        return context

class ServCompListView(ServiceOrgAccessMixin,ListView):
    model = Complaints
    template_name = 'serv_compl.html'
    context_object_name = 'scom'
    paginate_by = 5
    ordering = ['-databroke']

    def get_queryset(self):
        return super().get_queryset().select_related('car', 'serviceorg')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_tab'] = 'complaints'  # Ключевое здесь!
        return context
class ServMainUpdateView(ServiceOrgAccessMixin,UpdateView):
    model = Maintenance
    form_class = MaintenanceForm
    template_name = 'edit_form_serv_main.html'
    success_url = '/service/maintenance/'

    def dispatch(self, request, *args, **kwargs):

        if request.user.is_service:
            return super().dispatch(request, *args, **kwargs)

class ServComplUpdateView(ServiceOrgAccessMixin,UpdateView):
    model = Complaints
    form_class = ComplaintsForm
    template_name = 'edit_form_serv_compl.html'
    success_url = '/service/complaints/'

    def dispatch(self, request, *args, **kwargs):

        if request.user.is_service:
            return super().dispatch(request, *args, **kwargs)

class ServMainCreateView(CreateView):
    model = Maintenance
    form_class = ServMaintenanceCreateForm
    template_name = 'serv_create_main.html'
    success_url = reverse_lazy('serv_mainten')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_service:
            raise PermissionDenied("Доступ разрешён только сервисным организациям")
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if self.request.user.is_service and 'car' in form.fields:
            form.fields['car'].queryset = Car.objects.filter(
                servicecompany=self.request.user.service_org
            )
        return form
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_tab'] = 'mainten_add'
        return context


class ServComplCreateView(CreateView):
    model = Complaints
    form_class = ServComplaintsCreateForm
    template_name = 'serv_create_compl.html'
    success_url = reverse_lazy('serv_compl')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_service:
            raise PermissionDenied("Доступ разрешён только сервисным организациям")
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if self.request.user.is_service and 'car' in form.fields:
            form.fields['car'].queryset = Car.objects.filter(
                servicecompany=self.request.user.service_org
            )
        return form
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_tab'] = 'compl_add'
        return context


class MaintenanceDeleteView(LoginRequiredMixin, DeleteView):
    model = Maintenance
    success_url = reverse_lazy('serv_mainten')  # URL для перенаправления после удаления

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        # Проверка прав (аналогично UpdateView)
        if not (request.user.is_staff or
                (request.user.is_service and obj.serviceorg == request.user.service_org) or
                (request.user.is_client and obj.car.user == request.user)):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

class ComplDeleteView(LoginRequiredMixin, DeleteView):
    model = Complaints
    success_url = reverse_lazy('serv_compl')  # URL для перенаправления после удаления

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        # Проверка прав (аналогично UpdateView)
        if not (request.user.is_staff or
                (request.user.is_service and obj.serviceorg == request.user.service_org) or
                (request.user.is_client and obj.car.user == request.user)):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)