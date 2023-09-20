from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('get_news/', views.get_news, name='get_news'),
    path('techcrunch/', views.scrape_tech, name='techcrunch'),

]




