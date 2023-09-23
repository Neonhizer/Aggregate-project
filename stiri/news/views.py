import requests
from bs4 import BeautifulSoup
from django.shortcuts import render
from pymongo import MongoClient
from .models import Article
from django.http import JsonResponse
from django.http import HttpRequest
from urllib.parse import urljoin



def home(request):
    return render(request, 'news/home.html')



# def home(request):
#     # Fetch all the articles from the database
#     articles = Article.objects.all()


#     context = {
#         'articles': articles,
#     }

#     return render(request, 'news/home.html', context)

def get_news(request):
    # Extract all the news from the database
    news = Article.objects.all()

    news_data = {
        'titles': [article.title for article in news],
        'links': [article.url for article in news],
    }

    # Return the data as JSON
    return JsonResponse(news_data)


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



                    
                    short_description_element = article.find('div', class_='post-block__content')
                    short_description = short_description_element.get_text()
                    
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
                            'short_description': short_description,
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

    
    return render(request, 'news/techcrunch.html', {'articole': articole, 'sort_option': sort_option})






def scrape_thehackernews(request):
    client = MongoClient('localhost', 27017)
    db = client.news
    thehackernews_collection = db.thehackernews

    url = 'https://thehackernews.com'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    articles = soup.find_all('div', class_='body-post')

    # Get the search query from the GET parameters (in search)
    search_query = request.GET.get('q', '')

    
    filtered_articles = []

    for article in articles:
        title_element = article.find('h2', class_='home-title')
        title = title_element.text.strip() if title_element else 'N/A'

        img_element = article.find('img')
        img_url = img_element['data-src'].strip() if img_element else None

        article_link = article.find('a')['href']



        existing_article = thehackernews_collection.find_one({'article_url': article_link})
        if img_url and not existing_article:
            article_response = requests.get(article_link)
            article_soup = BeautifulSoup(article_response.text, 'html.parser')
            first_paragraph = article_soup.find('div', class_='articlebody').find('p')
            short_description = first_paragraph.text.strip() if first_paragraph else 'N/A'

            article_data = {
                'title': title,
                'img_url': img_url,
                'link': article_link,
                'short_description': short_description
            }

           
            if search_query.lower() in title.lower() or search_query.lower() in short_description.lower():
                filtered_articles.append(article_data)

            try:
                thehackernews_collection.insert_one(article_data)
            except Exception as e:
                print(f"Eroare la inserarea datelor: {str(e)}")

    articles_data = list(thehackernews_collection.find())
    context = {'articles_data': filtered_articles, 'search_query': search_query}
    return render(request, 'news/thehackernews.html', context)
