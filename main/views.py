from django.shortcuts import render
from .forms import RecipeForm
from .models import Recipe


def home_page(request):
    model = Recipe
    form = RecipeForm()
    context = {
        'info': "Здесь представлены все рецепты:",
        'title': "Главная страница",
        'heading': "Добро пожаловать",
        'form': form
    }
    return render(request, "main/index.html", context)
