from django.urls import path, include
from accounts.views import RoleLoginView, AdminCarListView, AdminMaintenanceListView, AdminCompListView, \
    AdminCarUpdateView, AdminMainUpdateView, AdminComplUpdateView, AdminCarCreateView, AdminCarDeleteView, \
    AdminMaintCreateView, AdminComplCreateView, AdminComplDeleteView, AdminMaintDeleteView

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
]