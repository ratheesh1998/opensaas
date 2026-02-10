


from django import forms

from organization.models import Env, Organization


class OrganizationForm(forms.ModelForm):
    docker_image = forms.CharField(max_length=100, label='Docker Image')
    database_name = forms.ChoiceField( label='Database Name',choices=[('postgres', 'Postgres'), ('mysql', 'MySQL')])

    class Meta:
        model = Organization
        fields = ['name','docker_image', 'database_name']


class EnvForm(forms.ModelForm):
    service = forms.ChoiceField( label='Service' , choices=[('service', 'Service'), ('database', 'Database')], required=True)
    class Meta:
        model = Env
        fields = ['key', 'value','organization_id']