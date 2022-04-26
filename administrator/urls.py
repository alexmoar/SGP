from django.urls import path

from administrator import views

app_name = 'administrator'
urlpatterns = [
    path('/dashboard/', views.render_index, name='dashboard'),
]
