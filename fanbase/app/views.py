from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.shortcuts import get_object_or_404
from .models import Post

def frontpage(request):
    posts = Post.objects.all().order_by('-posted_date')
    return render(request,"app/index.html", {"posts":posts}) 

@login_required(login_url='/login/')  # ログインが必要なビューにデコレータを追加
def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    # ログインが必要な記事かどうかのチェック
    if post.is_private and not request.user.is_authenticated:
        return redirect('/login/')  # ログインページにリダイレクト
    return render(request, "app/post_detail.html", {"post": post})

# ユーザー新規登録（sign up）
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'app/signup.html', {'form': form})

# ログイン機能
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            # ユーザーの存在を確認
            if User.objects.filter(username=username).exists():
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('/')
            else:
                form.add_error(None, 'User does not exist.')
        else:
            form.add_error(None, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'app/index.html', {'form': form, 'logged_in': request.user.is_authenticated})

# ログアウト機能
def user_logout(request):
    logout(request)
    return redirect('/')