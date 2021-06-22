from django.shortcuts import render
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


def home_page(request):
    context = {
        'info': "Здесь представлены все рецепты:",
        'title': "Главная страница",
        'heading': "Добро пожаловать"
    }
    return render(request, "main/index.html", context)
