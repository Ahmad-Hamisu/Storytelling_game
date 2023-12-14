from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .forms import StoryForm
from django.shortcuts import render, redirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Story
from .forms import StoryForm, TweetForm
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login


def story_list(request):
    stories = Story.objects.all()
    return render(request, 'story_list.html', {'stories': stories})


def story_detail(request, story_id):
    story = get_object_or_404(Story, pk=story_id)
    return render(request, 'story_detail.html', {'story': story})


@login_required
def create_story(request):
    if request.method == 'POST':
        form = StoryForm(request.POST)
        if form.is_valid():
            story = form.save()
            return redirect('story_detail', story_id=story.id)
    else:
        form = StoryForm()

    return render(request, 'create_story.html', {'form': form})


def like_story(request, story_id):
    story = get_object_or_404(Story, id=story_id)
    user = request.user

    if user in story.likes.all():
        story.likes.remove(user)
        liked = False
    else:
        story.likes.add(user)
        liked = True

    return JsonResponse({'likes': story.likes.count(), 'liked': liked})


@login_required
def contribute_tweet(request, story_id):
    story = get_object_or_404(Story, pk=story_id)

    if request.method == 'POST':
        form = TweetForm(request.POST)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.story = story
            tweet.save()
            story.current_tweet = tweet
            story.save()
            return redirect('story_detail', story_id=story.id)
    else:
        form = TweetForm()
    return render(request, 'contribute_tweet.html', {'form': form, 'story': story})


def home(request):
    return render(request, 'home.html')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Authenticate and log in the user
            user = authenticate(
                request, username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            login(request, user)
            # Redirect to a different page after signup, e.g., the story list
            return redirect('story_list')
    else:
        form = UserCreationForm()

    return render(request, 'registration/signup.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome, {username}!')
                # Replace 'home' with the name of your home page URL pattern
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})
