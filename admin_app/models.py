from django.db import models

# Create your models here.
class Creadentials(models.Model):
    railway_auth_token = models.CharField(max_length=255)
    railway_workspace_id = models.CharField(max_length=255)
    raiway_template_id = models.CharField(max_length=255)


    
class Project(models.Model):
    project_id = models.CharField(max_length=100)
    environment_id = models.CharField(max_length=100)
 
    def __str__(self):
        return self.project_id
    
class DeploymentTemplate(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=False)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    default_domain = models.CharField(max_length=100, null=True, blank=True)
    workflow_id = models.CharField(max_length=100, null=True, blank=True)   
    def __str__(self):
        return self.name

class TemplateService(models.Model):
    name = models.CharField(max_length=255)
    deployment_template = models.ForeignKey(DeploymentTemplate, on_delete=models.CASCADE)
    docker_image = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name
      
class Environment(models.Model):
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
    template_service_id = models.ForeignKey(TemplateService, on_delete=models.CASCADE)
    def __str__(self):
        return self.name
