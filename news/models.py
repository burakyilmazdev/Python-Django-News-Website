from unicodedata import category

from ckeditor.widgets import CKEditorWidget
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.forms import ModelForm, TextInput, Textarea, Select, FileInput, DateField, ModelChoiceField
from django.urls import reverse
from django.utils.safestring import mark_safe
from ckeditor_uploader.fields import RichTextUploadingField
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


class Category(MPTTModel):
    STATUS = (
        ('True', 'Evet'),
        ('False', 'Hayır'),

    )

    title = models.CharField(blank=True, max_length=100)
    keywords = models.CharField(blank=True, max_length=255)
    description = models.CharField(blank=True, max_length=255)
    image = models.ImageField(blank=True, upload_to='images/')
    status = models.CharField(max_length=10, choices=STATUS)

    slug = models.SlugField(null=False, unique=True)
    parent = TreeForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class MPTTMeta:
        order_insertion_by = ['title']

    def __str__(self):
        full_path = [self.title]
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return ' --> '.join(full_path[::-1])

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))

    image_tag.short_description = 'Image'

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})


class News(models.Model):
    STATUS = (
        ('True', 'Evet'),
        ('New', 'Yeni'),
        ('False', 'Hayır'),
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=150)
    keywords = models.CharField(blank=True, max_length=255)
    description = models.CharField(blank=True, max_length=255)
    image = models.ImageField(blank=True, upload_to='images/')
    slug = models.SlugField(null=False, unique=True)
    detail = RichTextUploadingField()
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def _str_(self):
        return self.title

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))

    image_tag.short_description = 'Image'

    def get_absolute_url(self):
        return reverse('news_detail', kwargs={'slug': self.slug})


class Images(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    title = models.CharField(max_length=150, blank=True)
    image = models.ImageField(blank=True, upload_to='images/')

    def _str_(self):
        return self.title

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))

    image_tag.short_description = 'Image'


class NewsImageForm(ModelForm):
    class Meta:
        model = Images
        fields = ['title', 'image']


class Comments(models.Model):
    STATUS = (
        ('True', 'Evet'),
        ('New', 'Yeni'),
        ('False', 'Hayır'),

    )
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    comment = models.TextField(max_length=200, blank=True)
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    ip = models.CharField(blank=True, max_length=20)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return self.subject


class CommentFormu(ModelForm):
    class Meta:
        model = Comments
        fields = ['subject', 'comment']


class NewsForm(ModelForm):
    class Meta:
        model = News
        queryset = Category.objects.all()
        fields = ['category', 'title', 'keywords', 'description', 'image', 'slug', 'detail']
        widgets = {
            'category': Select(attrs={'class': 'input', 'placeholder': 'category'}, choices=queryset),
            'title': TextInput(attrs={'class': 'input', 'placeholder': 'title'}),
            'keywords': TextInput(attrs={'class': 'input', 'placeholder': 'keywords'}),
            'description': TextInput(attrs={'class': 'input', 'placeholder': 'description'}),
            'image': FileInput(attrs={'class': 'input', 'placeholder': 'image'}),
            'slug': TextInput(attrs={'class': 'input', 'placeholder': 'slug'}),
            'detail': CKEditorWidget(),

        }
