from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import cache_page

from .forms import CommentForm, PostForm, SearchForm
from .models import Comment, Follow, Group, Post, User
from .utils import paginate

NUMBER_OF_POSTS: int = 10
INDEX_CACHE_TIME = 20


@cache_page(INDEX_CACHE_TIME, key_prefix='index_page')
def index(request):
    posts = Post.objects.select_related('author', 'group')
    page_obj = paginate(request, posts, NUMBER_OF_POSTS)
    form = SearchForm
    context = {
        'page_obj': page_obj,
        'form': form
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.select_related('author')
    page_obj = paginate(request, posts, NUMBER_OF_POSTS)
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    current_author = get_object_or_404(User, username=username)
    posts = current_author.posts.all()
    following = (request.user.is_authenticated and Follow.objects.filter(
        user=request.user,
        author=current_author).exists()
    )
    page_obj = paginate(request, posts, NUMBER_OF_POSTS)
    context = {
        'author': current_author,
        'page_obj': page_obj,
        'following': following
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    selected_post = get_object_or_404(Post, pk=post_id)
    post_count = selected_post.author.posts.count()
    form = CommentForm()
    comments = Comment.objects.filter(post=post_id)

    context = {
        'post': selected_post,
        'post_count': post_count,
        'is_author': selected_post.author == request.user,
        'form': form,
        'comments': comments,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    form = PostForm(request.POST or None, files=request.FILES or None,)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('posts:profile', post.author)
    return render(request, 'posts/create_post.html', {'form': form})


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if post.author != request.user:
        return redirect('posts:post_detail', post_id)

    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post,
    )
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('posts:post_detail', post_id)
    context = {
        'form': form,
        'post': post,
        'is_edit': True,
    }
    return render(request, 'posts/create_post.html', context)


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('posts:post_detail', post_id=post_id)


@login_required
def follow_index(request):
    posts = (
        Post.objects.filter(author__following__user=request.user)
        .select_related('author', 'group')
    )
    page_obj = paginate(request, posts, NUMBER_OF_POSTS)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/follow.html', context)


@login_required
def profile_follow(request, username):
    user = User.objects.get(username=username)
    if (
        not User.objects.filter(
            username=user,
            following__user=request.user,
        ).exists()
        and user != request.user
    ):

        following = Follow.objects.create(user=request.user, author=user)
        following.save()
    return redirect('posts:profile', username)


@login_required
def profile_unfollow(request, username):
    user = User.objects.get(username=username)
    Follow.objects.filter(user=request.user, author=user).delete()
    return redirect('posts:profile', username)
