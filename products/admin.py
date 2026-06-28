from django.contrib import admin

from .models import Category, Product, File


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['parent', 'title', 'is_enabled', 'created_time']
    list_filter = ['is_enabled', 'parent', 'created_time']
    search_fields = ['title']

class FileinlineAdmin(admin.StackedInline):
    model = File
    fields = ['title', 'file_type', 'file', 'is_enabled']
    extra = 0 

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_enabled', 'created_time']
    list_filter = ['is_enabled', 'created_time']
    filter_horizontal = ['categories']
    search_fields = ['title']
    inlines = [FileinlineAdmin]