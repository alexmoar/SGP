from django.contrib import admin

# Register your models here.
from projects.models import Score, Project, Question, Comment


@admin.register(Score)
class OptionMenuAdmin(admin.ModelAdmin):
    list_display = ('score', 'evaluator', 'project', 'question')

    list_filter = ('evaluator', 'question')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('author', 'title', 'status')

    list_filter = ('author', 'status')


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'answer', 'project')

    list_filter = ('project',)


@admin.register(Comment)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('author', 'project')

    list_filter = ('project',)
