from django.urls import path
from .import views

urlpatterns = [
    path(
        'create-organization/',
        views.CreateOrganizationView.as_view(),
        name='create_organization'
    ),
    path('',views.ListOrganizationView.as_view(),name='list_organization'),
    path('<int:id>/',views.DetailedOrganizationView.as_view(),name='detailed_organization') ,
    path('deployment_reload/<int:id>/',views.DeploymentReloadView.as_view(),name='deployment_reload'),
    path('add_env/<int:id>/',views.AddEnvView.as_view(),name='add_env'),
    path('update_env/<int:id>/',views.UpdateEnvView.as_view(),name='update_env'),
    path('delete_organization/<int:id>/',views.DeleteOrganizationView.as_view(),name='delete_organization'),
    path('deployment_status/<int:id>/',views.DeployementStatusView.as_view(),name='deployment_status'),
]
