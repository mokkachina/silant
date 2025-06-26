from django.urls import path
from . import views
from .views import ClientCarListView, ClientMaintenanceListView, ClientCompListView, MaintenanceUpdateView, \
    ClientCarCreateView, ClientMaintenDeleteView

urlpatterns = [
    path('', views.CarSearchView.as_view(), name='home'),
    path('client/car/',ClientCarListView.as_view(), name='client_car'),
    path('client/maintenance/',ClientMaintenanceListView.as_view(), name='client_mainten'),
    path('client/complaints/',ClientCompListView.as_view(), name='client_compl'),
    path('maintenance/<int:pk>/edit/', MaintenanceUpdateView.as_view(), name='edit_mainten'),
    path('client/maintenance/create/', ClientCarCreateView.as_view(), name='client_main_create'),
    path('complaints/<int:pk>/delete/', ClientMaintenDeleteView.as_view(), name='client_mainten_delete'),
]