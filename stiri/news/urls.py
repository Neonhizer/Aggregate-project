# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.home, name='home'),
#     path('scrape/', views.scrape_techcrunch, name='scrape_techcrunch'),
#     path('news/scrape_security/', views.scrape_security, name='scrape_security'), 
    

# ]


from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('scrape/', views.scrape_techcrunch, name='scrape'),
    path('news/scrape_security/', views.scrape_security, name='scrape'),
    path('get_news/', views.get_news, name='get_news'),  
    path('scrape_security/', views.scrape_security, name='scrape_security'),
    path('scrape_decrypt/', views.scrape_decrypt, name='scrape_decrypt'),
    
]




    # path('get_news/', views.get_news, name='get_news'),
    # path('scrape/', views.scrape_techcrunch, name='scrape'),  
    # path('search/', views.search_results, name='search_results'),
    # path('search/category/', views.search_results_category, name='search_results_category'),
    # path('search/location/', views.search_results_location, name='search_results_location'),
    # path('search/topic/', views.search_results_topic, name='search_results_topic'),
    # path('search/author/', views.search_results_author, name='search_results_author'),
    # path('search/date/', views.search_results_date, name='search_results_date'),

