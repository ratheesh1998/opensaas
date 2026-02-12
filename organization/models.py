from django.db import models

from admin_app.models import DeploymentTemplate, Project, TemplateService


class Organization(models.Model):
    name = models.CharField(max_length=100)
    deployment_template_id = models.ForeignKey(DeploymentTemplate, on_delete=models.SET_NULL, null=True, blank=True)
    default_domain = models.CharField(max_length=100, null=True, blank=True)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return self.name
    
class Env(models.Model):
    key = models.CharField(max_length=100)
    value = models.CharField(max_length=100)
    organization_id = models.ForeignKey(Organization, on_delete=models.CASCADE , null=True, blank=True )
    service = models.CharField(max_length=100, null=True, blank=True,choices=[('service', 'Service'), ('database', 'Database')])

    def __str__(self):
        return f"{self.key}: {self.value}"

class Service(models.Model):
    organization_id = models.ForeignKey(Organization, on_delete=models.CASCADE , null=True, blank=True )
    service_id = models.CharField(max_length=100, null=True, blank=True)
    postgres_service_id = models.CharField(max_length=100, null=True, blank=True)
    volume_id = models.CharField(max_length=100, null=True, blank=True)
    

    def __str__(self):
        return self.service_id + " " + self.organization_id.name