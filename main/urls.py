from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include


urlpatterns = [
    path('', views.home_page, name='home'),
    path('all/breakfast', views.all_breakfast, name='all_breakfast'),
    path('all/dinner', views.all_dinner, name='all_dinner'),
    url(r'^recipe/([0-9]{1,5})', views.get_one_recipe, name="view_recipe"),
    url(r'^recipe/add_coment/([0-9]{1,5})', views.add_coment),
    url(r'^recipe/delete_coment/([0-9]{1,5})/([0-9]{1,5})', views.delete_coment)
]