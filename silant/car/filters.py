import django_filters

from car.models import Car, Carmodel, Enginemodel, Transmodel, Axdrivemodel, Axcontrolmodel, Serviceorg
from maintenance.models import Maintenance, Complaints, Maintenview, Recoverymethod, Failnode


class CarFilter(django_filters.FilterSet):
    # Для ForeignKey полей используем ModelChoiceFilter с явным указанием queryset
    carmodel = django_filters.ModelChoiceFilter(
        queryset=Carmodel.objects.all(),
        field_name='carmodel',
        label='Модель техники'
    )

    enginemodel = django_filters.ModelChoiceFilter(
        queryset=Enginemodel.objects.all(),
        field_name='enginemodel',
        label='Модель двигателя'
    )

    transmodel = django_filters.ModelChoiceFilter(
        queryset=Transmodel.objects.all(),
        field_name='transmodel',
        label='Модель трансмиссии'
    )

    axdrivemodel = django_filters.ModelChoiceFilter(
        queryset=Axdrivemodel.objects.all(),
        field_name='axdrivemodel',
        label='Модель ведущего моста'
    )

    axcontrolmodel = django_filters.ModelChoiceFilter(
        queryset=Axcontrolmodel.objects.all(),
        field_name='axcontrolmodel',
        label='Модель управляемого моста'
    )

    # Для обычных полей используем CharFilter
    carnumber = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Зав. № машины'
    )

    class Meta:
        model = Car
        fields = []

class MaintenanceFilter(django_filters.FilterSet):
    viewmainten = django_filters.ModelChoiceFilter(
        queryset=Maintenview.objects.all(),
        field_name='viewmainten',
        label='Вид ТО'
    )
    carnumber = django_filters.CharFilter(
        field_name='car__carnumber',  # Связь через ForeignKey
        lookup_expr='icontains',
        label='Зав.номер машины'
    )
    serviceorg = django_filters.ModelChoiceFilter(
        queryset=Serviceorg.objects.all(),
        field_name='serviceorg',
        label='Сервисная компания'
    )
    class Meta:
        model = Maintenance
        fields = []

class ComplaintsFilter(django_filters.FilterSet):
    failnode = django_filters.ModelChoiceFilter(
        queryset=Failnode.objects.all(),  # Указываем явно queryset
        field_name='failnode',
        label='Узел отказа'
    )

    recoverymethod = django_filters.ModelChoiceFilter(
        queryset=Recoverymethod.objects.all(),
        field_name='recoverymethod',
        label='Способ восстановления'
    )
    serviceorg = django_filters.ModelChoiceFilter(
        queryset=Serviceorg.objects.all(),
        field_name='serviceorg',
        label='Сервисная компания'
    )

    class Meta:
        model = Complaints
        fields = []