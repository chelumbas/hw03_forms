from django.core.paginator import Paginator
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from .models import Post, Group, User
from .forms import PostForm

POSTS_TO_DISPLAY = 10
CHARACTERS_FOR_TITLE = 30


def get_page_objects(object_list, request):
    paginator = Paginator(object_list=object_list, per_page=POSTS_TO_DISPLAY)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)


def index(request):
    posts = Post.objects.all()
    page_obj = get_page_objects(posts, request)
    title = 'Последние обновления на сайте'
    context = {
        'title': title,
        'page_obj': page_obj
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()
    page_obj = get_page_objects(posts, request)
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    posts = author.posts.all()
    page_obj = get_page_objects(posts, request)
    context = {
        'author': author,
        'post_count': author.posts.count(),
        'page_obj': page_obj,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    title = f'Пост {post.text[0:CHARACTERS_FOR_TITLE]}'
    context = {
        'post': post,
        'title': title,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
@csrf_exempt
def post_create(request):
    form = PostForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('posts:profile', post.author.username)
    context = {
        'form': form,
        'title': 'Добавить запись',
    }
    return render(request, 'posts/create_post.html', context)


@login_required
@csrf_exempt
def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = PostForm(request.POST, instance=post)
    if form.is_valid():
        post.save()
        return redirect('posts:post_detail', post_id)
    context = {
        'is_edit': True,
        'form': form,
        'title': 'Редактировать запись',
    }
    return render(request, 'posts/create_post.html', context)
