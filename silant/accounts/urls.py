from django.urls import path, include
from accounts.views import RoleLoginView, AdminCarListView, AdminMaintenanceListView, AdminCompListView, \
    AdminCarUpdateView, AdminMainUpdateView, AdminComplUpdateView, AdminCarCreateView, AdminCarDeleteView, \
    AdminMaintCreateView, AdminComplCreateView, AdminComplDeleteView, AdminMaintDeleteView, admin_reference, \
    add_reference_item, edit_reference_item, delete_reference_item, RecoveryMethodDetailView, \
    FailnodeDetailView, ServiceorgDetailView, MaintenviewDetailView, CarmodelDetailView, EnginemodelDetailView, \
    TransmodelDetailView, AxdrivemodelDetailView, AxcontrolmodelDetailView

from allauth.account.views import LogoutView

from car import views





urlpatterns = [
    path('', views.CarSearchView.as_view(), name='home'),
    path('accounts/login/', RoleLoginView.as_view(template_name='includes/login.html'), name='login'),
    path(
        'accounts/logout/',
        LogoutView.as_view(template_name='includes/logout.html'),
        name='account_logout'
    ),
    path('manager/cars/', AdminCarListView.as_view(), name='admin_car'),
    path('manager/maintenance/', AdminMaintenanceListView.as_view(), name='admin_mainten'),
    path('manager/complaints/', AdminCompListView.as_view(), name='admin_compl'),
    path('manager/cars/<int:pk>/edit/', AdminCarUpdateView.as_view(), name='car_edit_manager'),
    path('manager/maintenance/<int:pk>/edit/', AdminMainUpdateView.as_view(), name='main_edit_manager'),
    path('manager/complaints/<int:pk>/edit/', AdminComplUpdateView.as_view(), name='com_edit_manager'),
    path('manager/cars/create/', AdminCarCreateView.as_view(), name='admin_car_create'),
    path('manager/maintenance/create/', AdminMaintCreateView.as_view(), name='admin_main_create'),
    path('manager/complaints/create/', AdminComplCreateView.as_view(), name='admin_compl_create'),
    path('manager/car/<int:pk>/delete/', AdminCarDeleteView.as_view(), name='admin_car_delete'),
    path('manager/maintenance/<int:pk>/delete/', AdminMaintDeleteView.as_view(), name='admin_main_delete'),
    path('manager/complaints/<int:pk>/delete/', AdminComplDeleteView.as_view(), name='admin_compl_delete'),
    path('manager/reference/', admin_reference, name='admin_reference'),
    path('manager/reference/add/<str:model_name>/', add_reference_item, name='add_reference_item'),
    path('manager/reference/edit/<str:model_name>/<int:item_id>/', edit_reference_item, name='edit_reference_item'),
    path('manager/reference/delete/<str:model_name>/<int:item_id>/', delete_reference_item, name='delete_reference_item'),
    path('recoverymethod/<int:pk>/', RecoveryMethodDetailView.as_view(), name='view_recoverymethod'),
    path('failnode/<int:pk>/', FailnodeDetailView.as_view(), name='view_failnode'),
    path('serviceorg/<int:pk>/', ServiceorgDetailView.as_view(), name='view_serviceorg'),
    path('maintenview/<int:pk>/', MaintenviewDetailView.as_view(), name='view_maintenview'),
    path('carmodel/<int:pk>/', CarmodelDetailView.as_view(), name='view_carmodel'),
    path('enginemodel/<int:pk>/', EnginemodelDetailView.as_view(), name='view_enginemodel'),
    path('transmodel/<int:pk>/', TransmodelDetailView.as_view(), name='view_transmodel'),
    path('axdrivemodel/<int:pk>/', AxdrivemodelDetailView.as_view(), name='view_axdrivemodel'),
    path('axcontrolmodel/<int:pk>/', AxcontrolmodelDetailView.as_view(), name='view_axcontrolmodel'),
]