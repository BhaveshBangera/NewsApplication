from django.shortcuts import render, redirect
import requests
from .models import Topic
from .forms import TopicForm

# Create your views here.
def index(request):
    #All news related to any particular keyword
    url = 'https://newsapi.org/v2/everything?q={}&apiKey=f5b4332785144768b04e4dcecaf70ad1'
    #For top headlines of any country
    #url = 'https://newsapi.org/v2/top-headlines?country=in&apiKey=f5b4332785144768b04e4dcecaf70ad1'
    #For top headlines of any news channel
    #url = 'https://newsapi.org/v2/top-headlines?sources=abc-news&apiKey=f5b4332785144768b04e4dcecaf70ad1'
    #For everything of any news channel
    #url = 'https://newsapi.org/v2/everything?sources=abc-news&apiKey=f5b4332785144768b04e4dcecaf70ad1'
    #Total Publishers all over the world
    #url = 'https://newsapi.org/v2/sources?apiKey=f5b4332785144768b04e4dcecaf70ad1'
    #Total Publishers from any country
    #url = 'https://newsapi.org/v2/sources?country=us&apiKey=f5b4332785144768b04e4dcecaf70ad1'

    if request.method == 'POST':
        form = TopicForm(request.POST)
        form.save()
        return redirect('newsapp:index')

    form = TopicForm()
    #Finding the Latest Topic name
    topicname = Topic.objects.all().order_by('-id')[0]
    #Printing the Latest Topic name
    print(topicname)
    #Type of the Latest Topic name - object type
    print(type(topicname))
    #Converting the Latest Topic name to string type
    strname = str(topicname)
    #Checking the Type of the Latest Topic name after converting it to String type
    print(type(strname))
    #Removing spaces between the string
    cleanedname = strname.replace(" ", "")
    #Printing the string after removing spaces
    print(cleanedname)
    #Sending the string without spaces to the requests and fetching the data
    r = requests.get(url.format(cleanedname), verify=False).json()
    #Creating a articles list
    articles_data = []
    #Checking the length of fetched articles and printing it
    totalarticles = len(r['articles'])
    print(totalarticles)
    #Looping through all the articles, storing each article data in a dictionary and then appending it to the list
    for x in range(totalarticles):
        post = {
          'sourcename': r['articles'][x]['source']['name'],
          'author': r['articles'][x]['author'],
          'title': r['articles'][x]['title'],
          'description': r['articles'][x]['description'],
          'url': r['articles'][x]['url'],
          'urlToImage': r['articles'][x]['urlToImage'],
          'publishedAt': r['articles'][x]['publishedAt']
        }
        articles_data.append(post)

    print(len(articles_data))
    #Sending list data, length of the fetched articles and form to the url
    context = {'articles_data': articles_data,'totalarticles': totalarticles, 'form': form}
    return render(request, 'news/headlines.html', context)
