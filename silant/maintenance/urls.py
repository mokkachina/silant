from django.urls import path
from . import views
from .views import ServCarListView, ServMaintenanceListView, ServCompListView, ServMainUpdateView, ServComplUpdateView, \
    ServMainCreateView, ServComplCreateView, MaintenanceDeleteView, ComplDeleteView

urlpatterns = [

    path('service/cars/', ServCarListView.as_view(), name='serv_car'),
    path('service/maintenance/', ServMaintenanceListView.as_view(), name='serv_mainten'),
    path('service/complaints/', ServCompListView.as_view(), name='serv_compl'),
    path('service/maintenance/<int:pk>/edit/', ServMainUpdateView.as_view(), name='main_edit_serv'),
    path('service/complaints/<int:pk>/edit/', ServComplUpdateView.as_view(), name='com_edit_serv'),
    path('service/maintenance/create/', ServMainCreateView.as_view(), name='serv_main_create'),
    path('service/complaints/create/', ServComplCreateView.as_view(), name='serv_compl_create'),
    path('maintenance/<int:pk>/delete/', MaintenanceDeleteView.as_view(), name='maintenance_delete'),
    path('complaints/<int:pk>/delete/', ComplDeleteView.as_view(), name='complaints_delete'),
]