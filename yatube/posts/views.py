from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import cache_page

from .forms import CommentForm, PostForm
from .models import Comment, Follow, Group, Post, User
from .utils import get_page_obj


@cache_page(20)
def index(request: HttpRequest) -> HttpResponse:
    post_list = Post.objects.select_related('author', 'group').all()
    context = {
        'page_obj': get_page_obj(request, post_list),
    }
    return render(request, 'posts/index.html', context)


def group_posts(request: HttpRequest, slug: str) -> HttpResponse:
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.all()
    context = {
        'group': group,
        'page_obj': get_page_obj(request, post_list),
    }
    return render(request, 'posts/group_list.html', context)


def profile(request: HttpRequest, username: str) -> HttpResponse:
    user = get_object_or_404(User, username=username)
    post_list = Post.objects.filter(
        author=user).prefetch_related('author', 'group').all()
    if not request.user.is_anonymous:
        following = user.following.filter(user=request.user).exists()
    else:
        following = False

    context = {
        'author': user,
        'page_obj': get_page_obj(request, post_list),
        'following': following
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request: HttpRequest, post_id: int) -> HttpResponse:
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST or None)

    comments = post.comments.all()
    context = {
        'post': post,
        'form': form,
        'comments': comments
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request: HttpRequest) -> HttpResponse:
    form = PostForm(
        request.POST or None,
        files=request.FILES or None
    )
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('posts:profile', username=request.user)

    context = {
        'form': form,
    }
    return render(request, 'posts/create_post.html', context)


@login_required
def post_edit(request: HttpRequest, post_id: int) -> HttpResponse:
    post = get_object_or_404(Post, pk=post_id)

    if request.user != post.author:
        return redirect('posts:post_detail', post_id=post_id)

    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post
    )
    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', post_id=post_id)

    context = {
        'is_edit': True,
        'form': form,
    }
    return render(request, 'posts/create_post.html', context)


@login_required
def add_comment(request: HttpRequest, post_id: int):
    post = get_object_or_404(Post, pk=post_id)

    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment: Comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
        return redirect('posts:post_detail', post_id=post_id)


@login_required
def follow_index(request: HttpRequest):
    author_list = [follow.author for follow in request.user.follower.all()]

    post_list = Post.objects.select_related(
        'author', 'group').filter(author__in=author_list)
    context = {
        'page_obj': get_page_obj(request, post_list),
    }
    return render(request, 'posts/follow.html', context)


@login_required
def profile_follow(request: HttpRequest, username: str):
    # Подписаться на автора
    author = get_object_or_404(User, username=username)
    is_signed = request.user.follower.filter(author=author).exists()
    if username != request.user.username and not is_signed:
        Follow.objects.create(user=request.user, author=author)
    return redirect('posts:profile', username=username)


@login_required
def profile_unfollow(request: HttpRequest, username: str):
    # Дизлайк, отписка
    author = get_object_or_404(User, username=username)
    Follow.objects.filter(user=request.user).filter(author=author).delete()
    return redirect('posts:profile', username=username)
