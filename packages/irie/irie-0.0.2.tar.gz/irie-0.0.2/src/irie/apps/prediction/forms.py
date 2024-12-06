#===----------------------------------------------------------------------===#
#
#         STAIRLab -- STructural Artificial Intelligence Laboratory
#
#===----------------------------------------------------------------------===#
from django import forms
from irie.apps.prediction.models import PredictorModel


# class CsiForm(forms.Form):
#     option1 = forms.CharField(label='Option 1', max_length=100)
#     option2 = forms.CharField(label='Option 2', max_length=100)
#     file_upload = forms.FileField(label='Upload a file', required=True)


class PredictorForm(forms.ModelForm):
    class Meta:
        model = PredictorModel
        fields = '__all__'
        exclude = ['render_file', 'metrics', 'active', 'entry_point', 'config', 'protocol']
