from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),
    path('scrape_techcrunch/', views.scrape_techcrunch, name='scrape_techcrunch'),
    path('get_news/', views.get_news, name='get_news'),
]
