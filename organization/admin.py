from django.contrib import admin

from organization.models import Organization, Service

# Register your models here.

admin.site.register(Organization)
admin.site.register(Service)