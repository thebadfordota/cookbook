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
    COMPLEXITY_CHOICES = (
        ('1', 'Очень легко'),
        ('2', 'Легко'),
        ('3', 'Средне'),
        ('4', 'Сложно'),
        ('5', 'Очень сложно'),
        ('6', 'Любая сложность'),
    )
    COOKING_TIME_CHOICES = (
        ('15', '15 минут'),
        ('30', '30 минут'),
        ('60', '1 час'),
        ('120', '2 часа'),
        ('240', '4 часа'),
        ('360', '6 часов'),
        ('480', '8 часов'),
        ('600', '10 часов'),
        ('9', 'Любое время'),
    )
    # selection_field = forms.ChoiceField(choices=((1, "English"), (2, "German"), (3, "French")))

    selection_meal = forms.ChoiceField(
        choices=MEAL_CHOICES,
        required=False,
        initial='Все категории'
    )
    selection_complexity = forms.ChoiceField(
        choices=COMPLEXITY_CHOICES,
        required=False,
        initial='6'
    )
    selection_cooking_time = forms.ChoiceField(
        choices=COOKING_TIME_CHOICES,
        required=False,
        initial='9'
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


