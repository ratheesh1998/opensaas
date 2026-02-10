

from admin_app.models import Creadentials
from django import forms


class CreadentialsForm(forms.ModelForm):
    class Meta:
        model = Creadentials
        fields = '__all__'