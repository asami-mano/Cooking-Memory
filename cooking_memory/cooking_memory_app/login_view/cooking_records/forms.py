from django import forms
from .models import CookingRecord, Recipe

class CookingRecordForm(forms.ModelForm):
    class Meta:
        model = CookingRecord
        fields = ['date', 'cooking_category', 'image_url', 'cooking_easiness', 'memo']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date','class': 'form-control'}),
            'memo': forms.Textarea(attrs={'rows': 3}),
        }
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
