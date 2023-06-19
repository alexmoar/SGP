from django.contrib import admin

from evaluator.models import Evaluator


# Register your models here.


@admin.register(Evaluator)
class OptionMenuAdmin(admin.ModelAdmin):
    list_display = ('user', 'category')
