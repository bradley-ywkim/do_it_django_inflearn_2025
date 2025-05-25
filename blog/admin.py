from django.contrib import admin
from .models import Post, Category

admin.site.register(Post)

class CategoryAdmin(admin.ModelAdmin): #django에서 제공하는 기능
    prepopulated_fields = {'slug':('name',)}
admin.site.register(Category, CategoryAdmin)

