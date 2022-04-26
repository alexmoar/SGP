from django.urls import path

from authentication import views

app_name = 'authentication'
urlpatterns = [
    path('', views.SignInView.as_view(), name='sign_in'),
    path('redirect-session', views.redirect_session, name='redirect_session'),
]
