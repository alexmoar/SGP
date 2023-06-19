from django.contrib import admin

from core.models import Category


# Register your models here.


@admin.register(Category)
class OptionMenuAdmin(admin.ModelAdmin):
    list_display = ('name',)

