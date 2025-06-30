from allauth.account.views import logout
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect, Http404

from django.contrib.auth.views import LoginView
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django_filters.views import FilterView
from django.shortcuts import render, redirect, get_object_or_404
from car.filters import CarFilter, MaintenanceFilter, ComplaintsFilter
from car.models import Car, Carmodel, Enginemodel, Transmodel, Axdrivemodel, Axcontrolmodel, Serviceorg
from maintenance.models import Maintenance, Complaints, Maintenview, Failnode, Recoverymethod
from .forms import RoleAuthForm, CarForm, MaintenanceForm, ComplaintsForm, MaintenanceCreateForm, \
    AdminComplaintsCreateForm, AdminCarAddForm
from .mixins import ManagerRequiredMixin


def logout_user(request):
    """Кастомный выход с очисткой сессии"""
    if 'car_id' in request.session:
        del request.session['car_id']
    logout(request)
    return HttpResponseRedirect(reverse_lazy('login'))


class RoleLoginView(LoginView):
    form_class = RoleAuthForm
    template_name = 'accounts/login.html'

    def get_success_url(self):
        user = self.request.user
        if user.is_manager:
            return reverse('admin_car')
        elif user.is_service:
            return reverse('serv_car')
        elif user.is_client:
            return reverse('client_car')
        return super().get_success_url()

class AdminCarListView(ManagerRequiredMixin, FilterView):
    """администратор Машины"""
    model = Car
    filterset_class = CarFilter
    fields = '__all__'
    template_name = 'admin_view.html'
    context_object_name = 'adcars'
    paginate_by = 2
    ordering = ['-datashipfactory']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_tab'] = 'cars'  # Ключевое здесь!
        return context
    # def get_queryset(self):
    #     return super().get_queryset().filter(user=self.request.user).select_related(
    #         'carmodel',
    #         'enginemodel',
    #         'servicecompany'
    #     )


class AdminMaintenanceListView(ManagerRequiredMixin, FilterView):
    """администратор ТО"""
    model = Maintenance
    filterset_class = MaintenanceFilter
    fields = '__all__'
    template_name = 'admin_maint.html'
    success_url = 'admin/maintenance'
    context_object_name = 'admain'
    ordering = ['-datamainten']
    paginate_by = 2 # Сохраняем пагинацию из вашего шаблона

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_tab'] = 'maintenance'  # Ключевое здесь!
        return context

    # def get_queryset(self):
    #     return Maintenance.objects.filter(car__user=self.request.user).select_related('car', 'car__carmodel')

class AdminCompListView(ManagerRequiredMixin, FilterView):
    """администратор Рекламации"""
    model = Complaints
    filterset_class = ComplaintsFilter
    fields = '__all__'
    template_name = 'admin_com.html'
    context_object_name = 'adcom'
    paginate_by = 2
    ordering = ['-databroke']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_tab'] = 'complaints'  # Ключевое здесь!
        return context

class AdminCarUpdateView(UpdateView):
    model = Car
    form_class = CarForm
    template_name = 'car_edit_form.html'
    success_url = reverse_lazy('admin_car')

    def dispatch(self, request, *args, **kwargs):
        # Менеджеры могут редактировать любые записи
        if request.user.is_manager:
            return super().dispatch(request, *args, **kwargs)
    # def dispatch(self, request, *args, **kwargs):
    #     obj = self.get_object()
    #     # Проверяем владельца машины напрямую (у Car есть поле user)
    #     if obj.user != request.user and not request.user.is_superuser:
    #         raise PermissionDenied("У вас нет прав для редактирования этой машины")
    #     return super().dispatch(request, *args, **kwargs)

class AdminMainUpdateView(UpdateView):
    model = Maintenance
    form_class = MaintenanceForm
    template_name = 'admin_maint_edit_form.html'
    success_url = reverse_lazy('admin_mainten')

    def dispatch(self, request, *args, **kwargs):
        # Менеджеры могут редактировать любые записи
        if request.user.is_manager:
            return super().dispatch(request, *args, **kwargs)

class AdminComplUpdateView(UpdateView):
    model = Complaints
    form_class = ComplaintsForm
    template_name = 'compl_edit_form.html'
    success_url = reverse_lazy('admin_compl')

    def dispatch(self, request, *args, **kwargs):
        # Менеджеры могут редактировать любые записи
        if request.user.is_manager:
            return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем дополнительные данные в контекст
        context['car'] = self.object.car  # Передаем связанную машину
        return context

class AdminCarCreateView(CreateView):
    model = Car
    form_class = AdminCarAddForm
    template_name = 'car_create.html'
    success_url = reverse_lazy('admin_car')  # URL для перенаправления после успешного создания

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_manager:
            raise PermissionDenied("Доступ разрешён только менеджерам")
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Корректная передача пользователя
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_tab'] = 'car_add'
        return context

class AdminComplCreateView(CreateView):
    model = Complaints
    form_class = AdminComplaintsCreateForm
    template_name = 'admin_create_compl.html'
    success_url = reverse_lazy('admin_compl')  # URL для перенаправления после успешного создания

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_manager:
            raise PermissionDenied("Доступ разрешён только менеджерам")
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Корректная передача пользователя
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_tab'] = 'mainten_add'
        return context
class AdminMaintCreateView(CreateView):
    model = Maintenance
    form_class = MaintenanceCreateForm
    template_name = 'main_create.html'
    success_url = reverse_lazy('admin_mainten')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_manager:
            raise PermissionDenied("Доступ разрешён только менеджерам")
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Корректная передача пользователя
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_tab'] = 'mainten_add'
        return context

class AdminCarDeleteView(LoginRequiredMixin, DeleteView):
    model = Car
    success_url = reverse_lazy('admin_car')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        # Проверка прав (аналогично UpdateView)
        if not (request.user.is_staff or
                (request.user.is_service and obj.serviceorg == request.user.service_org) or
                (request.user.is_client and obj.car.user == request.user)):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

class AdminMaintDeleteView(LoginRequiredMixin, DeleteView):
    model = Maintenance
    success_url = reverse_lazy('admin_mainten')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        # Проверка прав (аналогично UpdateView)
        if not (request.user.is_staff or
                (request.user.is_service and obj.serviceorg == request.user.service_org) or
                (request.user.is_client and obj.car.user == request.user)):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

class AdminComplDeleteView(LoginRequiredMixin, DeleteView):
    model = Complaints
    success_url = reverse_lazy('admin_compl')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        # Проверка прав (аналогично UpdateView)
        if not (request.user.is_staff or
                (request.user.is_service and obj.serviceorg == request.user.service_org) or
                (request.user.is_client and obj.car.user == request.user)):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

 # Справочник
REFERENCE_MODELS = {
    'Виды ТО': Maintenview,
    'Узлы отказа': Failnode,
    'Способы восстановления': Recoverymethod,
    'Модели техники': Carmodel,
    'Модели двигателя': Enginemodel,
    'Модели трансмиссии': Transmodel,
    'Модели ведущего моста': Axdrivemodel,
    'Модели управляемого моста': Axcontrolmodel,
    'Сервисные компании': Serviceorg,
}
def get_model_class(model_name):
    """Получает класс модели по ее названию"""
    return REFERENCE_MODELS.get(model_name)

def admin_reference(request):
    # Получаем все справочники
    reference_models = {
        'Виды ТО': Maintenview.objects.all(),
        'Узлы отказа': Failnode.objects.all(),
        'Способы восстановления': Recoverymethod.objects.all(),
        'Модели техники': Carmodel.objects.all(),
        'Модели двигателя': Enginemodel.objects.all(),
        'Модели трансмиссии': Transmodel.objects.all(),
        'Модели ведущего моста': Axdrivemodel.objects.all(),
        'Модели управляемого моста': Axcontrolmodel.objects.all(),
        'Сервисные компании': Serviceorg.objects.all(),
    }

    return render(request, 'reference_admin.html', {
        'reference_models': reference_models,
        'active_tab': 'reference'  # для подсветки активной вкладки
    })


def add_reference_item(request, model_name):
    Model = get_model_class(model_name)
    if not Model:
        raise Http404("Справочник не найден")

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        Model.objects.create(name=name, description=description)
        return redirect('admin_reference')

    return render(request, 'reference_add_item.html', {
        'model_name': model_name,
        'active_tab': 'reference'
    })

def edit_reference_item(request, model_name, item_id):
    Model = get_model_class(model_name)
    if not Model:
        raise Http404("Справочник не найден")

    item = get_object_or_404(Model, id=item_id)

    if request.method == 'POST':
        item.name = request.POST.get('name')
        item.description = request.POST.get('description')
        item.save()
        return redirect('admin_reference')

    return render(request, 'reference_edit_item.html', {
        'model_name': model_name,
        'item': item,
        'active_tab': 'reference'
    })

def delete_reference_item(request, model_name, item_id):
    Model = get_model_class(model_name)
    if not Model:
        raise Http404("Справочник не найден")

    item = get_object_or_404(Model, id=item_id)

    if request.method == 'POST':
        item.delete()
        return redirect('admin_reference')

    return render(request, 'reference_confirm_delete.html', {
        'model_name': model_name,
        'item': item,
        'active_tab': 'reference'
    })
# Просмотр описания по ссылке
class RecoveryMethodDetailView(DetailView):
    model = Recoverymethod
    template_name = 'view_detail.html'  # Шаблон для отображения description
    context_object_name = 'method'
class FailnodeDetailView(DetailView):
    model = Failnode
    template_name = 'view_detail.html'  # Шаблон для отображения description
    context_object_name = 'method'
class ServiceorgDetailView(DetailView):
    model = Serviceorg
    template_name = 'view_detail.html'  # Шаблон для отображения description
    context_object_name = 'method'
class MaintenviewDetailView(DetailView):
    model = Maintenview
    template_name = 'view_detail.html'  # Шаблон для отображения description
    context_object_name = 'method'
class CarmodelDetailView(DetailView):
    model = Carmodel
    template_name = 'view_detail.html'  # Шаблон для отображения description
    context_object_name = 'method'
class EnginemodelDetailView(DetailView):
    model = Enginemodel
    template_name = 'view_detail.html'  # Шаблон для отображения description
    context_object_name = 'method'
class TransmodelDetailView(DetailView):
    model = Transmodel
    template_name = 'view_detail.html'  # Шаблон для отображения description
    context_object_name = 'method'
class AxdrivemodelDetailView(DetailView):
    model = Axdrivemodel
    template_name = 'view_detail.html'  # Шаблон для отображения description
    context_object_name = 'method'
class AxcontrolmodelDetailView(DetailView):
    model = Axcontrolmodel
    template_name = 'view_detail.html'  # Шаблон для отображения description
    context_object_name = 'method'