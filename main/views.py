from django.shortcuts import render, redirect, HttpResponse
from .forms import *
from .models import *
from accounts.models import *


def home_page(request):
    if request.method == 'POST':
        form = FilteringRecipes(request.POST)
        if form.is_valid():
            if form.cleaned_data['selection_field'] == 'Завтрак':
                return redirect('all_breakfast')
            elif form.cleaned_data['selection_field'] == 'Ужин':
                return redirect('all_dinner')
    else:
        form = FilteringRecipes()
    all_recipe = Recipe.objects.order_by('id')
    all_typing = Typing.objects.order_by('recipe_id')
    all_rating = Rating.objects.order_by('recipe_id')
    # form = FilteringRecipes()
    context = {
        'info': "Здесь представлены все рецепты:",
        'title': "Все рецепты",
        'heading': "Все рецепты",
        'all_recipe': all_recipe,
        'all_typing': all_typing,
        'all_rating': all_rating,
        'form': form
    }
    return render(request, "main/index.html", context)


def all_breakfast(request):
    if request.method == 'POST':
        form = FilteringRecipes(request.POST)
        if form.is_valid():
            if form.cleaned_data['selection_field'] == 'Завтрак':
                return redirect('all_breakfast')
            elif form.cleaned_data['selection_field'] == 'Ужин':
                return redirect('all_dinner')
    else:
        form = FilteringRecipes()
    all_recipe = Recipe.objects.filter(meal_type='Завтрак')
    all_typing = Typing.objects.order_by('id')
    all_rating = Rating.objects.order_by('id')
    # form = FilteringRecipes()
    context = {
        'info': "Здесь представлены все завтраки:",
        'title': "Все завтраки",
        'heading': "Все завтраки",
        'all_recipe': all_recipe,
        'all_typing': all_typing,
        'all_rating': all_rating,
        'form': form

    }
    return render(request, "main/index.html", context)


def all_dinner(request):
    if request.method == 'POST':
        form = FilteringRecipes(request.POST)
        if form.is_valid():
            if form.cleaned_data['selection_field'] == 'Завтрак':
                return redirect('all_breakfast')
            elif form.cleaned_data['selection_field'] == 'Ужин':
                return redirect('all_dinner')
    else:
        form = FilteringRecipes()
    all_recipe = Recipe.objects.filter(meal_type='Ужин')
    all_typing = Typing.objects.order_by('id')
    all_rating = Rating.objects.order_by('id')
    # form = FilteringRecipes()
    context = {
        'info': "Здесь представлены все завтраки:",
        'title': "Все завтраки",
        'heading': "Все завтраки",
        'all_recipe': all_recipe,
        'all_typing': all_typing,
        'all_rating': all_rating,
        'form': form

    }
    return render(request, "main/index.html", context)


def get_one_recipe(request, id_recipe):

    try:
        one_recipe = Recipe.objects.get(id=id_recipe)

    except Exception:
        return render(request, "main/resipe.html",
                      {'error': 'Страница с данным рецептом не найдена '
                                'или у вас нету прав к нему',
                       'heading': "Ошибка",
                       })
    # нужно получить коментарий
    coment_recipe = Comments.objects.filter(recipe_id=id_recipe)
    typing_recipe = Typing.objects.get(recipe_id=one_recipe)
    context = {
       'error': 'zero',
        'autor': str(one_recipe.user.last_name) + " " + str(one_recipe.user.first_name),
        'heading': str(one_recipe.name),
        'title':  str(one_recipe.name),
        'text': str(one_recipe.text),
        'video_url': str(one_recipe.url_video),
        'images': one_recipe.image,
        'comments': coment_recipe,
        'id_recipe': str(id_recipe),
        'user': request.user, #id пользоватля, который запрашивает страницу
        'typing': typing_recipe,
    }
    return render(request, "main/resipe.html", context)


def add_coment(request, id_recipe):
    user = AdvUser.objects.get(id=request.user.id)
    one_recipe = Recipe.objects.get(id=id_recipe)
    text = request.GET.get('text_coment')
    buffer = Comments(recipe_id=one_recipe, user=user, text=text)
    buffer.save()
    return redirect("/recipe/"+str(id_recipe))


def delete_coment(request, id_coment, id_recipe):
    one_coment = Comments.objects.get(id=id_coment)
    if request.user.id == one_coment.user.id:
        one_coment.delete()
        return redirect("/recipe/" + str(id_recipe))
    else:
        HttpResponse(status=404)
