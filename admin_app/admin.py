from django.contrib import admin

from admin_app.models import Creadentials, DeploymentTemplate, TemplateService, Environment,Project

# Register your models here.
admin.site.register([Creadentials, DeploymentTemplate, TemplateService, Environment,Project])