from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path('', views.home_page, name='home'),
    url(r'^recipe/([0-9]{1,5})', views.get_one_recipe, name="view_recipe"),
    path('recipes/chosen', views.view_chosen_recipes, name='chosen_recipes'),
    path('recipes/yours', views.view_yours_recipe, name='yours_recipe'),
    url(r'^recipe/add_coment/([0-9]{1,5})', views.add_coment),
    url(r'^recipe/delete_coment/([0-9]{1,5})/([0-9]{1,5})', views.delete_coment),
    url(r'^recipe/add_favorite/([0-9]{1,5})', views.add_favorite),
    url(r'^recipe/delete_favorite/([0-9]{1,5})', views.delete_favorite),
    url(r'^recipe/push_rating/([0-9]{1,5})/([0-5])', views.push_rating),
    url(r'^recipe/add_page', views.add_page, name="add_recipe"),
    url(r'^recipe/add_ricipe', views.add_ricipe),
    url(r'^recipe/delete_recipe/([0-9]{1,5})', views.delete_recipe),
    url(r'^recipe/update_recipe/([0-9]{1,5})', views.update_recipe),
    url(r'^recipe/edit_page/([0-9]{1,5})', views.edit_page),
    url(r'^error', views.error),
]

urlpatterns += staticfiles_urlpatterns()

