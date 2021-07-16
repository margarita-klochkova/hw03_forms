from .forms import PostForm
from django.shortcuts import get_object_or_404, render, redirect
from .models import Group, Post
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required


User = get_user_model()


def index(request):
    post_list = Post.objects.all().order_by('-pub_date')
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'index.html', {'page': page, })


def posts_group(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group).order_by("-pub_date")
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, "group.html", {"group": group, 'page': page})


def profile(request, username):
    author = get_object_or_404(User, username=username)
    count = author.posts.count()
    post = author.posts.all()
    paginator = Paginator(post, 10)
    page_num = request.GET.get('page')
    page = paginator.get_page(page_num)
    context = {
        "author": author,
        "post": post,
        "count": count,
        "page": page
    }
    return render(request, "profile.html", context)


def post_view(request, username, post_id):
    author = User.objects.get(username=username)
    count = author.posts.count()
    post = author.posts.get(id=post_id)
    context = {
        "author": author,
        "count": count,
        "post": post, }
    return render(request, "post.html", context)


@login_required
def new_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('/')
    form = PostForm()
    return render(request, "new_post.html", {'form': form, 'new': True})


def post_edit(request, username, post_id):
    post = get_object_or_404(Post, author__username=username, pk=post_id)
    if request.user == post.author:
        form = PostForm(request.POST or None, instance=post)
        if form.is_valid():
            form.save()
            return redirect(f'/{username}/{post_id}')
        return render(request, 'new_post.html',
                      {'form': form,
                       'username': username,
                       'post_id': post_id})
    return redirect(f'/{username}/{post_id}')
