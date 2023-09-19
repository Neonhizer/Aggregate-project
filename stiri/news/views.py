import requests
from bs4 import BeautifulSoup
from django.shortcuts import render
from pymongo import MongoClient
from .models import Article
from django.http import JsonResponse
from django.http import HttpResponse

import logging



# def scrape_techcrunch(request):
    
#     url = "https://techcrunch.com/"
#     response = requests.get(url)
#     if response.status_code == 200:
#         soup = BeautifulSoup(response.text, 'html.parser')
#         articles = soup.find_all('article')
#         article_data = []

#         for article in articles:
#             title = article.find('h3').get_text()
#             link = article.find('a')['href']

#             #image_element = soup.select('figure.post-block__media img')
#             #image = image_element[0]['src'] if image_element else None
                        

           


#             author_element = article.find('p', class_='fi-main-block__byline').find('a', href=True)
#             author = author_element.get_text() if author_element else ''
            

#             article_data.append({
#                 'title': title,
#                 'link': link,
#             #    'image': image,
#                 'author': author,
#             })

#         context = {
#             'articles': article_data,
#         }
#         # Save the articles in the MongoDB database
#         client = MongoClient('localhost', 27017)
#         db = client['news']
#         news_collection = db['techcrunch_news']

#         for data in article_data:
#             news_collection.insert_one(data)

#         return render(request, 'news/test.html', context)



    







# def scrape_security(request):
#     url = "https://www.securityweek.com"
#     response = requests.get(url)
#     context = {'articles': []}

#     if response.ok and response.status_code == 200:
#         soup = BeautifulSoup(response.text, 'html.parser')
#         articles = soup.find_all('article')

#         article_data = []

#         for article in articles:
#             title_element = article.find('h1', class_='zox-post-title')
#             title = title_element.get_text() if title_element else ''
#             print("Titlu:", title)

#             article_data.append({
#                 'title': title,
#             })

#         client = MongoClient('localhost', 27017)
#         db = client['news']
#         news_collection = db['security_news']

#         for data in article_data:
#             news_collection.insert_one(data)

#         context['articles'] = article_data

#     return render(request, 'news/scrape_security.html', context)



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

            # image_element = soup.select('figure.post-block__media img')
            # image = image_element[0]['src'] if image_element else None

            author_element = article.find('p', class_='fi-main-block__byline').find('a', href=True)
            author = author_element.get_text() if author_element else ''

            article_data.append({
                'title': title,
                'link': link,
                # 'image': image,
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









def scrape_security(request):
    
    logging.basicConfig(filename='scrape_security.log', level=logging.ERROR)
    
    url = "https://www.securityweek.com/"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        logging.error(f"Failed to fetch data from SecurityWeek. Status code: {response.status_code}")
        return HttpResponse('Failed to fetch data from SecurityWeek')
    
    soup = BeautifulSoup(response.text, 'html.parser')
    articles = soup.find_all('div', class_='news-post')
    article_data = []

    for article in articles:
        title_element = article.find('h2', class_='news-post-title')
        title = title_element.a.get_text() if title_element else ''
        link = title_element.a['href'] if title_element else ''

        article_data.append({
            'title': title,
            'link': link,
        })

    
    client = MongoClient('localhost', 27017)
    db = client['news']
    news_collection = db['securityweeks_news'] 
    
    for data in article_data:
        news_collection.insert_one(data)

    context = {
        'articles': article_data,
    }

    return render(request, 'news/scrape_security.html', context)











def scrape_decrypt(request):
    url = "https://decrypt.co/"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = soup.find_all('div', class_='article-list-item')
        article_data = []

        for article in articles:
            title = article.find('h2', class_='article-title').get_text()
            author = article.find('span', class_='author-name').get_text()
            link = article.find('a')['href']

            article_data.append({
                'title': title,
                'author': author,
                'link': link,
            })

        context = {
            'articles': article_data,
        }

 
        client = MongoClient('localhost', 27017)
        db = client['news']
        news_collection = db['decrypt_news']

        for data in article_data:
            news_collection.insert_one(data)

        return render(request, 'news/scrape_decrypt.html', context)
    else:
        return HttpResponse('Failed to fetch data from Decrypt')















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


# # def index(request):
# #     return HttpResponse('Hello, world!')






