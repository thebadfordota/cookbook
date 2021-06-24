from .models import Recipe
from django.forms import ModelForm, TextInput, NumberInput, DateInput, TimeInput, EmailInput, ChoiceField
from django import forms


class RecipeForm(ModelForm):

    class Meta:
        model = Recipe
        fields = ['meal_type']


class FilteringRecipes(forms.Form):
    MEAL_CHOICES = (
        ('Завтрак', 'Завтрак'),
        ('Обед', 'Обед'),
        ('Ужин', 'Ужин'),
        ('Напиток', 'Напиток'),
        ('Десерт', 'Десерт'),
    )
    # selection_field = forms.ChoiceField(choices=((1, "English"), (2, "German"), (3, "French")))

    selection_field = forms.ChoiceField(
        choices=MEAL_CHOICES
    )
