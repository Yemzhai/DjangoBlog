from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.generic import View
from .models import *
from .forms import TagForm, PostForm
from .utils import *
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q





def posts_list(request):
    search_query = request.GET.get('search', '')

    if search_query:
        posts =Post.objects.filter(Q(title__icontains=search_query)|
                                   Q(body__icontains=search_query)|
                                   Q(description__icontains=search_query)
                                   )

    else:
        posts = Post.objects.all()
    paginator = Paginator(posts, 4)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)

    #page pagination
    is_paginated = page.has_other_pages()
    if page.has_previous():
        prev_url = '?page={}'.format(page.previous_page_number())
    else:
        prev_url = ''
    if page.has_next():
        next_url = '?page={}'.format(page.next_page_number())
    else:
        next_url = ''

    dict = {
        'pages': page,
        'is_paginated': is_paginated,
        'next_url': next_url,
        'prev_url': prev_url
    }
    # searching

    return render(request, 'blog/index.htm', dict)

class PostDetail(ObjectDetailMixin, View):
    model = Post
    template = 'blog/post_detail.htm'

class PostCreate(LoginRequiredMixin, ObjectCreateMixin, View):
    model_form = PostForm
    template = 'blog/post_create.htm'
    raise_exception = True

class PostUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
    model = Post
    model_form = PostForm
    template = 'blog/post_update.htm'
    raise_exception = True

class PostDelete(LoginRequiredMixin, ObjectDeleteMixin, View):
    model = Post
    template = 'blog/post_delete.htm'
    url_name = 'posts_list_url'
    raise_exception = True









def tags_list(request):
    tags = Tag.objects.all()
    return render(request, 'blog/tags_list.htm', {'tags':tags})

class TagDetail(ObjectDetailMixin, View):
    model = Tag
    template = 'blog/tag_detail.htm'

class TagCreate(LoginRequiredMixin, ObjectCreateMixin, View):
    model_form = TagForm
    template = 'blog/tag_create.htm'
    raise_exception = True


class TagUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
    model = Tag
    model_form = TagForm
    template = 'blog/tag_update.htm'
    raise_exception = True

class TagDelete(LoginRequiredMixin, ObjectDeleteMixin, View):
    model = Tag
    template = 'blog/tag_delete.htm'
    url_name = 'tags_list_url'
    raise_exception = True




