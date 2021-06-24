from .models import Recipe
from django.forms import ModelForm, TextInput, NumberInput, DateInput, TimeInput, EmailInput


class RecipeForm(ModelForm):

    class Meta:
        model = Recipe
        fields = ['meal_type']