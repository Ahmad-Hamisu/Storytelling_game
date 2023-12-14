from django.urls import path
from .views import story_list, story_detail, create_story, contribute_tweet, like_story
from . import views

urlpatterns = [
    path('', story_list, name='story_list'),
    path('<int:story_id>/', story_detail, name='story_detail'),
    path('create/', create_story, name='create_story'),
    path('<int:story_id>/contribute_tweet/',
         contribute_tweet, name='contribute_tweet'),
    path('', views.home, name='home'),
    path('like_story/<int:story_id>/', like_story, name='like_story'),


]
