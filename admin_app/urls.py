from django.urls import path
from .import views

urlpatterns = [
    path('settings/credentials/', views.CreadentialsFormView.as_view(), name='credentials_form'),
    path('settings/template-list/', views.TemplateListView.as_view(), name='template_list'),
    path('settings/template/<int:pk>/', views.TemplateDetailedView.as_view(), name='template_detailed_view'),
    path('settings/service/add/<int:template_pk>/', views.ServiceFormView.as_view(), name='service_form'),
    path('settings/environment/add/<int:service_pk>/', views.EnvironmentFormView.as_view(), name='environment_add'),
    path('settings/environment/update/<int:pk>/', views.EnvironmentUpdateView.as_view(), name='environment_update'),
    path('settings/environment/delete/<int:pk>/', views.EnvironmentDeleteView.as_view(), name='environment_delete'),
]
