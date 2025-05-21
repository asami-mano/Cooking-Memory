from django import forms
from .models import Recipe

class RecipeForm(forms.ModelForm):
    recipe_url = forms.URLField(
        label='URL',
        required=True,
        error_messages={
            'invalid': '有効なURLを入力してください。',  # カスタムメッセージ
        },
        widget=forms.TextInput(attrs={'class': 'input-large'})
    )
    
    class Meta:
        model = Recipe
        fields = ['name', 'recipe_url']
