import requests
from bs4 import BeautifulSoup
from django.shortcuts import render
from pymongo import MongoClient
from .models import Article
from django.http import JsonResponse




def scrape_techcrunch(request):
    
    url = "https://techcrunch.com/"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = soup.find_all('article')
        article_data = []

        for article in articles:
            title = article.find('h3').get_text()
            link = article.find('a')['href']
            
            image_element = soup.select_one('figure.post-block__media img')
            image = image_element['src'] if image_element else None
            

           


            author_element = article.find('p', class_='fi-main-block__byline').find('a', href=True)
            author = author_element.get_text() if author_element else ''
            

            article_data.append({
                'title': title,
                'link': link,
                'image': image,
                'author': author,
            })

        context = {
            'articles': article_data,
        }
        # Save the articles in the MongoDB database
        client = MongoClient('localhost', 27017)
        db = client['news']
        news_collection = db['techcrunch_news']

        for data in article_data:
            news_collection.insert_one(data)

    return render(request, 'news/scrape_techcrunch.html', context)
    

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







# def search_results(request):
#     if'search_term' in request.GET and request.GET["search_term"]:
#         search_term = request.GET.get("search_term")
#         searched_articles = Article.search_by_title(search_term)
#         message = f"{search_term}"


# def index(request):
#     return HttpResponse('Hello, world!')

