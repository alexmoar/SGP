from django.urls import path

from evaluator import views

app_name = 'evaluator'
urlpatterns = [
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
]
