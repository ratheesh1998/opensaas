from django.db import models

# Create your models here.
class Creadentials(models.Model):
    railway_auth_token = models.CharField(max_length=255)
    railway_workspace_id = models.CharField(max_length=255)
    raiway_template_id = models.CharField(max_length=255)