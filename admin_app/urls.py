from django.urls import path
from . import views


urlpatterns = [

    
    path('', views.AdminDashboardView.as_view(), name='admin_dashboard'),
    path('users/', views.AdminUserListView.as_view(), name='admin_users'),
    path('users/<int:pk>/', views.AdminUserDetailView.as_view(), name='admin_user_detail'),
    path('organizations/', views.AdminOrganizationListView.as_view(), name='admin_organization_list'),
    path('organizations/<int:pk>/', views.AdminOrganizationDetailView.as_view(), name='admin_organization_detail'),
    path('templates/', views.AdminTemplateListView.as_view(), name='admin_template_list'),
    path('templates/create/', views.AdminTemplateCreateView.as_view(), name='admin_template_create'),
    path('templates/<int:pk>/edit/', views.AdminTemplateUpdateView.as_view(), name='admin_template_edit'),
    path('templates/<int:pk>/', views.AdminTemplateDetailView.as_view(), name='admin_template_detail'),
    path('templates/<int:template_pk>/services/add/', views.AdminServiceAddView.as_view(), name='admin_service_add'),
    path('templates/services/<int:service_pk>/env/add/', views.AdminEnvironmentAddView.as_view(), name='admin_environment_add'),
    path('templates/env/<int:pk>/update/', views.AdminEnvironmentUpdateView.as_view(), name='admin_environment_update'),
    path('templates/env/<int:pk>/delete/', views.AdminEnvironmentDeleteView.as_view(), name='admin_environment_delete'),
    path('websites/', views.AdminWebsiteListView.as_view(), name='admin_website_list'),
    path('websites/create/', views.AdminWebsiteCreateView.as_view(), name='admin_website_create'),
    path('websites/<int:pk>/update/', views.AdminWebsiteUpdateView.as_view(), name='admin_website_update'),
    path('websites/<int:pk>/', views.AdminWebsiteDetailView.as_view(), name='admin_website_detail'),
    path('websites/<int:pk>/sections/add/', views.AdminSectionAddView.as_view(), name='admin_section_add'),
    path('websites/<int:website_pk>/sections/<int:section_pk>/edit/', views.AdminSectionEditView.as_view(), name='admin_section_edit'),
    path('websites/<int:website_pk>/sections/<int:section_pk>/update/', views.AdminSectionUpdateView.as_view(), name='admin_section_update'),
    path('websites/<int:website_pk>/sections/<int:section_pk>/delete/', views.AdminSectionDeleteView.as_view(), name='admin_section_delete'),
    path('settings/general/', views.AdminSettingsGeneralView.as_view(), name='admin_settings_general'),
    path('settings/credentials/manage/', views.AdminCredentialsView.as_view(), name='admin_credentials'),
    path('settings/credentials/', views.CreadentialsFormView.as_view(), name='credentials_form'),
]