from django import forms
from .models import CookingRecord

class CookingRecordForm(forms.ModelForm):
    class Meta:
        model = CookingRecord
        fields = ['date', 'cooking_category', 'image_url', 'cooking_easiness', 'is_favorite', 'memo',]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'memo': forms.Textarea(attrs={'rows': 3}),
        }
