from django.contrib import admin

from organization.models import Organization, Project, Service

# Register your models here.

admin.site.register(Organization)
admin.site.register(Project)
admin.site.register(Service)