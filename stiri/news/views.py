import requests
from bs4 import BeautifulSoup
from django.shortcuts import render
from pymongo import MongoClient
from .models import Article
from django.http import JsonResponse
from django.http import HttpResponse
import pymongo
import logging
from django.http import HttpRequest
from urllib.parse import urljoin




def home(request):
    # Fetch all the articles from the database
    articles = Article.objects.all()


    context = {
        'articles': articles,
    }

    return render(request, 'news/home.html', context)

def get_news(request):
    # Extract all the news from the database
    news = Article.objects.all()

    news_data = {
        'titles': [article.title for article in news],
        'links': [article.url for article in news],
    }

    # Return the data as JSON
    return JsonResponse(news_data)





# # def search_results(request):
# #     if'search_term' in request.GET and request.GET["search_term"]:
# #         search_term = request.GET.get("search_term")
# #         searched_articles = Article.search_by_title(search_term)
# #         message = f"{search_term}"




def scrape_tech(request: HttpRequest):
    
    urls = [
        'https://techcrunch.com',
    ]

    article_data = []
    base_url = 'https://techcrunch.com'  

   
    client = MongoClient("mongodb://localhost:27017/")  
    db = client["news"]  
    news_collection = db["techcrunch"]  

    for url in urls:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            if 'techcrunch.com' in url:
                articles = soup.find_all('div', class_='post-block')

                for article in articles:
                    title = article.find('h2').get_text()
                    author = article.find('span', class_='river-byline__authors').get_text()
                    article_relative_url = article.find('a')['href']

                    # Check if the article URL is relative or absolute and correct accordingly
                    if not article_relative_url.startswith('http:'):
                        article_url = urljoin(base_url, article_relative_url)
                    else:
                        article_url = article_relative_url

                   
                    image_element = article.find('img')
                    image_url = image_element['src'] if image_element else None

                    # Check if the image URL is valid and if the article doesn't already exist in the collection
                    existing_article = news_collection.find_one({'article_url': article_url})
                    if image_url and not existing_article:
                        article_data.append({
                            'title': title,
                            'author': author,
                            'article_url': article_url,
                            'image_url': image_url,
                        })

   # Insert the data into the MongoDB collection
    if article_data:
        news_collection.insert_many(article_data)

        # Retrieve data from MongoDB to display in the HTML template
    sort_option = request.GET.get('sort', '')  # Get the sorting option from the request
    if sort_option == 'author':
        articole = news_collection.find().sort('author', 1)  
    elif sort_option == 'title':
        articole = news_collection.find().sort('title', 1) 
    else:
        articole = news_collection.find()

   
    client.close()

    
    return render(request, 'news/test_techcrunch.html', {'articole': articole, 'sort_option': sort_option})



