from django import forms
from .models import CookingRecord, CookingCategory

class CookingRecordForm(forms.ModelForm):
    class Meta:
        model = CookingRecord
        fields = ['date', 'cooking_category', 'image_url', 'cooking_easiness', 'memo']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'memo': forms.Textarea(attrs={'rows': 3}),
        }
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user.share_group:
            self.fields['cooking_category'].queryset = CookingCategory.objects.filter(user__share_group=user.share_group)
        else:
            self.fields['cooking_category'].queryset = CookingCategory.objects.filter(user=user)