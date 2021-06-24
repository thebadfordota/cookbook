from .models import Recipe, Ingredients
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
        ('Все категории', 'Все категории'),
    )
    # selection_field = forms.ChoiceField(choices=((1, "English"), (2, "German"), (3, "French")))

    selection_field = forms.ChoiceField(
        choices=MEAL_CHOICES,
        required=False
    )


class FilteringIngredients(forms.Form):
    all_name = Ingredients.objects.all()

    # ingredients = forms.ChoiceField(
    #    choices=all_name
    # )
    # ingredients = forms.ModelChoiceField(queryset=Recipe.objects.values_list('name'))
    ingredients = forms.ModelChoiceField(queryset=Ingredients.objects.all(), required=False)

    #model = Recipe
    #ingredients = forms.ModelChoiceField(queryset=Recipe.objects.all().order_by('name'))


