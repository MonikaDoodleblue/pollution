from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('home/', views.home, name='home'),
    path('prediction/', views.predict, name="predict"),
    path('news/', views.news, name='news'),
    path('chart/', views.chart, name="chart"),
    path('favicon.ico', RedirectView.as_view(
        url='/static/favicon.ico', permanent=True)),
]