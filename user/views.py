from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from content.models import Menu
from home.models import UserProfile
from news.models import Category, News, Comments, NewsForm, NewsImageForm, Images
from user.forms import UserUpdateForm, ProfileUpdateForm


def index(request):
    category = Category.objects.all()
    menu = Menu.objects.all()
    current_user = request.user
    profile = UserProfile.objects.get(user_id=current_user.id)
    context = {'category': category,
               'profile': profile,
               'menu': menu}
    return render(request, 'user_profile.html', context)


def user_update(request):
    menu = Menu.objects.all()
    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)

        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated')
            return redirect('/user')

    else:
        category = Category.objects.all()
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.userprofile)
        context = {
            'category': category,
            'user_form': user_form,
            'profile_form': profile_form,
            'menu': menu
        }

        return render(request, 'user_update.html', context)


def change_password(request):
    menu = Menu.objects.all()
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password has been updated')
            return redirect('change_password')
        else:
            messages.warning(request, "Error")
            return HttpResponseRedirect('/user/password')

    else:
        category = Category.objects.all()
        form = PasswordChangeForm(request.user)
        return render(request, 'change_password.html', {
            'form': form, 'category': category, 'menu': menu,
        })


@login_required(login_url='/login')
def mynews(request):
    menu = Menu.objects.all()
    category = Category.objects.all()
    current_user = request.user
    news = News.objects.filter(user_id=current_user).order_by('-id')
    context = {
        'category': category,
        'news': news,
        'menu': menu
    }

    return render(request, 'user_news.html', context)


@login_required(login_url='/login')
def comments(request):
    menu = Menu.objects.all()
    category = Category.objects.all()
    current_user = request.user
    comments = Comments.objects.filter(user_id=current_user).order_by('-id')
    context = {
        'category': category,
        'comments': comments,
        'menu': menu
    }
    return render(request, 'user_comments.html', context)


@login_required(login_url='/login')
def deletecomment(request, id):
    current_user = request.user
    Comments.objects.filter(id=id, user_id=current_user.id).delete()
    messages.success(request, 'Comment has been deleted')
    return HttpResponseRedirect('/user/comments')


@login_required(login_url='/login')
def addnews(request):
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            current_user = request.user
            data = News()
            data.user_id = current_user.id
            data.title = form.cleaned_data['title']
            data.keywords = form.cleaned_data['keywords']
            data.description = form.cleaned_data['description']
            data.image = form.cleaned_data['image']
            data.category = form.cleaned_data['category']
            data.slug = form.cleaned_data['slug']
            data.detail = form.cleaned_data['detail']
            data.status = 'New'
            data.save()
            messages.success(request, 'Your news has been added!')
            return HttpResponseRedirect('/user/mynews')
        else:
            messages.warning(request, "Error")
            return HttpResponseRedirect('/user/addnews')

    else:
        news = News.objects.all()
        category = Category.objects.all()
        menu = Menu.objects.all()
        form = NewsForm()
        context = {
            'category': category,
            'form': form,
            'menu': menu,
            'news': news,
        }
        return render(request, 'user_addnews.html', context)


@login_required(login_url='/login')
def newsedit(request, id):
    news = News.objects.get(id=id)
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES, instance=news)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your news has been updated!')
            return HttpResponseRedirect('/user/mynews')
        else:
            messages.warning(request, "Error")
            return HttpResponseRedirect('/user/newsedit' + str(id))

    else:
        category = Category.objects.all()
        menu = Menu.objects.all()
        form = NewsForm(instance=news)
        context = {
            'category': category,
            'form': form,
            'menu': menu,
            'news': news,
        }
        return render(request, 'user_addnews.html', context)


@login_required(login_url='/login')
def newsdelete(request, id):
    current_user = request.user
    News.objects.filter(id=id, user_id=current_user.id).delete()
    messages.success(request, 'News has been deleted')
    return HttpResponseRedirect('/user/mynews')


def newsaddimage(request, id):
    if request.method == 'POST':
        lasturl = request.META.get('HTTP_REFERER')
        form = NewsImageForm(request.POST,request.FILES)

        if form.is_valid():
            data = Images()
            data.title= form.cleaned_data['title']
            data.news_id = id
            data.image = form.cleaned_data['image']
            data.save()
            messages.success(request, 'Your image has been uploaded!')
            return HttpResponseRedirect(lasturl)
        else:
            messages.warning(request, "Error")
            return HttpResponseRedirect(lasturl)

    else:
        news = News.objects.get(id=id)
        category = Category.objects.all()
        images=Images.objects.filter(news_id=id)
        form = NewsImageForm
        context = {
            'news': news,
            'images': images,
            'form': form,
            'category':category,
        }
        return render(request, 'news_gallery.html', context)
