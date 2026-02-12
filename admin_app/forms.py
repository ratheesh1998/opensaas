

from admin_app.models import Creadentials, DeploymentTemplate, Environment, TemplateService
from django import forms


class CreadentialsForm(forms.ModelForm):
    class Meta:
        model = Creadentials
        fields = '__all__'

class DeploymentTemplateForm(forms.ModelForm):
    class Meta:
        model = DeploymentTemplate
        fields = ['name', 'description', 'published']

class TemplateServiceForm(forms.ModelForm):
    class Meta:
        model = TemplateService
        exclude = ['deployment_template']

class EnvironmentForm(forms.ModelForm):
    class Meta:
        model = Environment
        fields = ['name', 'value']