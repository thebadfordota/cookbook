from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include


urlpatterns = [
    path('', views.home_page, name='home'),
    url(r'^recipe/([0-9]{1,5})', views.get_one_recipe, name="view_recipe"),
    url(r'^recipe/add_coment/([0-9]{1,5})', views.add_coment),
    url(r'^recipe/delete_coment/([0-9]{1,5})/([0-9]{1,5})', views.delete_coment),
    url(r'^recipe/add_favorite/([0-9]{1,5})', views.add_favorite),
    url(r'^recipe/delete_favorite/([0-9]{1,5})', views.delete_favorite),
    url(r'^recipe/push_rating/([0-9]{1,5})/([0-5])', views.push_rating),
    url(r'^recipe/add_page', views.add_page, name="add_recipe"),
    url(r'^recipe/add_ricipe', views.add_ricipe),
    url(r'^error', views.error),
]