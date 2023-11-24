from django.contrib import admin

from main.models import Todo, Category

admin.site.register((Todo,Category))
