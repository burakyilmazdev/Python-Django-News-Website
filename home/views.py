from django.contrib import messages
from django.core.serializers import json
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from home.forms import SearchForm
from home.models import Setting, ContactFormu, ContactFormMessage
from news.models import News, Category, Images, Comments


def index(request):
    setting = Setting.objects.get(pk=1)
    sliderdata = News.objects.all()[:6]
    category = Category.objects.all()
    lastnews = News.objects.all().order_by('-id')[:4]
    randomnews = News.objects.all().order_by('?')[:4]

    context = {'setting': setting,
               'category': category,
               'page': 'home',
               'sliderdata': sliderdata,
               'lastnews': lastnews,
               'randomnews': randomnews}
    return render(request, 'index.html', context)


def aboutus(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    context = {'setting': setting,
               'page': 'aboutus',
               'category': category}
    return render(request, 'aboutus.html', context)


def contact(request):
    category = Category.objects.all()
    if request.method == 'POST':
        form = ContactFormu(request.POST)
        if form.is_valid():
            data = ContactFormMessage()
            data.name = form.cleaned_data['name']
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            messages.success(request, "Mesajınız gönderildi")
            return HttpResponseRedirect('/contact')

    setting = Setting.objects.get(pk=1)
    form = ContactFormu()
    context = {'setting': setting,
               'form': form,
               'category': category}
    return render(request, 'contact.html', context)


def category_news(request, id, slug):
    category = Category.objects.all()
    categorydata = Category.objects.get(pk=id)
    news = News.objects.filter(category_id=id)
    context = {'news': news,
               'category': category,
               'categorydata': categorydata
               }
    return render(request, 'news.html', context)


def news_detail(request, id, slug):
    category = Category.objects.all()
    news = News.objects.get(pk=id)
    images = Images.objects.filter(news_id=id)
    comments = Comments.objects.filter(news_id=id, status='True')
    context = {'news': news,
               'category': category,
               'images': images,
               'comments': comments}
    return render(request, 'news_detail.html', context)


def news_search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            category = Category.objects.all()
            query = form.cleaned_data['query']
            news = News.objects.filter(title__icontains=query)

            context = {'news': news,
                       'category': category, }
            return render(request, 'news_search.html', context)

        return HttpResponseRedirect('/')


def news_search_auto(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        news = News.objects.filter(title__icontains=q)
        results = []
        for rs in news:
            news_json = {}
            news_json = rs.title
            results.append(news_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)
