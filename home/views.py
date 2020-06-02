from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.core.serializers import json
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from content.models import Menu, Content, CImages
from home.forms import SearchForm, RegisterForm
from home.models import Setting, ContactFormu, ContactFormMessage, FAQ, UserProfile
from news.models import News, Category, Images, Comments
import json


def index(request):
    setting = Setting.objects.get(pk=1)
    sliderdata = News.objects.all()[:6]
    category = Category.objects.all()
    menu = Menu.objects.all()
    lastnews = News.objects.filter(status="True").order_by('-id')[:4]
    randomnews = News.objects.filter(status="True").order_by('?')[:4]
    events = Content.objects.filter(type='etkinlik').order_by('-id')[:3]
    announcements = Content.objects.filter(type='duyuru').order_by('-id')[:3]

    context = {'setting': setting,
               'category': category,
               'page': 'home',
               'menu': menu,
               'sliderdata': sliderdata,
               'lastnews': lastnews,
               'randomnews': randomnews,
               'events': events,
               'announcements': announcements}
    return render(request, 'index.html', context)


def aboutus(request):
    setting = Setting.objects.get(pk=1)
    menu = Menu.objects.all()
    category = Category.objects.all()
    context = {'setting': setting,
               'page': 'aboutus',
               'category': category,
               'menu': menu}
    return render(request, 'aboutus.html', context)


def contact(request):
    category = Category.objects.all()
    menu = Menu.objects.all()
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
               'category': category,
               'menu': menu}
    return render(request, 'contact.html', context)


def category_news(request, id, slug):
    category = Category.objects.all()
    categorydata = Category.objects.get(pk=id)
    news = News.objects.filter(category_id=id,status="True")
    menu = Menu.objects.all()
    context = {'news': news,
               'category': category,
               'categorydata': categorydata,
               'menu': menu,
               }
    return render(request, 'news.html', context)


def news_detail(request, id, slug):
    category = Category.objects.all()
    news = News.objects.get(pk=id)
    images = Images.objects.filter(news_id=id)
    menu = Menu.objects.all()
    comments = Comments.objects.filter(news_id=id, status='True')
    context = {'news': news,
               'category': category,
               'images': images,
               'comments': comments,
               'menu': menu}
    return render(request, 'news_detail.html', context)


def news_search(request):
    menu = Menu.objects.all()
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            category = Category.objects.all()
            query = form.cleaned_data['query']
            news = News.objects.filter(title__icontains=query)

            context = {'news': news,
                       'category': category,
                       'menu': menu, }
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


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')

        else:
            messages.warning(request, "Hatalı kullanıcı adı veya şifre!")
            return HttpResponseRedirect('/login')

    category = Category.objects.all()
    menu = Menu.objects.all()
    context = {'category': category,
               'menu': menu}
    return render(request, 'login.html', context)


def signup_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)

            current_user = request.user
            data = UserProfile()
            data.user_id = current_user.id
            data.image = "images/users/user.png"
            data.save()
            messages.success(request, "Üye olundu,Hoşgeldiniz!")
            return HttpResponseRedirect('/user')
        else:
            messages.warning(request, "Bu kullanıcı adı veya email kullanılıyor!")

    form = RegisterForm()
    category = Category.objects.all()
    menu = Menu.objects.all()
    context = {'category': category,
               'form': form,
               'menu': menu
               }
    return render(request, 'signup.html', context)


def menu(request, id):
    try:
        content = Content.objects.get(menu_id=id)
        link = '/content/' + str(content.id) + '/menu'
        return HttpResponseRedirect(link)
    except:
        messages.warning(request, "İçerik bulunamadı!")
        link = '/error'
        return HttpResponseRedirect(link)


def contentdetail(request, id, slug):
    category = Category.objects.all()
    menu = Menu.objects.all()
    content = Content.objects.get(pk=id)
    images = CImages.objects.filter(content_id=id)

    context = {'content': content,
               'category': category,
               'menu': menu,
               'images': images, }
    return render(request, 'content_detail.html', context)


def error(request):
    category = Category.objects.all()
    menu = Menu.objects.all()

    context = {'category': category,
               'menu': menu,
               }
    return render(request, 'error.html', context)


def faq(request):
    category = Category.objects.all()
    menu = Menu.objects.all()
    faq = FAQ.objects.all().order_by('number')

    context = {'category': category,
               'menu': menu,
               'faq': faq,
               }
    return render(request, 'faq.html', context)
