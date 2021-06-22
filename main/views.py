from django.shortcuts import render

# Create your views here.


def home_page(request):
    context = {
        'info': "Здесь представлены все рецепты:",
        'title': "Главная страница",
        'heading': "Добро пожаловать"
    }
    return render(request, "main/index.html", context)
