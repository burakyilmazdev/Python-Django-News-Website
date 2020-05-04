from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from news.models import CommentFormu, Comments


def index(request):
    return HttpResponse("News Page")


@login_required(login_url='/login')
def addcomment(request, id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        form = CommentFormu(request.POST)
        if form.is_valid():
            current_user = request.user

            data = Comments()
            data.user_id = current_user.id
            data.news_id = id
            data.subject = form.cleaned_data['subject']
            data.comment = form.cleaned_data['comment']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            messages.success(request, "Yorumunuz gönderildi")
            return HttpResponseRedirect(url)

    messages.warning(request, "Yorumunuz gönderilemedi")
    return HttpResponseRedirect(url)
