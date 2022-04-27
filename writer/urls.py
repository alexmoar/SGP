from django.urls import path

from writer import views

app_name = 'writer'
urlpatterns = [
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
]
