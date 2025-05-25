from django.contrib import admin
from .models import Post, Category, Tag

admin.site.register(Post)

class CategoryAdmin(admin.ModelAdmin): #django에서 제공하는 기능
    prepopulated_fields = {'slug':('name',)}

class TagAdmin(admin.ModelAdmin): #django에서 제공하는 기능
    prepopulated_fields = {'slug':('name',)}


admin.site.register(Category, CategoryAdmin)

admin.site.register(Tag, TagAdmin)
