import requests
from bs4 import BeautifulSoup
from django.shortcuts import render
from pymongo import MongoClient
from .models import Article  
from django.http import JsonResponse
from .models import Article


def scrape_techcrunch(request):
    url = "https://techcrunch.com/"

    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = soup.find_all('article')
        article_data = []

        for article in articles:
            title = article.find('h2').get_text()
            link = article.find('a')['href']
            image_tag = article.find('img')
            image = image_tag['src'] if image_tag else ''
            author_tag = article.find('span', class_='river-byline__authors')
            author = author_tag.get_text() if author_tag else ''

            article_data.append({
                'title': title,
                'link': link,
                'image': image,
                'author': author,
            })

        # Save the articles in the MongoDB database
        client = MongoClient('localhost', 27017) 
        db = client['news'] 
        news_collection = db['techcrunch_news']  

        for data in article_data:
            news_collection.insert_one(data)

    return render(request, 'news/scrape_techcrunch.html')

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
        'titles': [Article.title for stire in news],
        'links': [Article.url for stire in news],
    }

    # Return the data as JSON
    return JsonResponse(news_data)