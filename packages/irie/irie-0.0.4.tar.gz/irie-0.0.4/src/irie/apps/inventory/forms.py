#===----------------------------------------------------------------------===#
#
#         STAIRLab -- STructural Artificial Intelligence Laboratory
#
#===----------------------------------------------------------------------===#
from django import forms
from irie.apps.inventory.models import Asset

class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = '__all__'
