from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import PostForm, UserProfileForm

def register_view(request):
    if request.user.is_authenticated:
        return redirect('post_list')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('post_list')
    else:
        form = UserCreationForm()

    for field_name, field in form.fields.items():
        field.widget.attrs['class'] = 'form-input'

    context = {
        'form': form
    }
    return render(request, 'core_app/register.html', context)

def login_view(request):
    if request.user.is_authenticated:
        return redirect('post_list')
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('post_list')
    else:
        form = AuthenticationForm()
    context = {
        'form' : form
    }
    return render(request, 'core_app/login.html', context)

def logout_view(request):
    logout(request)
    return redirect('login_view')

def post_list(request):
    posts = Post.objects.all()
    context = {
        'posts' : posts
    }
    return render(request, "core_app/posts.html", context)

@login_required(login_url='login')
def create_post_view(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('post_list')
    else:
        form = PostForm()
    context = {
        'form' : form
    }
    return render(request, 'core_app/create.html', context)

@login_required(login_url='login')
def update_post_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.user == request.user or request.user.is_superuser:
        if request.method == 'POST':
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                form.save()
                return redirect('post_list')
        else:
            form = PostForm(instance=post)
        context = {
            'form' : form
        }
        return render(request, 'core_app/Edit.html', context)


@login_required(login_url='login')
def delete_post_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.user == request.user or request.user.is_superuser:
        if request.method == 'POST':
            post.delete()
            return redirect('post_list')
        context = {
            'post' : post
        }
        return render(request, 'core_app/delete.html', context)

@login_required(login_url='login')
def edit_profile_view(request):
    user = request.user
    profile = user.profile  # assume OneToOneField exists

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            # Save username
            form.save()

            # Save avatar URL to profile
            avatar = form.cleaned_data.get('avatarURL')
            if avatar:
                profile.avatarURL = avatar
                profile.save()

            return redirect('post_list')  # or another page after saving
    else:
        # Pre-fill form with current username and avatar URL
        form = UserProfileForm(initial={
            'username': user.username,
            'avatarURL': profile.avatarURL
        })
    context = {
        'form': form,
        'profile': profile
    }
    return render(request, 'core_app/profile.html', context)