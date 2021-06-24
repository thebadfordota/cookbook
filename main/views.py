from django.shortcuts import render
<<<<<<< HEAD
from .forms import RecipeForm
from .models import Recipe
=======
from .models import *
# Create your views here.
"""
Дальше пойдёт мои функции для удобно взимодействия с моделями
проверка на дурака тоже тут проходит 
"""
class user_api:
    def delete(self):
        pass
    def update(self):
        pass
    def add(self, fisrt_name, last_name, email, admin_status):
        pass
    def get_info(self):
        pass
>>>>>>> 59a1c56379bd45c76a872a41d90db0b2d7f4d8c8


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
