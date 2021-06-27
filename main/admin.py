from django.contrib import admin
from .models import *


admin.site.register(Recipe)
admin.site.register(Rating)
admin.site.register(Ingredients)
admin.site.register(FavoriteDishes)
admin.site.register(Comments)