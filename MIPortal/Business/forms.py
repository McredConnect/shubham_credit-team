from django.forms import ModelForm
from Investors.models import Entity, EntityBusinessROIMapping, EntityInvestorRORMapping


class EntityForm(ModelForm):
    class Meta:
        model = Entity
        fields = '__all__'
        exclude = ['entity_id']

class EntityBusinessForm(ModelForm):
    class Meta:
        model = EntityBusinessROIMapping
        exclude =['entity_id', 'business_id']

class EntityInvestorForm(ModelForm):
    class Meta:
        model = EntityInvestorRORMapping
        exclude =['entity_id', 'investor_id']


