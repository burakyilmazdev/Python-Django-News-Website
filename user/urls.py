from django.urls import path

from . import views

urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),
    path('update/', views.user_update, name='user_update'),
    path('password/', views.change_password, name='change_password'),
    path('mynews/', views.mynews, name='mynews'),
    path('comments/', views.comments, name='comments'),
    path('deletecomment/<int:id>', views.deletecomment, name='deletecomment'),
    path('newsedit/<int:id>', views.newsedit, name='newsedit'),
    path('newsdelete/<int:id>', views.newsdelete, name='newsdelete'),
    path('addnews/', views.addnews, name='addnews'),
    path('newsaddimage/<int:id>',views.newsaddimage,name='newsaddimage'),
    # ex: /polls/5/
    # path('<int:question_id>/', views.detail, name='detail'),

]
