from tests.models import *
from django import forms


class blogform(forms.ModelForm):
    class Meta:
        model = Blog
        fields = '__all__'