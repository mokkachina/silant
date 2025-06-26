from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.utils import timezone
from car.models import Car, Serviceorg
from maintenance.models import Maintenance, Complaints


class RoleAuthForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)
        if not user.is_active:
            raise forms.ValidationError("Аккаунт неактивен", code='inactive')

# class LoginForm(AuthenticationForm):
#     username = forms.CharField(label='Логин')
#     password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
#     class Meta:
#         model = get_user_model()
#         fields = ['username', 'password']
class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = '__all__'

class AdminCarAddForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = '__all__'
        widgets = {
            'datashipfactory': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control datetimepicker',
                    'max': timezone.now().strftime('%Y-%m-%dT%H:%M')
                }
            ),
            # Для других полей с датами добавьте аналогичные виджеты
        }
        labels = {
            'datashipfactory': 'Дата отгрузки с завода',
            # Остальные подписи полей
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and not self.instance.datashipfactory:
            self.initial['datashipfactory'] = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.datashipfactory:
            self.initial['datashipfactory'] = self.instance.datashipfactory.strftime('%Y-%m-%dT%H:%M')

    def __init__(self, *args, **kwargs):
        # Извлекаем пользователя перед вызовом родительского конструктора
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Здесь можно добавить логику фильтрации/настройки полей
        # Например, для менеджера:
        if self.user and self.user.is_manager:
            # Пример: ограничить выбор сервисных организаций
            if 'servicecompany' in self.fields:
                self.fields['servicecompany'].queryset = Serviceorg.objects.filter(
                    # ваши условия фильтрации
                )

class MaintenanceForm(forms.ModelForm):
    class Meta:
        model = Maintenance
        fields = '__all__'

class ComplaintsForm(forms.ModelForm):
    class Meta:
        model = Complaints
        fields = '__all__'


class MaintenanceCreateForm(forms.ModelForm):
    class Meta:
        model = Maintenance
        fields = [
            'car', 'viewmainten', 'datamainten', 'workhour',
            'workordernum', 'workorderdate', 'maintenorg', 'serviceorg'
        ]
        widgets = {
            'datamainten': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control',
                    'max': timezone.now().strftime('%Y-%m-%dT%H:%M')
                }
            ),
            'workorderdate': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control'
                }
            ),
            'workordernum': forms.TextInput(attrs={'class': 'form-control'}),
            'workhour': forms.NumberInput(attrs={'class': 'form-control'}),
            'viewmainten': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'maintenorg': 'Организация, проводившая ТО',
            'serviceorg': 'Сервисная компания',
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            # Фильтрация автомобилей
            if 'car' in self.fields:
                if user.is_client:
                    self.fields['car'].queryset = Car.objects.filter(user=user)
                elif user.is_service:
                    self.fields['car'].queryset = Car.objects.filter(servicecompany=user.service_org)

            # Настройка полей сервисной организации
            if 'serviceorg' in self.fields:
                if user.is_service:
                    self.fields['serviceorg'].initial = user.service_org
                    self.fields['serviceorg'].disabled = True
                elif user.is_client:
                    self.fields['serviceorg'].queryset = Serviceorg.objects.filter(
                        id__in=Car.objects.filter(user=user).values('servicecompany')
                    )

            # Фильтрация организаций, проводивших ТО
            if 'maintenorg' in self.fields:
                if user.is_service:
                    self.fields['maintenorg'].initial = user.service_org
                    self.fields['maintenorg'].disabled = True



class AdminComplaintsCreateForm(forms.ModelForm):
    class Meta:
        model = Complaints
        fields = [
            'car', 'databroke', 'workhour', 'failnode',
            'description', 'recoverymethod', 'usepart',
            'datamainten', 'restoredate', 'serviceorg'
        ]
        widgets = {
            'databroke': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control',
                    'max': timezone.now().strftime('%Y-%m-%dT%H:%M')
                }
            ),
            'datamainten': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control'
                }
            ),
            'restoredate': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control'
                }
            ),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'usepart': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'workhour': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'serviceorg': 'Сервисная организация',
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)



class ServMaintenanceCreateForm(forms.ModelForm):
    class Meta:
        model = Maintenance
        fields = [
            'car', 'viewmainten', 'datamainten', 'workhour',
            'workordernum', 'workorderdate', 'maintenorg', 'serviceorg'
        ]
        widgets = {
            'datamainten': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control',
                    'max': timezone.now().strftime('%Y-%m-%dT%H:%M')
                }
            ),
            'workorderdate': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control'
                }
            ),
            'workordernum': forms.TextInput(attrs={'class': 'form-control'}),
            'workhour': forms.NumberInput(attrs={'class': 'form-control'}),
            'viewmainten': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'maintenorg': 'Организация, проводившая ТО',
            'serviceorg': 'Сервисная компания',
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            # Фильтрация автомобилей
            if 'car' in self.fields:
                if user.is_client:
                    self.fields['car'].queryset = Car.objects.filter(user=user)
                elif user.is_service:
                    self.fields['car'].queryset = Car.objects.filter(servicecompany=user.service_org)

            # Настройка полей сервисной организации
            if 'serviceorg' in self.fields:
                if user.is_service:
                    self.fields['serviceorg'].initial = user.service_org
                    self.fields['serviceorg'].disabled = True
                elif user.is_client:
                    self.fields['serviceorg'].queryset = Serviceorg.objects.filter(
                        id__in=Car.objects.filter(user=user).values('servicecompany')
                    )

            # Фильтрация организаций, проводивших ТО
            if 'maintenorg' in self.fields:
                if user.is_service:
                    self.fields['maintenorg'].initial = user.service_org
                    self.fields['maintenorg'].disabled = True

# def __init__(self, *args, **kwargs):
#         # Извлекаем пользователя перед вызовом родительского конструктора
#         self.user = kwargs.pop('user', None)
#         super().__init__(*args, **kwargs)
#
#         # Фильтруем автомобили для сервисных организаций
#         if self.user and self.user.is_service and 'car' in self.fields:
#             self.fields['car'].queryset = Car.objects.filter(
#                 servicecompany=self.user.service_org
#             )


class ServComplaintsCreateForm(forms.ModelForm):
    class Meta:
        model = Complaints
        fields = [
            'car', 'databroke', 'workhour', 'failnode',
            'description', 'recoverymethod', 'usepart',
            'datamainten', 'restoredate', 'serviceorg'
        ]
        widgets = {
            'databroke': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control',
                    'max': timezone.now().strftime('%Y-%m-%dT%H:%M')
                }
            ),
            'datamainten': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control'
                }
            ),
            'restoredate': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control'
                }
            ),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'usepart': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'workhour': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'serviceorg': 'Сервисная организация',
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if self.user and self.user.is_service and 'car' in self.fields:
            self.fields['car'].queryset = Car.objects.filter(
                servicecompany=self.user.service_org
            )